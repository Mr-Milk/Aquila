# API Document of Baize

```
root: api.baize.com

GET /data
get all the data_id

['id1', 'id2', ...]

GET /meta/{data_id}
get the meta of a data

DataMeta:
{}

GET /stats/{type}/{data_id}
get stats of a data

json

GET /roi/{data_id}
get all roi_id and their levels of data

GET /cell_info/{roi_id}
get cell info

GET /cell_exp/{roi_id}
get cell exp

GET /data/query/?{}
return a list of data_id

GET /download/{data_id}
download a .zip file of a data
```





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

