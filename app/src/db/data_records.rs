use crate::schema::QueryData;
use anyhow::Result;
use serde::{Deserialize, Serialize};
use sqlx::{FromRow, PgPool, Row};
use std::fmt::Debug;

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct IndexMeta {
    data_id: String,
    technology: String,
    species: String,
    disease: String,
    disease_subtype: String,
    molecular: String,
    source_url: Vec<String>,
    journal: String,
    year: i32,
    resolution: i32,
    cell_count: i32,
    has_cell_type: bool,
    level_name: Vec<String>,
    level_count: Vec<i32>,
}

#[derive(Serialize, FromRow, Debug)]
pub struct DataRecords {
    data_id: String,
    technology: String,
    species: String,
    tissue: String,
    disease: String,
    disease_subtype: String,
    molecular: String,
    source_name: String,
    source_url: Vec<String>,
    journal: String,
    year: i32,
    resolution: i32,
    cell_count: i32,
    markers: Vec<String>,
    has_cell_type: bool,
    level_name: Vec<String>,
    level_count: Vec<i32>,
}

impl DataRecords {
    pub async fn all_data_ids(pool: &PgPool) -> Result<Vec<String>> {
        let mut data_ids: Vec<String> = vec![];
        let recs = sqlx::query(
            r#"
            SELECT data_id FROM data_records;
        "#,
        )
        .fetch_all(pool)
        .await?;

        for rec in recs {
            data_ids.push(rec.get(0));
        }

        Ok(data_ids)
    }

    pub async fn all_metas(pool: &PgPool) -> Result<Vec<DataRecords>> {
        //let mut metas: Vec<DataRecords> = vec![];
        let metas: Vec<DataRecords> = sqlx::query_as(
            r#"
            SELECT * FROM data_records;
        "#,
        )
        .fetch_all(pool)
        .await?;

        Ok(metas)
    }

    pub async fn index_metas(pool: &PgPool) -> Result<Vec<IndexMeta>> {
        //let mut metas: Vec<DataRecords> = vec![];
        let metas: Vec<IndexMeta> = sqlx::query_as(
            r#"
            SELECT * FROM data_records;
        "#,
        )
        .fetch_all(pool)
        .await?;

        Ok(metas)
    }

    pub async fn one_meta(data_id: String, pool: &PgPool) -> Result<DataRecords> {
        let meta: DataRecords = sqlx::query_as(
            r#"
            SELECT * FROM data_records WHERE data_id = $1;
            "#,
        )
        .bind(data_id)
        .fetch_one(pool)
        .await?;

        Ok(meta)
    }

    pub async fn filter_data_ids(query: QueryData, pool: &PgPool) -> Result<Vec<String>> {
        let mut data_ids: Vec<String> = vec![];
        let recs = sqlx::query(query.to_sql().as_str()).fetch_all(pool).await?;

        for rec in recs {
            data_ids.push(rec.get(0));
        }

        Ok(data_ids)
    }
}
