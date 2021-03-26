import React from "react";
import MUIDataTable from "mui-datatables";
import Skeleton from "@material-ui/lab/Skeleton";
import Link from "next/link";
import Launch from "@material-ui/icons/Launch";
import LinkIcon from "@material-ui/icons/Link";
import { useRouter } from "next/router";

import { records } from "../data/api";
import { Alert } from "@material-ui/lab";
import { IconButton, Snackbar } from "@material-ui/core";

export default function RecordsTable() {
  const router = useRouter();

  const { data, isLoading, isError } = records();
  let isError_ = isError;
  const [open, setOpen] = React.useState(true);

  const handleClose = (event, reason) => {
    if (reason === "clickaway") {
      return;
    }

    setOpen(false);
    isError_ = false;
  };

  if (isLoading) {
    return <Skeleton variant="rect" width={"gl"} height={1000} />;
  }

  if (isError) {
    return (
      <>
        <Snackbar
          open={open}
          onClose={handleClose}
          anchorOrigin={{ vertical: "top", horizontal: "right" }}
        >
          <Alert severity="error" onClose={handleClose}>
            Please check your connection
          </Alert>
        </Snackbar>
        <Skeleton variant="rect" width={"gl"} height={1000} />
      </>
    );
  }

  const columns = [
    {
      name: "molecular",
      label: "Molecular",
    },
    {
      name: "technology",
      label: "Technology",
    },
    {
      name: "tissue",
      label: "Tissue",
    },
    {
      name: "disease_subtype",
      label: "Disease",
    },
    {
      name: "journal",
      label: "Journal",
    },
    {
      name: "year",
      label: "Year",
    },
    {
      name: "resolution",
      label: "Resolution",
    },
    {
      name: "cell_count",
      label: "Cells",
    },
    {
      name: "marker_count",
      label: "Markers",
    },
    {
      name: "source_url",
      label: "Link",
      options: {
        customBodyRender: (value) => {
          return (
            <IconButton
              color="primary"
              href={value}
              target="_blank"
              rel="noreferrer noopener"
            >
              <LinkIcon />
            </IconButton>
          );
        },
      },
    },
    {
      name: "data_id",
      label: "View",
      options: {
        customBodyRender: (value) => {
          return (
            // <Link href={`/data/${value}`}>
            <IconButton
              color="primary"
              onClick={() => router.push(`/data/${value}`)}
            >
              <Launch />
            </IconButton>
            // </Link>
          );
        },
      },
    },
  ];

  const options = {
    selectableRowsHideCheckboxes: true,
    viewColumns: false,
    print: false,
    hint: "Hi",
    download: false,
  };

  return (
    <MUIDataTable
      title="Data"
      data={data}
      columns={columns}
      options={options}
    />
  );
}
