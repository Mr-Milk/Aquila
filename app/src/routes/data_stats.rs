use actix_web::{get, Responder, web};
use sqlx::PgPool;

use crate::db::DataStats;
use crate::routes::response::{error_response, json_response};

#[get("/stats/{data_id}")]
async fn stats(data_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    let result = DataStats::all_stats(data_id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(stats) => json_response(stats),
        Err(e) => error_response(e),
    }
}

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(stats);
}
