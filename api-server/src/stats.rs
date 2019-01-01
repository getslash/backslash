use actix::prelude::*;
use actix_web::{AsyncResponder, HttpRequest, Query, Responder, State};
use aggregators::{CountHistorgram, DurationAggregator};
use failure::Error;
use state::AppState;
use std::collections::HashMap;
use std::fmt::Write;
use std::net::IpAddr;
use std::time::Duration;
use utils::duration_from_secs;

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
}

pub(crate) trait RequestTimesMap {
    fn ingest<'a>(&mut self, path: &str, timing: Duration);
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

#[derive(Debug, Deserialize)]
pub struct RequestInfo {
    pub(crate) endpoint: Option<String>,
    pub(crate) peer: Option<IpAddr>,
    pub(crate) total: f64,
    pub(crate) active: f64,
    pub(crate) db: f64,
}

impl Message for RequestInfo {
    type Result = ();
}

impl Handler<RequestInfo> for StatsCollector {
    type Result = ();

    fn handle(&mut self, msg: RequestInfo, _ctx: &mut Context<Self>) {
        if let Some(endpoint) = msg.endpoint {
            self.total_times
                .ingest(&endpoint, duration_from_secs(msg.total));
            self.active_times
                .ingest(&endpoint, duration_from_secs(msg.active));
            self.db_times.ingest(&endpoint, duration_from_secs(msg.db));

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

enum EntityType {
    Session,
    Test,
}

struct EntityStarted(EntityType);

impl Message for EntityStarted {
    type Result = ();
}

impl Handler<EntityStarted> for StatsCollector {
    type Result = ();

    fn handle(&mut self, msg: EntityStarted, _ctx: &mut Context<Self>) {
        match msg.0 {
            EntityType::Session => self.num_sessions += 1,
            EntityType::Test => self.num_tests += 1,
        };
    }
}

pub struct QueryStats;

impl Message for QueryStats {
    type Result = Result<String, Error>;
}

impl Handler<QueryStats> for StatsCollector {
    type Result = Result<String, Error>;

    fn handle(&mut self, _msg: QueryStats, _ctx: &mut Self::Context) -> Self::Result {
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
            &mut returned, "backslash_internal_timers_size",
            (self.total_times.len() + self.active_times.len() + self.db_times.len()) as u64,
            "Size of timer map held by metrics server"
        );

        write_gauge(
            &mut returned, "backslash_internal_client_map_size",
            self.clients.len() as u64,
            "Size of timer map held by metrics server"
        );

        write_latency_group(&mut returned, "total", &self.total_times);
        write_latency_group(&mut returned, "active", &self.active_times);
        write_latency_group(&mut returned, "db", &self.db_times);

        write_gauge_map(
            &mut returned,
            "backslash_client_requests_1m",
            &self.clients,
            "client",
            |v| v.get_current(),
            "Number of requests from client in the last 1 minute",
        );

        write_gauge_map(
            &mut returned,
            "backslash_client_requests_10m",
            &self.clients,
            "client",
            |v| v.get_total(),
            "Number of requests from client in the last 10 minutes",
        );
        Ok(returned)
    }
}

fn write_gauge(writer: &mut Write, name: &str, value: u64, help: &str) {
    write!(
        writer,
        "# HELP {0} {1}\n# TYPE {0} gauge\n{0} {2}\n",
        name, help, value
    )
    .unwrap();
}

fn write_latency_group(
    writer: &mut Write,
    name: &str,
    values: &HashMap<String, DurationAggregator>,
) {
    write_gauge_map(
        writer,
        &format!("backslash_request_avg_{}_latency", name),
        &values,
        "endpoint",
        |v| v.average_secs(),
        &format!("Average API {} latency per endpoint", name),
    );

    write_gauge_map(
        writer,
        &format!("backslash_request_min_{}_latency", name),
        &values,
        "endpoint",
        |v| v.min_secs().unwrap(),
        &format!("Minimum API {} latency per endpoint", name),
    );

    write_gauge_map(
        writer,
        &format!("backslash_request_max_{}_latency", name),
        &values,
        "endpoint",
        |v| v.max_secs().unwrap(),
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
    for (index, (key, value)) in values.iter().enumerate() {
        if index == 0 {
            write!(writer, "# HELP {0} {1}\n# TYPE {0} gauge\n", name, help,).unwrap();
        }
        write!(
            writer,
            "{}{{{}=\"{}\"}} {}\n",
            name,
            key_name,
            key,
            encode(value)
        )
        .unwrap();
    }
}

pub fn render(req: &HttpRequest<AppState>) -> impl Responder {
    req.state().stats_collector.send(QueryStats).responder()
}

pub fn update((state, timing): (State<AppState>, Query<RequestInfo>)) -> &'static str {
    state.stats_collector.do_send(timing.into_inner());
    "ok"
}

pub fn notify_session_start(state: State<AppState>) -> &'static str {
    state
        .stats_collector
        .do_send(EntityStarted(EntityType::Session));
    "ok"
}

pub fn notify_test_start(state: State<AppState>) -> &'static str {
    state
        .stats_collector
        .do_send(EntityStarted(EntityType::Test));
    "ok"
}
