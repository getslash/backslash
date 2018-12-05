use actix::prelude::*;
use actix_web::{
    client::ClientResponse, http::header::HeaderValue, AsyncResponder, HttpMessage, HttpRequest,
    Responder,
};
use aggregators::{CountHistorgram, DurationAggregator};
use failure::Error;
use futures::Future;
use state::AppState;
use std::collections::HashMap;
use std::fmt::Write;
use std::net::IpAddr;
use std::time::Duration;

const HISTOGRAM_RESOLUTION_SECONDS: usize = 60;
const HISTOGRAM_NUM_BINS: usize = 10;

// TODO: hashing requests should use Arc's, need to measure if performance justifies it
pub struct StatsCollector {
    total_times: HashMap<String, DurationAggregator>,
    active_times: HashMap<String, DurationAggregator>,
    db_times: HashMap<String, DurationAggregator>,
    clients: HashMap<IpAddr, CountHistorgram>,
    num_sessions: u64,
    num_tests: u64,
    num_pending_requests: u64,
}

/// A distilled snapshot of the stats
pub struct Stats {
    request_total_times: HashMap<String, EndpointStats>,
    request_active_times: HashMap<String, EndpointStats>,
    request_db_times: HashMap<String, EndpointStats>,

    clients: HashMap<String, ClientStats>,

    num_sessions: u64,
    num_tests: u64,
    num_pending_requests: u64,
}

pub(crate) trait RequestTimesMap {
    fn ingest<'a>(&mut self, path: &str, timing: Duration);

    fn as_endpoint_stats(&self) -> HashMap<String, EndpointStats>;
}

impl RequestTimesMap for HashMap<String, DurationAggregator> {
    fn ingest(&mut self, endpoint: &str, timing: Duration) {
        if let Some(durations) = self.get_mut(endpoint) {
            durations.ingest(timing);
            return;
        }
        let mut durations = DurationAggregator::init();
        durations.ingest(timing);
        self.insert(endpoint.to_string(), durations);
    }

    fn as_endpoint_stats(&self) -> HashMap<String, EndpointStats> {
        self.iter().map(|(k, v)| (k.clone(), v.into())).collect()
    }
}

impl StatsCollector {
    pub fn init() -> StatsCollector {
        StatsCollector {
            total_times: HashMap::new(),
            active_times: HashMap::new(),
            db_times: HashMap::new(),
            clients: HashMap::new(),
            num_tests: 0,
            num_sessions: 0,
            num_pending_requests: 0,
        }
    }
}

impl Actor for StatsCollector {
    type Context = Context<Self>;

    fn started(&mut self, ctx: &mut Self::Context) {
        ctx.run_interval(
            Duration::from_secs(HISTOGRAM_RESOLUTION_SECONDS as u64),
            |actor, mut _ctx| {
                actor.clients.retain(|_ip, counter| {
                    counter.rollover();
                    !counter.is_empty()
                })
            },
        );
    }
}

pub struct RequestStarted;

impl Message for RequestStarted {
    type Result = ();
}

impl Handler<RequestStarted> for StatsCollector {
    type Result = ();

    fn handle(&mut self, _msg: RequestStarted, _ctx: &mut Context<Self>) {
        self.num_pending_requests += 1;
    }
}

pub struct RequestEnded {
    pub(crate) endpoint: Option<String>,
    pub(crate) peer: Option<IpAddr>,
    pub(crate) timing: Option<RequestTimes>,
    pub(crate) is_success: bool,
}

#[derive(Debug)]
pub(crate) struct RequestTimes {
    pub(crate) total: Duration,
    pub(crate) active: Duration,
    pub(crate) db: Duration,
}

impl RequestTimes {
    pub(crate) fn from_headers(headers: Option<&ClientResponse>) -> Option<Self> {
        headers.map(|resp| resp.headers()).and_then(|headers| {
            Some(Self {
                total: duration_from_header(headers.get("X-Timing-Total"))?,
                active: duration_from_header(headers.get("X-Timing-Active"))?,
                db: duration_from_header(headers.get("X-Timing-DB"))?,
            })
        })
    }
}

fn duration_from_header(value: Option<&HeaderValue>) -> Option<Duration> {
    value
        .and_then(|header_value| header_value.to_str().ok())
        .and_then(|header_str| header_str.parse::<f64>().ok())
        .map(|secs: f64| Duration::from_millis((secs.max(0.) * 1000.) as u64))
}

impl Message for RequestEnded {
    type Result = ();
}

impl Handler<RequestEnded> for StatsCollector {
    type Result = ();

    fn handle(&mut self, msg: RequestEnded, _ctx: &mut Context<Self>) {
        self.num_pending_requests -= 1;

        if let Some(endpoint) = msg.endpoint {
            if msg.is_success {
                if endpoint == "api.report_test_start" {
                    self.num_tests += 1;
                } else if endpoint == "api.report_session_start" {
                    self.num_sessions += 1;
                }
            }

            if let Some(timing) = msg.timing {
                self.total_times.ingest(&endpoint, timing.total);
                self.active_times.ingest(&endpoint, timing.active);
                self.db_times.ingest(&endpoint, timing.db);

                if let Some(addr) = msg.peer {
                    let hist = self
                        .clients
                        .entry(addr)
                        .or_insert_with(|| CountHistorgram::init(HISTOGRAM_NUM_BINS));
                    hist.inc();
                }
            }
        }
    }
}

pub struct QueryStats;

impl Message for QueryStats {
    type Result = Result<Stats, Error>;
}

impl Handler<QueryStats> for StatsCollector {
    type Result = Result<Stats, Error>;

    fn handle(&mut self, _msg: QueryStats, _ctx: &mut Self::Context) -> Self::Result {
        Ok(Stats {
            num_tests: self.num_tests,
            num_sessions: self.num_sessions,
            num_pending_requests: self.num_pending_requests,

            request_total_times: self.total_times.as_endpoint_stats(),
            request_active_times: self.active_times.as_endpoint_stats(),
            request_db_times: self.db_times.as_endpoint_stats(),

            clients: self
                .clients
                .iter()
                .map(|(k, v)| {
                    (
                        k.to_string(),
                        ClientStats {
                            num_requests_1m: v.get_current(),
                            num_requests_10m: v.get_total(),
                        },
                    )
                }).collect(),
        })
    }
}

impl Stats {
    fn into_prometheus_metrics(&self) -> String {
        let mut returned = String::new();

        write_gauge(
            &mut returned,
            "backslash_num_new_sessions",
            self.num_sessions,
            "Number of sessions started since Backslash came up",
        );
        write_gauge(
            &mut returned,
            "backslash_num_new_tests",
            self.num_tests,
            "Number of tests started since Backslash came up",
        );

        write_gauge(
            &mut returned,
            "backslash_num_pending_requests",
            self.num_pending_requests,
            "Number of requests pending or being processed",
        );

        write_latency_group(&mut returned, "total", &self.request_total_times);
        write_latency_group(&mut returned, "active", &self.request_active_times);
        write_latency_group(&mut returned, "db", &self.request_db_times);

        write_gauge_map(
            &mut returned,
            "backslash_client_requests_1m",
            &self.clients,
            "client",
            |v| v.num_requests_1m,
            "Number of requests from client in the last 1 minute",
        );

        write_gauge_map(
            &mut returned,
            "backslash_client_requests_10m",
            &self.clients,
            "client",
            |v| v.num_requests_10m,
            "Number of requests from client in the last 10 minutes",
        );

        returned
    }
}

fn write_gauge(writer: &mut Write, name: &str, value: u64, help: &str) {
    write!(
        writer,
        "# HELP {0} {1}\n# TYPE {0} gauge\n{0} {2}\n",
        name, help, value
    );
}

fn write_latency_group(writer: &mut Write, name: &str, values: &HashMap<String, EndpointStats>) {
    write_gauge_map(
        writer,
        &format!("backslash_request_avg_{}_latency", name),
        &values,
        "endpoint",
        |v| v.avg_latency,
        &format!("Average API {} latency per endpoint", name),
    );

    write_gauge_map(
        writer,
        &format!("backslash_request_min_{}_latency", name),
        &values,
        "endpoint",
        |v| v.min_latency,
        &format!("Minimum API {} latency per endpoint", name),
    );

    write_gauge_map(
        writer,
        &format!("backslash_request_max_{}_latency", name),
        &values,
        "endpoint",
        |v| v.max_latency,
        &format!("Maximum API {} latency per endpoint", name),
    );
}

fn write_gauge_map<K, V, R, F>(
    writer: &mut Write,
    name: &str,
    values: &HashMap<K, V>,
    key_name: &str,
    encode: F,
    help: &str,
) where
    F: Fn(&V) -> R,
    R: std::fmt::Display,
    K: Eq + std::hash::Hash + std::fmt::Display,
{
    write!(writer, "# HELP {0} {1}\n# TYPE {0} gauge\n", name, help,);

    for (key, value) in values.iter() {
        write!(
            writer,
            "{}{{{}=\"{}\"}} {}\n",
            name,
            key_name,
            key,
            encode(value)
        );
    }
}

pub struct ClientStats {
    num_requests_1m: u64,
    num_requests_10m: u64,
}

pub struct EndpointStats {
    avg_latency: f64,
    min_latency: f64,
    max_latency: f64,
}

impl<'a> From<&'a DurationAggregator> for EndpointStats {
    fn from(durations: &'a DurationAggregator) -> EndpointStats {
        EndpointStats {
            avg_latency: durations.average_secs(),
            max_latency: durations.max_secs().unwrap(),
            min_latency: durations.min_secs().unwrap(),
        }
    }
}

pub fn render(req: &HttpRequest<AppState>) -> impl Responder {
    req.state()
        .stats_collector
        .send(QueryStats)
        .and_then(|stats| Ok(stats.unwrap().into_prometheus_metrics()))
        .responder()
}
