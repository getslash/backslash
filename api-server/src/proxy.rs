use actix_web::{
    client,
    http::header::{HeaderName, HeaderValue},
    AsyncResponder, Error, HttpMessage, HttpRequest, HttpResponse,
};
use futures::future::ok;
use futures::Future;
use log::error;
use state::AppState;
use stats::{RequestEnded, RequestStarted};
use std::iter::Iterator;
use std::time::{Duration, SystemTime};

// TODO: support compressed data end-to-end (pending on https://github.com/actix/actix-web/issues/350)

pub fn forward(req: &HttpRequest<AppState>) -> Box<Future<Item = HttpResponse, Error = Error>> {
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

    let mut req_builder = client::ClientRequest::build();

    req_builder.method(req.method().clone());
    req_builder.no_default_headers();
    req_builder.timeout(Duration::from_secs(30));
    req_builder.uri(new_url);

    for (header_name, header_value) in req
        .headers()
        .iter()
        .filter(should_pass_header)
        // We filter out content-length to avoid invalid length for compressed post data
        .filter(|(name, _)| *name != "content-length")
    {
        req_builder.header(header_name, header_value.clone());
    }

    let client_req = req_builder.streaming(req.payload()).unwrap();
    println!("Client req: {:?}", client_req);

    client_req
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
        }).and_then(construct_response)
        .responder()
}

fn construct_response(
    resp: client::ClientResponse,
) -> Box<dyn Future<Item = HttpResponse, Error = Error>> {
    let mut client_resp = HttpResponse::build(resp.status());
    for (header_name, header_value) in resp.headers().iter().filter(should_pass_header) {
        client_resp.header(header_name.clone(), header_value.clone());
    }
    //    Ok(client_resp.streaming(resp.payload()))
    if resp.chunked().unwrap_or(false) {
        Box::new(ok(client_resp.streaming(resp.payload())))
    } else {
        Box::new(
            resp.body()
                .from_err()
                .and_then(move |body| Ok(client_resp.body(body))),
        )
    }
}

fn should_pass_header((header_name, header_value): &(&HeaderName, &HeaderValue)) -> bool {
    if *header_name == "connection" {
        false
    } else if *header_name == "content-encoding"
        && *header_value == HeaderValue::from_static("gzip")
    {
        false
    } else {
        true
    }
}
