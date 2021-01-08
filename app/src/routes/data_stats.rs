use crate::db::DataStats;
use crate::schema::QueryData;
use actix_web::{get, web, HttpResponse, Responder};
use serde::Serialize;
use sqlx::PgPool;

#[get("/stats/{data_id}")]
async fn stats(data_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    println!("Get /stats {:?}", data_id);
    let result = DataStats::all_stats(data_id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(stats) => HttpResponse::Ok().json(stats),
        _ => HttpResponse::BadRequest().body("Error"),
    }
}

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(stats);
}
