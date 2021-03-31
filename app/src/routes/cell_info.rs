use actix_web::{get, HttpResponse, Responder, web};
use serde::Serialize;
use sqlx::PgPool;

use crate::db::{CellInfo, CellExp};
use crate::routes::response::{error_response, json_response};


#[get("/cell_info/{roi_id}")]
async fn cell_info(roi_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    let result = CellInfo::get_cell_info(roi_id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(info) => json_response(info),
        Err(e) => error_response(e),
    }
}


#[get("/cell_exp/{roi_id}/{marker}")]
async fn cell_exp(query: web::Path<(String, String)>, db_pool: web::Data<PgPool>) -> impl Responder {
    let query = query.into_inner();
    let result = CellExp::get_roi_exp(query.0, query.1,db_pool.get_ref()).await;
    match result {
        Ok(info) => json_response(info),
        Err(e) => error_response(e),
    }
}


pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(cell_info);
    cfg.service(cell_exp);
}