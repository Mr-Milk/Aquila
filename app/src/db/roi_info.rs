struct CellInfo {
    data_id: String,
    roi_id: String,
    cells: Vec<OneCell>
}

struct OneCell {
    cell_id: String,
    cell_x: f32,
    cell_y: f32,
    cell_type: String,
    cell_exp: Vec<f32>,
}

struct ROIInfo {
    roi_id: String,
    data_id: String,
    levels_table: String,
}