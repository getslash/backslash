#![deny(warnings)]
extern crate actix;
extern crate actix_web;
extern crate env_logger;
extern crate failure;
extern crate futures;
extern crate log;
extern crate serde;
#[macro_use]
extern crate serde_derive;
extern crate sentry;
extern crate sentry_actix;
extern crate structopt;
extern crate url;

mod aggregators;
mod state;
mod stats;
mod utils;

use actix::prelude::*;
use actix_web::{server, App};
use env_logger::Builder;
use log::info;
use state::AppState;
use stats::StatsCollector;
use std::env;
use std::net::IpAddr;
use structopt::StructOpt;

#[derive(StructOpt, Debug)]
#[structopt(name = "basic")]
struct Opt {
    listen_addr: IpAddr,
    listen_port: u16,
}

fn main() {
    let _guard = sentry::init(env::var("SENTRY_DSN").ok());
    env::set_var("RUST_BACKTRACE", "1");
    sentry::integrations::panic::register_panic_handler();

    Builder::new()
        .filter_module("api_server", log::LevelFilter::Debug)
        .init();

    let opt = Opt::from_args();

    info!("Backslash API Backend Starting...");

    let system = System::new("system");

    let stats_collector = StatsCollector::init().start();

    let server = server::new(move || {
        App::with_state(AppState::init(stats_collector.clone()))
            .resource("/metrics/request", |r| {
                r.post().with(stats::update);
            })
            .resource("/metrics/session_start", |r| {
                r.post().with(stats::notify_session_start);
            })
            .resource("/metrics/test_start", |r| {
                r.post().with(stats::notify_test_start);
            })
            .resource("/metrics", |r| {
                r.get().f(stats::render);
            })
    })
    .bind((opt.listen_addr, opt.listen_port))
    .expect("Cannot bind listening port");

    server.system_exit().start();
    system.run();
}
