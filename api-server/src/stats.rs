use actix::prelude::*;
use aggregators::{CountHistorgram, RequestDurations};
use failure::Error;
use std::collections::HashMap;
use std::net::IpAddr;
use std::time::Duration;

const HISTOGRAM_RESOLUTION_SECONDS: usize = 60;
const HISTOGRAM_NUM_BINS: usize = 10;

pub struct StatsCollector {
    aggs: HashMap<String, RequestDurations>,
    clients: HashMap<IpAddr, CountHistorgram>,
}

impl StatsCollector {
    pub fn init() -> StatsCollector {
        StatsCollector {
            aggs: HashMap::new(),
            clients: HashMap::new(),
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
}

impl Message for RequestInfo {
    type Result = ();
}

impl Handler<RequestInfo> for StatsCollector {
    type Result = ();

    fn handle(&mut self, msg: RequestInfo, _ctx: &mut Context<Self>) {
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

#[derive(Serialize)]
pub struct Stats {
    endpoints: HashMap<String, EndpointStats>,

    clients: HashMap<String, ClientStats>,
}

#[derive(Serialize)]
pub struct ClientStats {
    num_requests_1m: u64,
    num_requests_10m: u64,
}

#[derive(Serialize)]
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
