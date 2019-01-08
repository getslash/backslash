use actix::prelude::*;
use crate::stats::StatsCollector;

pub struct AppState {
    pub(crate) stats_collector: Addr<StatsCollector>,
}

impl AppState {
    pub fn init(stats_collector: Addr<StatsCollector>) -> AppState {
        AppState { stats_collector }
    }
}
