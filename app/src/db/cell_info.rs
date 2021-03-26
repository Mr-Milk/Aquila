use std::fmt::Debug;

use anyhow::Result;
use serde::{Deserialize, Serialize};
use sqlx::{FromRow, PgPool, Row, Type, Postgres};
use serde_json::{Map, Value};
use std::collections::HashMap;


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
    matrix: HashMap<String, Vec<f64>>,
}

impl CellInfo {
    pub async fn get_cell_info(roi_id: String, pool: &PgPool) -> Result<CellInfo> {

        let info = sqlx::query(
            r#"
            SELECT * FROM cell_info WHERE roi_id = $1;
            "#,
        )
            .bind(roi_id.clone())
            .fetch_one(pool)
            .await?;

        let exp = sqlx::query(
            r#"
            SELECT * FROM cell_exp WHERE roi_id = $1;
            "#,
        ).bind(roi_id)
            .fetch_all(pool)
            .await?;

        let markers: Vec<String> = info.get(8);
        let mut matrix: HashMap<String, Vec<f64>> = markers
            .iter()
            .enumerate()
            .map(|(i, x)| {
                (x.into(), exp[i].get(3))
            }).collect();

        let cell_info = CellInfo {
            roi_id: info.get(0),
            data_id: info.get(1),
            cell_x: info.get(2),
            cell_y: info.get(3),
            cell_type: info.get(4),
            cell_name: info.get(5),
            neighbor_one: info.get(6),
            neighbor_two: info.get(7),
            markers,
            matrix
        };

        Ok(cell_info)
    }

}