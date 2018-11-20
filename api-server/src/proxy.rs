use actix_web::{
    client, http::header::HeaderValue, AsyncResponder, Error, HttpMessage, HttpRequest,
    HttpResponse,
};
use futures::future::ok;
use futures::Future;
use log::error;
use state::AppState;
use stats::{RequestEnded, RequestStarted};
use std::time::{Duration, SystemTime};

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
        }).and_then(construct_response)
        .responder()
}

fn construct_response(
    resp: client::ClientResponse,
) -> Box<dyn Future<Item = HttpResponse, Error = Error>> {
    let mut client_resp = HttpResponse::build(resp.status());
    for (header_name, header_value) in resp.headers().iter().filter(|(h, v)| {
        *h != "connection" && !(*h == "content-encoding" && *v != HeaderValue::from_static("gzip"))
    }) {
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
