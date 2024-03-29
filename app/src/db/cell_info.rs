use std::fmt::Debug;

use anyhow::Result;
use serde::{Deserialize, Serialize};
use sqlx::{FromRow, PgPool};


#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct CellInfo {
    roi_id: String,
    data_id: String,
    cell_x: Vec<f64>,
    cell_y: Vec<f64>,
    cell_type: Vec<String>,
    cell_name: Vec<i32>,
    neighbor_one: Vec<i32>,
    neighbor_two: Vec<i32>,
    markers: Vec<String>,
}

impl CellInfo {
    pub async fn get_cell_info(roi_id: String, pool: &PgPool) -> Result<CellInfo> {

        let info: CellInfo = sqlx::query_as(
            r#"
            SELECT * FROM cell_info WHERE roi_id = $1;
            "#,
        )
            .bind(roi_id.clone())
            .fetch_one(pool)
            .await?;

        Ok(info)
    }

}


#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct CellExp {
    roi_id: String,
    data_id: String,
    marker: String,
    expression: Vec<f64>,
}

impl CellExp {
    pub async fn get_roi_exp(roi_id: String, marker: String, pool: &PgPool) -> Result<CellExp> {
        println!("before query");
        let exp: CellExp = sqlx::query_as(
            r#"
            SELECT * FROM cell_exp WHERE
            roi_id = $1 AND marker = $2;
            "#
        )
            .bind(roi_id)
            .bind(marker)
            .fetch_one(pool)
            .await?;

        Ok(exp)
    }
}