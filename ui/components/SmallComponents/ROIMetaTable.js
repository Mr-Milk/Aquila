import MUIDataTable from "mui-datatables";
import { roiMeta } from "../../data/api";
import { Button, Card } from "@material-ui/core";
import LinkIcon from "@material-ui/icons/Link";
import React from "react";

export default function ROIMetaTable(props) {
  const { tableData, update, ...leftProps } = props;

  function handleClick(roi_id) {
    update(roi_id);
  }

  const header = tableData[0]["header"].slice(1);
  const construct_columns = [];
  header.map((h) => {
    construct_columns.push({
      name: h,
      label: h.replace(/^\w/, (c) => c.toUpperCase()),
    });
  });
  const columns = [
    {
      name: "roi_id",
      label: "View ROI",
      options: {
        filter: false,
        customBodyRender: (value) => {
          return (
            <Button
              color="primary"
              variant="outlined"
              onClick={() => {
                handleClick(value);
              }}
            >
              View
            </Button>
          );
        },
      },
    },
    ...construct_columns,
  ];

  const data = [];
  tableData.map((d) => {
    data.push(d["meta"]);
  });

  const options = {
    selectableRowsHideCheckboxes: true,
    viewColumns: false,
    print: false,
    hint: "Hi",
    download: false,
    rowsPerPage: 5,
    rowsPerPageOptions: [5],
    responsive: "standard",
  };
  return (
    <MUIDataTable
      title="ROI Table"
      data={data}
      columns={columns}
      options={options}
      {...leftProps}
    />
  );
}
