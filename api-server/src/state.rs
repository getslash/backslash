use actix::prelude::*;
use stats::StatsCollector;
use std::net::SocketAddr;
use url::Url;

pub struct AppState {
    pub(crate) forward_url: Url,
    pub(crate) stats_collector: Addr<StatsCollector>,
}

impl AppState {
    pub fn init(stats_collector: Addr<StatsCollector>, forward_addr: SocketAddr) -> AppState {
        AppState {
            stats_collector,
            forward_url: Url::parse(&format!("http://{}", forward_addr)).unwrap(),
        }
    }
}
