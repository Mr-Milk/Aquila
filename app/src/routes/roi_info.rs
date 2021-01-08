use crate::db::{CellInfo, ROIInfo};
use crate::schema::QueryData;
use actix_web::{get, web, HttpResponse, Responder};
use serde::Serialize;
use sqlx::PgPool;

#[get("/roi/{data_id}")]
async fn roi_levels(data_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    println!("Get /roi/{:?}", data_id);
    let result = ROIInfo::get_roi_info(data_id.into_inner(), db_pool.get_ref()).await;
    println!("fetch db");
    match result {
        Ok(info) => HttpResponse::Ok().json(info),
        _ => HttpResponse::BadRequest().body("Error"),
    }
}

#[get("/cell_info/{roi_id}")]
async fn cell_info(roi_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    println!("Get /cell_info/{:?}", roi_id.clone());
    let result = CellInfo::get_cell_info(roi_id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(info) => HttpResponse::Ok().json(info),
        _ => HttpResponse::BadRequest().body("Error"),
    }
}

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(roi_levels);
    cfg.service(cell_info);
}
