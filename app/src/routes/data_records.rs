use actix_web::{get, web, Responder, HttpResponse};
use sqlx::PgPool;
use crate::db::DataRecords;
use crate::schema::QueryData;


#[get("/data")]
async fn data(db_pool: web::Data<PgPool>) -> impl Responder {
    println!{"Get /data"};
    let result = DataRecords::all_data_ids(db_pool.get_ref()).await;
    match result {
        Ok(data_ids) => HttpResponse::Ok().json(data_ids),
        _ => HttpResponse::BadRequest().body("Error")
    }
}


#[get("/data/query")]
async fn query_data(selector: web::Query<QueryData>, db_pool: web::Data<PgPool>) -> impl Responder {
    println!("Get /data/query {}", selector.clone());
    let result = DataRecords::filter_data_ids(selector.clone(), db_pool.get_ref()).await;
    match result {
        Ok(data_ids) => HttpResponse::Ok().json(data_ids),
        _ => HttpResponse::BadRequest().body("Error")
    }
}


#[get("/meta")]
async fn meta(db_pool: web::Data<PgPool>) -> impl Responder {
    println!{"Get /meta"};
    let result = DataRecords::index_metas(db_pool.get_ref()).await;
    match result {
        Ok(data_metas) => HttpResponse::Ok().json(data_metas),
        _ => HttpResponse::BadRequest().body("Error")
    }
}


#[get("/meta/{data_id}")]
async fn get_one_meta(data_id: web::Path<String>, db_pool: web::Data<PgPool>) -> impl Responder {
    println!("Get /meta/{}", data_id.clone());
    let result = DataRecords::one_meta(data_id.into_inner(), db_pool.get_ref()).await;
    match result {
        Ok(datameta) => HttpResponse::Ok().json(datameta),
        _ => HttpResponse::BadRequest().body("Error")
    }
}

pub fn init(cfg: &mut web::ServiceConfig) {
    cfg.service(data);
    cfg.service(query_data);
    cfg.service(meta);
    cfg.service(get_one_meta);
}