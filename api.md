# API Document of Baize

**API Root**: [api.baize.cheunglab.org]()



**Get Database Statistic**

**GET** ```/dbstats```
Example: ```{"data_count": 10, "disease_count": 22, "tissue_count": 12}```



**Get all the data_id**

**GET** ```/data_ids```

Example: ```["id 1", "id 2", ..., "id n"]```



**Get the meta of a data**

**GET** ```/records```: Get all

**GET** ```/records/{data_id}```: Get one data

```javascript
{
    "data_id": String,
    "technology": String,
    "species": String,
    "disease": String,
    "disease_subtype": String,
    "molecular": String,
    "source_url": Vec<String>,
    "journal": String,
    "year": i32,
    "resolution": i32,
    "cell_count": i32,
    "marker_count": i32,
    "has_cell_type": bool,
}
```



**Get data statistics**

**GET** ```/stats/cell_components/{data_id}```

```javascript
{
  "data_id": string,
  "cell_types": ["type1", "type2", ..., "type n"],
  "fraction": [0.1, 0.35, ...]
}
```



**GET** ```/stats/cell_density/{data_id}```

```javascript
{
  "data_id": string,
	"cell_types": ["type1", "type2", ..., "type n"],
  "density": [
    [0.1, 0.2, ..., 0.6],
    [0.4, 2.3, ..., 8.5],
    ...
  ]
}
```



**GET** ```/stats/coexp/{data_id}```

```javascript
{
	"data_id": string,
	"markers": ["m1", "m2", ...],
	"relationship": [(source, target, value), ...],
	
}
```



**GET** ```/stats/cci/{data_id}```

```javascript
{
	"data_id": string,
	"cell_types": ["c1", "c2", ...],
	"relationship": [(source, target, value), ...]
}
```





**Get ROI information**

**GET** ```/roi/{data_id}```: Get all roi_id and their levels of data in a data

```javascript
{
  "data_id": string,
  "roi_ids": ["id 1", "id 2", ..., "id n"]，
  "shannon_entropy":
	"altieri_entropy":
  "header": ["roi_id", "patient", "stage", ],
  "meta": [
      [ "id 1", "patient 1", "stage 1",],
      ["patient 1", "stage 2", "id 2"],
      ["patient 1", "stage 3", "id 3"],
      ...
    ]
}
```



**GET** ```/cell_info/{roi_id}```

```javascript
{
	"data_id":
	"roi_id":
	"cell_name": [id1, id2, ]
	"cell_loc": [(x, y), ...],
	"cell_type": ["type 1", ...],
	"cell_exp": {
		"markers": [],
		"matrix": {
			marker: [matrix...],
		}
	}
	"cell_neighbors": [(source, target), ...]
}
```



GET /data/query/?{}
return a list of data_id

GET /download/{data_id}
download a .zip file of a data





# Database Tables

```sql
CREATE USER baize WITH PASSWORD 'baize';
CREATE DATABASE sscmap;
GRANT ALL PRIVILEGES ON DATABASE sscmap to baize;

CREATE DATABASE "sscmap";
GRANT ALL PRIVILEGES ON DATABASE "sscmap" to baize;
```



### query_options

- technology: ARRAY[VARCHAR]

- disease: ARRAY[VARCHAR]
- molecular: ARRAY[VARCHAR]
- marker: ARRAY[VARCHAR]
- disease_subtype: ARRAY[VARCHAR]



### data_records

- **data_id**: VARCHAR, PRIMARY KEY
- data_meta: JSON

```json
{"data_id": "101016jcell201808039-f6b993db", 
 "technology": ["mibi"], 
 "species": ["human"], 
 "tissue": ["breast"], 
 "disease": ["cancer"], 
 "molecular": ["protein"], 
 "source_name": ["A Structured Tumor-Immune Microenvironment in Triple Negative Breast Cancer Revealed by Multiplexed Ion Beam Imaging"], 
 "source_url": ["http://dx.doi.org/10.1016/j.cell.2018.08.039"], 
 "journal": ["Cell"], 
 "year": [2018], 
 "resolution": [1000], 
 "cell_count": 191316, 
 "marker_count": 39, 
 "markers": ["Vimentin", "SMA", "B7H3", "FoxP3", "Lag3", "CD4", "CD16", "CD56", "OX40", "PD1", "CD31", "PD-L1", "EGFR", "Ki67", "CD209", "CD11c", "CD138", "CD163", "CD68", "CSF-1R", "CD8", "CD3", "IDO", "Keratin17", "CD63", "CD45RO", "CD20", "p53", "Beta catenin", "HLA-DR", "CD11b", "CD45", "H3K9ac", "Pan-Keratin", "H3K27me3", "phospho-S6", "MPO", "Keratin6", "HLA_Class_1"], 
 "has_cell_type": true, 
 "level_name": ["Patient"], 
 "level_count": [40], 
 "disease_subtype": ["breast cancer"],
 }
```



### data_stats

- **data_id**: VARCHAR, PRIMARY KEY
- cell_components: JSON
- cell_density: JSON
- spatial_distribution: JSON
- entropy_shannon: JSON
- entropy_altieri: JSON



### cell_info

- **cell_id**: UUID, PRIMARY KEY
- cell_x: FLOAT
- cell_y: FLOAT
- cell_type: VARCHAR
- roi_id: UUID, INDEX
- data_id: VARCHAR, INDEX



### cell_expression

- **cell_id**: UUID, PRIMARY KEY
- expression: ARRAY[FLOAT]
- roi_id: UUID, INDEX
- data_id: UUID, INDEX



### group_level

- **data_id**: VARCHAR, PRIMARY KEY
- levels_table: JSON

```json
# A dataframe, store as JSON
{	"roi_id":[],
  "Patient":[],
  ""
}
```

