use actix_web::{get, HttpResponse, Responder, web};
use sqlx::PgPool;

use crate::db::DataStats;

#[get("/stats/{data_id}")]
async fn stats(data_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    let result = DataStats::all_stats(data_id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(stats) => HttpResponse::Ok().json(stats),
        _ => HttpResponse::BadRequest().body("Error"),
    }
}

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(stats);
}
