use crate::schema::QueryData;
use anyhow::{Error, Result};
use serde::{Deserialize, Serialize};
use serde_json::{from_str, Map, Value};
use sqlx::{FromRow, PgPool, Postgres, Row};
use std::fmt::Debug;

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct DataStats {
    data_id: String,
    cell_components: String,
    cell_density: String,
    spatial_distribution: String,
    entropy_shannon: String,
    entropy_altieri: String,
}

impl DataStats {
    pub async fn all_stats(data_id: String, pool: &PgPool) -> Result<DataStatsResponse> {
        let stats: DataStats = sqlx::query_as(
            r#"
            SELECT * FROM data_stats WHERE data_id = $1;
            "#,
        )
        .bind(data_id)
        .fetch_one(pool)
        .await?;

        let response = DataStatsResponse {
            data_id: stats.data_id,
            cell_components: from_str(&*stats.cell_components).unwrap(),
            cell_density: from_str(&*stats.cell_density).unwrap(),
            spatial_distribution: from_str(&*stats.spatial_distribution).unwrap(),
            entropy_shannon: from_str(&*stats.entropy_shannon).unwrap(),
            entropy_altieri: from_str(&*stats.entropy_altieri).unwrap(),
        };

        Ok(response)
    }
}

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct DataStatsResponse {
    data_id: String,
    cell_components: Vec<Map<String, Value>>,
    cell_density: Vec<Map<String, Value>>,
    spatial_distribution: Vec<Map<String, Value>>,
    entropy_shannon: Vec<Map<String, Value>>,
    entropy_altieri: Vec<Map<String, Value>>,
}
