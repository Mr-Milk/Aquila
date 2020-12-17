mod db;
mod config;
mod routes;
mod schema;

use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use dotenv::dotenv;
use db::DataRecords;
use sqlx::PgPool;
use sqlx::postgres::PgPoolOptions;
use anyhow::Result;
use listenfd::ListenFd;


#[get("/")]
async fn hello() -> impl Responder {
    println!{"Get /index"};
    HttpResponse::Ok().body("Hello world!")
}

#[post("/echo")]
async fn echo(req_body: String) -> impl Responder {
    HttpResponse::Ok().body(req_body)
}

async fn manual_hello() -> impl Responder {
    HttpResponse::Ok().body("Hey there!")
}

#[actix_web::main]
async fn main() -> Result<()> {

    dotenv().ok();

    let config = crate::config::Config::from_env().unwrap();
    let db_pool = PgPoolOptions::new()
        .max_connections(config.max_connections)
        .connect(&config.database_url).await?;

    let mut listenfd = ListenFd::from_env();
    let mut server = HttpServer::new(move || {
        App::new()
            .data(db_pool.clone())
            .service(hello)
            .service(echo)
            .route("/hey", web::get().to(manual_hello))
            .configure(routes::init)
    });

    server = if let Some(l) = listenfd.take_tcp_listener(0).unwrap(){
        server.listen(l)?
    } else {
        server.bind(format!("{}:{}", config.host, config.port))?
    };

    server.run().await?;

    Ok(())
}
