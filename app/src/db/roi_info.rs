use crate::schema::QueryData;
use anyhow::{Error, Result};
use serde::{Deserialize, Serialize};
use serde_json::{from_str, Map, Value};
use sqlx::{FromRow, PgPool, Row};
use std::fmt::Debug;

#[derive(Serialize, Deserialize, Debug)]
pub struct CellInfo {
    data_id: String,
    roi_id: String,
    cells: Vec<OneCell>,
}

impl CellInfo {
    pub async fn get_cell_info(roi_id: String, pool: &PgPool) -> Result<CellInfo> {
        println!("call get cell info!");

        let info: Vec<OneCell> = sqlx::query_as(
            r#"
            SELECT cell_id, cell_x, cell_y, cell_type, expression FROM cell_info WHERE roi_id = $1;
            "#,
        )
        .bind(roi_id.clone())
        .fetch_all(pool)
        .await?;

        println!("fetch cell info success!");

        let rec = sqlx::query(
            r#"
            SELECT data_id, roi_id FROM group_level WHERE roi_id = $1;
            "#,
        )
        .bind(roi_id.clone())
        .fetch_one(pool)
        .await?;

        println!("fetch data id success!");

        Ok(CellInfo {
            data_id: rec.get(0),
            roi_id: rec.get(1),
            cells: info,
        })
    }
}

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct OneCell {
    cell_id: String,
    cell_x: f64,
    cell_y: f64,
    cell_type: String,
    expression: Vec<f64>,
}

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct ROIInfo {
    roi_id: String,
    data_id: String,
    levels_table: String,
}

impl ROIInfo {
    pub async fn get_roi_info(data_id: String, pool: &PgPool) -> Result<Vec<ROIInfoResponse>> {
        println!("call get_roi_info");
        let rois: Vec<ROIInfo> = sqlx::query_as(
            r#"
            SELECT * FROM group_level WHERE data_id = $1;
            "#,
        )
        .bind(data_id)
        .fetch_all(pool)
        .await?;
        println!("fetch success!");

        let mut response: Vec<ROIInfoResponse> = vec![];

        for roi in rois {
            response.push(ROIInfoResponse {
                roi_id: roi.roi_id,
                data_id: roi.data_id,
                levels_table: from_str(&*roi.levels_table).unwrap(),
            })
        }
        Ok(response)
    }
}

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct ROIInfoResponse {
    roi_id: String,
    data_id: String,
    levels_table: Vec<Map<String, Value>>,
}
