use std::fmt::Debug;

use anyhow::Result;
use serde::{Deserialize, Serialize};
use sqlx::{FromRow, PgPool, Row, Type, Postgres};


#[derive(Serialize, Deserialize, Debug, sqlx::Type)]
#[sqlx(transparent)]
struct VecF64(Vec<Vec<f64>>);

#[derive(Serialize, Deserialize, Debug, sqlx::Type)]
#[sqlx(transparent)]
struct VecI32(Vec<Vec<i32>>);


#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct CellInfo {
    roi_id: String,
    data_id: String,
    cell_x: Vec<f64>,
    cell_y: Vec<f64>,
    cell_type: Vec<String>,
    markers: Vec<String>,
    expression: Vec<f64>,
    cell_name: Vec<i32>,
    neighbors: Vec<i32>,
}

impl CellInfo {
    pub async fn get_cell_info(roi_id: String, pool: &PgPool) -> Result<CellInfo> {

        let info: CellInfo = sqlx::query_as(
            r#"
            SELECT * FROM cell_info WHERE roi_id = $1;
            "#,
        )
            .bind(roi_id)
            .fetch_one(pool)
            .await?;

        Ok(info)
    }

}