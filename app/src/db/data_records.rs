use anyhow::Result;
use serde::{Deserialize, Serialize};
use sqlx::{FromRow, PgPool, Row};

use crate::schema::QueryData;

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct DataRecords {
    data_id: String,
    technology: String,
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
    marker_count: i32,
    has_cell_type: bool,
}

impl DataRecords {
    pub async fn dbstats(pool: &PgPool) -> Result<DBStats> {
        let data = sqlx::query!(
            r#"
            SELECT COUNT(data_id) as "count!" FROM data_records;
            "#
        ).fetch_one(pool).await?;
        let tissue = sqlx::query!(
            r#"
            SELECT COUNT(DISTINCT tissue) as "count!" FROM data_records;
            "#
        ).fetch_one(pool).await?;
        let disease = sqlx::query!(
            r#"
            SELECT COUNT(DISTINCT disease) as "count!" FROM data_records;
            "#
        ).fetch_one(pool).await?;

        let stats = DBStats{
            data_count: data.count,
            tissue_count: tissue.count,
            disease_count: disease.count,
        };

        Ok(stats)
    }

    pub async fn all_data_ids(pool: &PgPool) -> Result<Vec<String>> {
        let mut data_ids: Vec<String> = vec![];
        let recs = sqlx::query!(
            r#"
            SELECT data_id FROM data_records;
        "#,
        )
        .fetch_all(pool)
        .await?;

        for rec in recs {
            data_ids.push(rec.data_id);
        }

        Ok(data_ids)
    }

    pub async fn all_records(pool: &PgPool) -> Result<Vec<DataRecords>> {
        let records: Vec<DataRecords> = sqlx::query_as(
            r#"
            SELECT * FROM data_records;
        "#,
        )
        .fetch_all(pool)
        .await?;

        Ok(records)
    }

    pub async fn one_record(data_id: String, pool: &PgPool) -> Result<DataRecords> {
        let record: DataRecords = sqlx::query_as(
            r#"
            SELECT * FROM data_records WHERE data_id = $1;
            "#,
        )
        .bind(data_id)
        .fetch_one(pool)
        .await?;

        Ok(record)
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

#[derive(Serialize, Deserialize, FromRow, Debug)]
pub struct DBStats {
    data_count: i64,
    tissue_count: i64,
    disease_count: i64,
}

// impl Display for DBStats {
//     fn fmt(&self, f: &mut Formatter<'_>) -> fResult {
//         write!(f, "data {}, tissue {}, disease {}", self.data_count, self.tissue_count, self.disease_count)
//     }
// }
