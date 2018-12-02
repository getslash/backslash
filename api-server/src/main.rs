#![deny(warnings)]
extern crate actix;
extern crate actix_web;
extern crate clap;
extern crate env_logger;
extern crate failure;
extern crate futures;
extern crate log;
extern crate sentry;
extern crate sentry_actix;
extern crate url;

mod aggregators;
mod proxy;
mod state;
mod stats;
mod utils;

use actix::prelude::*;
use actix_web::{server, App};
use clap::{value_t, Arg};
use env_logger::Builder;
use log::info;
use sentry_actix::SentryMiddleware;
use state::AppState;
use stats::StatsCollector;
use std::env;
use std::net::ToSocketAddrs;

fn main() {
    let _guard = sentry::init(env::var("SENTRY_DSN").ok());
    env::set_var("RUST_BACKTRACE", "1");
    sentry::integrations::panic::register_panic_handler();

    Builder::new()
        .filter_module("api_server", log::LevelFilter::Debug)
        .filter_module("actix", log::LevelFilter::Debug)
        .init();

    info!("Backslash API Backend Starting...");

    let matches = clap::App::new("Backslash API Server")
        .arg(
            Arg::with_name("listen_addr")
                .takes_value(true)
                .value_name("LISTEN ADDR")
                .index(1)
                .required(true),
        ).arg(
            Arg::with_name("listen_port")
                .takes_value(true)
                .value_name("LISTEN PORT")
                .index(2)
                .required(true),
        ).arg(
            Arg::with_name("forward_addr")
                .takes_value(true)
                .value_name("FWD ADDR")
                .index(3)
                .required(true),
        ).arg(
            Arg::with_name("forward_port")
                .takes_value(true)
                .value_name("FWD PORT")
                .index(4)
                .required(true),
        ).get_matches();

    let listen_addr = matches.value_of("listen_addr").unwrap();
    let listen_port = value_t!(matches, "listen_port", u16).unwrap_or_else(|e| e.exit());

    let forwarded_addr = matches.value_of("forward_addr").unwrap();
    let forwarded_port = value_t!(matches, "forward_port", u16).unwrap_or_else(|e| e.exit());

    let forwarded_addr = (forwarded_addr, forwarded_port)
        .to_socket_addrs()
        .expect("Cannot resolve address")
        .next()
        .unwrap();

    let system = System::new("system");

    let stats_collector = StatsCollector::init().start();

    let server = server::new(move || {
        App::with_state(AppState::init(stats_collector.clone(), forwarded_addr))
            .middleware(SentryMiddleware::new())
            .resource("/metrics", |r| r.f(stats::render))
            .default_resource(|r| {
                r.f(proxy::forward);
            })
    }).workers(32)
    .bind((listen_addr, listen_port))
    .expect("Cannot bind listening port");

    server.system_exit().start();
    system.run();
}
