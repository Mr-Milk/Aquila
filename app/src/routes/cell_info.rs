use actix_web::{get, HttpResponse, Responder, web};
use serde::Serialize;
use sqlx::PgPool;

use crate::db::CellInfo;
use crate::routes::response::{error_response, json_response};


#[get("/cell_info/{roi_id}")]
async fn cell_info(roi_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    let result = CellInfo::get_cell_info(roi_id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(info) => json_response(info),
        _ => error_response(),
    }
}


pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(cell_info);
}