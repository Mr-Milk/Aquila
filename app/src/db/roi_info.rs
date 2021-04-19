use std::fmt::Debug;

use anyhow::Result;
use serde::{Deserialize, Serialize};
use sqlx::{FromRow, PgPool};


#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct ROIInfo {
    roi_id: String,
    data_id: String,
    header: Vec<String>,
    meta: Vec<String>,
    shannon_entropy: f64,
    altieri_entropy: f64,
}

impl ROIInfo {
    pub async fn roi_info(data_id: String, pool: &PgPool) -> Result<Vec<ROIInfo>> {
        let rois: Vec<ROIInfo> = sqlx::query_as(
            r#"
            SELECT * FROM roi_info WHERE data_id = $1;
            "#,
        )
        .bind(data_id)
        .fetch_all(pool)
        .await?;

        Ok(rois)
    }
}
