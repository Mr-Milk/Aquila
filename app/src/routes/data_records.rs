use actix_web::{get, HttpResponse, Responder, web};
use sqlx::PgPool;

use crate::db::DataRecords;
use crate::routes::response::{error_response, json_response};

#[get("/data_ids")]
async fn data(db_pool: web::Data<PgPool>) -> impl Responder {
    let result = DataRecords::all_data_ids(db_pool.get_ref()).await;
    match result {
        Ok(data_ids) => json_response(data_ids),
        _ => error_response(),
    }
}

#[get("/dbstats")]
async fn dbstats(db_pool: web::Data<PgPool>) -> impl Responder {
    let result = DataRecords::dbstats(db_pool.get_ref()).await;
    match result {
        Ok(stats) => json_response(stats),
        _ => error_response(),
    }
}

// #[get("/data/query")]
// async fn query_data(selector: web::Query<QueryData>, db_pool: web::Data<PgPool>) -> impl Responder {
//     println!("Get /data/query {}", selector.clone());
//     let result = DataRecords::filter_data_ids(selector.clone(), db_pool.get_ref()).await;
//     match result {
//         Ok(data_ids) => HttpResponse::Ok().json(data_ids),
//         _ => HttpResponse::BadRequest().body("Error"),
//     }
// }

#[get("/records")]
async fn records(db_pool: web::Data<PgPool>) -> impl Responder {
    let result = DataRecords::all_records(db_pool.get_ref()).await;
    match result {
        Ok(records) => json_response(records),
        _ => error_response(),
    }
}

#[get("/records/{data_id}")]
async fn one_records(data_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    let result = DataRecords::one_record(data_id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(record) => json_response(record),
        _ => error_response(),
    }
}

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(data);
    cfg.service(dbstats);
    // cfg.service(query_data);
    cfg.service(records);
    cfg.service(one_records);
}
