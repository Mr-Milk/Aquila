# API Document of Baize

**API Root**: [api.baize.cheunglab.org]()


**GET** ```/download/{data_id}```: Download a .zip file of a data

**GET** ```/dbstats```: Get statistic of database
```rust
struct DBStats {
    data_count: i64,
    tissue_count: i64,
    disease_count: i64,
}
```
Example: ```{"data_count": 10, "disease_count": 22, "tissue_count": 12}```


**GET** ```/data_ids```: Get all the data_id
```rust
Vec<String>
```
Example: ```["id 1", "id 2", ..., "id n"]```


**GET** ```/records/{data_id}```: Get one data
```rust
struct DataRecords {
    data_id: String,
    technology: String,
    species: String,
    tissue: String,
    disease: String,
    disease_subtype: String,
    molecule: String,
    source_name: String,
    source_url: String,
    journal: String,
    year: i32,
    resolution: i32,
    cell_count: i32,
    marker_count: i32,
    has_cell_type: bool,
    notice: Option<String>,
}
```
Example: 
```json
{"data_id":"c57c6719f73e64307f7f58a2c635534a-lung",
"technology":"CyCIF",
"species":"Human",
"tissue":"Lung",
"disease":"Cancer",
"disease_subtype":"Lung cancer",
"molecule":"Protein",
"source_name":"Qualifying antibodies for image-based immune profiling and multiplexed tissue imaging",
"source_url":"http://dx.doi.org/10.1038/s41596-019-0206-y",
"journal":"Nature Protocols",
"year":2019,
"resolution":200,
"cell_count":166811,
"marker_count":26,
"has_cell_type":false,
"notice":null}
```

**GET** ```/records```: Get all records
```rust
Vec<DataRecords>
```


**GET** ```/stats/{data_id}```: Get analysis result of a specific data
```rust
struct DataStats {
    data_id: String,
    cell_components: String,
    cell_density: String,
    co_expression: String,
    cell_interaction: String,
}
```
The tabular data stored in the json format.


**GET** ```/roi/{data_id}```: Get all roi_id and their levels of data in a data
```rust
struct ROIInfo {
    roi_id: String,
    data_id: String,
    header: Vec<String>,
    meta: Vec<String>,
    shannon_entropy: f64,
    spatial_entropy: f64,
}
```

**GET** ```/cell_info/{roi_id}```
```rust
struct CellInfo {
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
```

**GET** ```/cell_exp/{roi_id}/{marker}```
```rust
struct CellExp {
    roi_id: String,
    data_id: String,
    marker: String,
    expression: Vec<f64>,
}
```

