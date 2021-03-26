use actix_web::{get, Responder, web};
use sqlx::PgPool;

use crate::db::ROIInfo;
use crate::routes::response::{error_response, json_response};

#[get("/roi/{data_id}")]
async fn roi_info(data_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    let result = ROIInfo::roi_info(data_id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(info) => json_response(info),
        Err(e) => error_response(e),
    }
}

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(roi_info);
}
