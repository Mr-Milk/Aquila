mod config;
mod db;
mod routes;
mod schema;

use actix_files as fs;
use actix_web::{get, post, web, App, HttpResponse, HttpServer, Responder};
use anyhow::Result;
use db::DataRecords;
use dotenv::dotenv;
use sqlx::postgres::PgPoolOptions;
use sqlx::PgPool;

#[get("/")]
async fn hello() -> impl Responder {
    println! {"Get /index"};
    HttpResponse::Ok().body("Hello world!")
}

#[actix_web::main]
async fn main() -> Result<()> {
    dotenv().ok();

    let config = crate::config::Config::from_env().unwrap();
    let db_pool = PgPoolOptions::new()
        .max_connections(config.max_connections)
        .connect(&config.database_url)
        .await?;

    let mut server = HttpServer::new(move || {
        App::new()
            .data(db_pool.clone())
            .service(hello)
            .service(fs::Files::new("/static", "./").show_files_listing())
            .configure(routes::data_records_init)
            .configure(routes::data_stats_init)
            .configure(routes::roi_info_init)
    })
    .bind(format!("{}:{}", config.host, config.port))?;

    server.run().await?;

    Ok(())
}
