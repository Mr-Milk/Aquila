use actix_files as fs;
use actix_web::{App, get, HttpResponse, HttpServer, Responder};
use actix_web::middleware::{Logger, DefaultHeaders};
use env_logger::Env;
use anyhow::Result;
use dotenv::dotenv;
use sqlx::postgres::PgPoolOptions;

mod config;
mod db;
mod routes;
mod schema;

#[get("/")]
async fn hello() -> impl Responder {
    HttpResponse::Ok().body("Hi! This is the API of Aquila: The spatial single cell pathology database")
}

#[actix_web::main]
async fn main() -> Result<()> {
    env_logger::Builder::from_env(
        Env::default().default_filter_or("info")
    ).init();

    dotenv().ok();

    let config = crate::config::Config::from_env().unwrap();
    let db_pool = PgPoolOptions::new()
        .max_connections(config.max_connections)
        .connect(&config.database_url)
        .await?;

    let server = HttpServer::new(move || {
        App::new()
            .wrap(Logger::default())
            .wrap(DefaultHeaders::new()
                .header("Access-Control-Allow-Origin", "*")
                .header("Access-Control-Allow-Credentials", "true"))
            .data(db_pool.clone())
            .service(hello)
            .service(fs::Files::new("/static", "../scripts/data").show_files_listing())
            .configure(routes::data_records_init)
            .configure(routes::data_stats_init)
            .configure(routes::roi_info_init)
            .configure(routes::cell_info_init)
    })
    .bind(format!("{}:{}", config.host, config.port))?;

    server.run().await?;

    Ok(())
}
