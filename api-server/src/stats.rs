use actix::prelude::*;
use actix_web::{http::StatusCode, AsyncResponder, HttpRequest, Responder};
use aggregators::{CountHistorgram, RequestDurations};
use failure::Error;
use futures::Future;
use state::AppState;
use std::collections::HashMap;
use std::fmt::Write;
use std::net::IpAddr;
use std::time::Duration;

const HISTOGRAM_RESOLUTION_SECONDS: usize = 60;
const HISTOGRAM_NUM_BINS: usize = 10;

pub struct StatsCollector {
    aggs: HashMap<String, RequestDurations>,
    clients: HashMap<IpAddr, CountHistorgram>,
    num_sessions: u64,
    num_tests: u64,
}

impl StatsCollector {
    pub fn init() -> StatsCollector {
        StatsCollector {
            aggs: HashMap::new(),
            clients: HashMap::new(),
            num_tests: 0,
            num_sessions: 0,
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

pub struct RequestInfo {
    pub(crate) path: String,
    pub(crate) peer: Option<IpAddr>,
    pub(crate) timing: Duration,
    pub(crate) status: StatusCode,
}

impl Message for RequestInfo {
    type Result = ();
}

impl Handler<RequestInfo> for StatsCollector {
    type Result = ();

    fn handle(&mut self, msg: RequestInfo, _ctx: &mut Context<Self>) {
        if msg.status.is_success() {
            if msg.path == "/api/report_test_start" {
                self.num_tests += 1;
            } else if msg.path == "/api/report_session_start" {
                self.num_sessions += 1;
            }
        }

        let agg = self
            .aggs
            .entry(msg.path)
            .or_insert_with(RequestDurations::init);
        agg.ingest(msg.timing);

        if let Some(addr) = msg.peer {
            let hist = self
                .clients
                .entry(addr)
                .or_insert_with(|| CountHistorgram::init(HISTOGRAM_NUM_BINS));
            hist.inc();
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

            endpoints: self
                .aggs
                .iter()
                .map(|(k, v)| (k.to_string(), v.into()))
                .collect(),

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

pub struct Stats {
    endpoints: HashMap<String, EndpointStats>,

    clients: HashMap<String, ClientStats>,

    num_sessions: u64,
    num_tests: u64,
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

        write_gauge_map(
            &mut returned,
            "backslash_request_avg_latency",
            &self.endpoints,
            "endpoint",
            |v| v.avg_latency,
            "Average API latency per endpoint",
        );

        write_gauge_map(
            &mut returned,
            "request_min_latency",
            &self.endpoints,
            "endpoint",
            |v| v.min_latency,
            "Minimum API latency per endpoint",
        );

        write_gauge_map(
            &mut returned,
            "backslash_request_max_latency",
            &self.endpoints,
            "endpoint",
            |v| v.max_latency,
            "Maximum API latency per endpoint",
        );

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

impl<'a> From<&'a RequestDurations> for EndpointStats {
    fn from(durations: &'a RequestDurations) -> EndpointStats {
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
