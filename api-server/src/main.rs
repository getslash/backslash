#![deny(warnings)]
extern crate actix;
extern crate actix_web;
extern crate clap;
extern crate env_logger;
extern crate failure;
extern crate futures;
extern crate log;
extern crate url;

mod aggregators;
mod state;
mod stats;

use actix::prelude::*;
use actix_web::{
    client, server, App, AsyncResponder, Error, HttpMessage, HttpRequest, HttpResponse,
};
use clap::{value_t, Arg};
use env_logger::Builder;
use futures::Future;
use log::{error, info};
use state::AppState;
use stats::{RequestEnded, RequestStarted, StatsCollector};
use std::net::ToSocketAddrs;
use std::time::{Duration, SystemTime};

fn forward(req: &HttpRequest<AppState>) -> Box<Future<Item = HttpResponse, Error = Error>> {
    let start_time = SystemTime::now();
    let state = req.state();
    let path = req.uri().path().to_string();
    let peer = req.peer_addr();
    let mut new_url = state.forward_url.clone();
    let stats_collector = state.stats_collector.clone();
    new_url.set_path(req.uri().path());
    new_url.set_query(req.uri().query());

    stats_collector
        .try_send(RequestStarted)
        .unwrap_or_else(|e| error!("Failed sending request start notification: {:?}", e));

    client::ClientRequest::build_from(req)
        .no_default_headers()
        .timeout(Duration::from_secs(30))
        .uri(new_url)
        .streaming(req.payload())
        .unwrap()
        .send()
        .map_err(Error::from)
        .then(move |res| {
            let timing = SystemTime::now()
                .duration_since(start_time)
                .unwrap_or_else(|_| Duration::new(0, 0));

            stats_collector
                .try_send(RequestEnded {
                    timing,
                    path,
                    is_success: res
                        .as_ref()
                        .map(|resp| resp.status())
                        .map(|s| s.is_success())
                        .unwrap_or(false),
                    peer: peer.map(|a| a.ip()),
                }).unwrap_or_else(|e| error!("Failed sending request end notification: {:?}", e));
            res
        }).and_then(move |resp| {
            let mut client_resp = HttpResponse::build(resp.status());
            for (header_name, header_value) in
                resp.headers().iter().filter(|(h, _)| *h != "connection")
            {
                client_resp.header(header_name.clone(), header_value.clone());
            }
            Ok(client_resp.streaming(resp.payload()))
        }).responder()
}

fn main() {
    Builder::new()
        .filter_module("api_server", log::LevelFilter::Debug)
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
            .resource("/metrics", |r| r.f(stats::render))
            .default_resource(|r| {
                r.f(forward);
            })
    }).workers(32)
    .bind((listen_addr, listen_port))
    .expect("Cannot bind listening port");

    server.system_exit().start();
    system.run();
}
