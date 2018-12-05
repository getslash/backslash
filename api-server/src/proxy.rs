use actix_web::{
    client,
    http::header::{HeaderName, HeaderValue},
    AsyncResponder, Error, HttpMessage, HttpRequest, HttpResponse,
};
use futures::future::ok;
use futures::Future;
use log::error;
use state::AppState;
use stats::{RequestEnded, RequestStarted, RequestTimes};
use std::iter::Iterator;
use std::time::Duration;
use utils::LoggedResult;

const PROXY_VERSION: &'static str = env!("CARGO_PKG_VERSION");

// TODO: support compressed data end-to-end (pending on https://github.com/actix/actix-web/issues/350)

pub fn forward(req: &HttpRequest<AppState>) -> Box<Future<Item = HttpResponse, Error = Error>> {
    let state = req.state();
    let peer = req
        .headers()
        .get("X-Real-IP")
        .and_then(|h| h.to_str().log_err().ok())
        .and_then(|ip| ip.parse().log_err().ok())
        .or_else(|| req.peer_addr().map(|addr| addr.ip()));
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

    client_req
        .send()
        .map_err(Error::from)
        .then(move |res| {
            let endpoint = res
                .as_ref()
                .ok()
                .and_then(|resp| resp.headers().get("x-api-endpoint"))
                .and_then(|header| header.to_str().ok())
                .map(String::from);
            stats_collector
                .try_send(RequestEnded {
                    timing: RequestTimes::from_headers(res.as_ref().ok()),
                    endpoint,
                    is_success: res
                        .as_ref()
                        .map(|resp| resp.status())
                        .map(|s| s.is_success())
                        .unwrap_or(false),
                    peer,
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
    client_resp.header("X-Backslash-API-Server", PROXY_VERSION);

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
