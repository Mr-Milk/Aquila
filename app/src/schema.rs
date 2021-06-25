use std::fmt::{Debug, Display, Result};

use serde::Deserialize;

fn construct_in_query(field: &str, item: Option<String>, as_type: &str) -> String {
    let sql = match item {
        Some(x) => {
            let ele: Vec<String> = x
                .split(",")
                .map(|e| {
                    if as_type == "str" {
                        format!("'{}'", e)
                    } else {
                        format!("{}", e)
                    }
                })
                .collect();

            if ele.len() == 1 {
                format!("{} = {}", &field, ele[0])
            } else {
                format!("{} IN ({})", &field, ele.join(", "))
            }
        }
        None => "".to_string(),
    };

    sql
}

fn construct_range_query(field: &str, item: Option<String>) -> String {
    let sql = match item {
        Some(x) => {
            let ele: Vec<i32> = x.split(",").map(|e| e.parse().unwrap()).collect();

            if ele.len() == 1 {
                format!("{} = {}", &field, ele[0])
            } else {
                let a = ele[0];
                let b = ele[1];
                if a > b {
                    format!("{} BETWEEN {} AND {}", &field, b, a)
                } else {
                    format!("{} BETWEEN {} AND {}", &field, a, b)
                }
            }
        }
        None => "".to_string(),
    };

    sql
}

#[derive(Deserialize, Clone, Debug)]
pub struct QueryData {
    pub(crate) technology: Option<String>,
    pub(crate) tissue: Option<String>,
    pub(crate) disease: Option<String>,
    pub(crate) sub_disease: Option<String>,
    pub(crate) molecular: Option<String>,
    pub(crate) year: Option<String>,
    pub(crate) resolution: Option<String>,
    pub(crate) cell_count: Option<String>,
    pub(crate) marker_count: Option<String>,
    pub(crate) year_range: Option<String>,
    pub(crate) resolution_range: Option<String>,
    pub(crate) cell_count_range: Option<String>,
    pub(crate) marker_count_range: Option<String>,
    pub(crate) has_cell_type: Option<bool>,
}

impl QueryData {
    pub(crate) fn to_sql(&self) -> String {
        let conditions = vec![
            construct_in_query("technology", self.technology.clone(), "str"),
            construct_in_query("tissue", self.tissue.clone(), "str"),
            construct_in_query("disease", self.disease.clone(), "str"),
            construct_in_query("sub_disease", self.sub_disease.clone(), "str"),
            construct_in_query("molecular", self.molecular.clone(), "str"),
            construct_in_query("year", self.year.clone(), "int"),
            construct_in_query("resolution", self.resolution.clone(), "int"),
            construct_in_query("cell_count", self.cell_count.clone(), "int"),
            construct_in_query("marker_count", self.marker_count.clone(), "int"),
            construct_range_query("year", self.year_range.clone()),
            construct_range_query("resolution", self.resolution_range.clone()),
            construct_range_query("cell_count", self.cell_count_range.clone()),
            construct_range_query("marker_count", self.marker_count_range.clone()),
            {
                match self.has_cell_type {
                    Some(x) => {
                        let v = if x {
                            "true".to_string()
                        } else {
                            "false".to_string()
                        };
                        format!("has_cell_type = {}", v)
                    }
                    None => ("".to_string()),
                }
            },
        ];

        let mut query_params = vec![];
        for c in conditions {
            if c != "" {
                query_params.push(c)
            }
        }

        format!(
            "SELECT data_id FROM data_records WHERE {};",
            query_params.join(" AND ")
        )
    }
}

// impl Display for QueryData {
//     fn fmt<W>(&self, f: &mut dyn Formatter) -> Result {
//         write!(f, "{}", self.to_sql())
//     }
// }
