use std::fmt::Debug;

use anyhow::Result;
use serde::{Deserialize, Serialize};
use sqlx::{FromRow, PgPool, Row};
use serde_json::{from_str, Map, Value};

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct DataStats {
    data_id: String,
    cell_components: String,
    cell_density: String,
    co_expression: String,
    cell_interaction: String,
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
            co_expression: from_str(&*stats.co_expression).unwrap(),
            cell_interaction: from_str(&*stats.cell_interaction).unwrap(),
        };

        Ok(response)
    }
}

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct DataStatsResponse {
    data_id: String,
    cell_components: Map<String, Value>,
    cell_density: Map<String, Value>,
    co_expression: Map<String, Value>,
    cell_interaction: Map<String, Value>,
}