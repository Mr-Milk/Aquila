use actix_web::HttpResponse;
use serde::{Deserialize, Serialize};

pub fn json_response<'a, T: Deserialize<'a> + Serialize>(content: T) -> HttpResponse {
    HttpResponse::Ok().json(content)
}

pub fn error_response() -> HttpResponse {
    HttpResponse::BadRequest().body("Error")
}