import React from "react";
import MUIDataTable from "mui-datatables";
import Skeleton from "@material-ui/lab/Skeleton";
import Link from "next/link";
import Visibility from "@material-ui/icons/Visibility";
import GetApp from "@material-ui/icons/GetApp";
import LinkIcon from "@material-ui/icons/Link";
import {useRouter} from "next/router";

import {records} from "../data/api";
import {Alert} from "@material-ui/lab";
import {IconButton, Snackbar} from "@material-ui/core";
import {createMuiTheme} from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";

export default function RecordsTable() {
    const router = useRouter();

    const {data, isLoading, isError} = records();
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
        return <Skeleton variant="rect" width={"gl"} height={1000}/>;
    }

    if (isError) {
        return (
            <>
                <Snackbar
                    open={open}
                    onClose={handleClose}
                    anchorOrigin={{vertical: "top", horizontal: "right"}}
                >
                    <Alert severity="error" onClose={handleClose}>
                        Please check your connection
                    </Alert>
                </Snackbar>
                <Skeleton variant="rect" width={"gl"} height={1000}/>
            </>
        );
    }

    data.map((d) => {
        d.download = `/static/${d.data_id}`;
    });

    const columns = [
                {
            name: "data_id",
            label: "View",
            options: {
                filter: false,
                customBodyRender: (value) => {
                    return (
                        <Button
                            variant="outlined"
                            size="small"
                            color="primary"
                            href={`/data/${value}`}
                            target="_blank"
                            rel="noreferrer noopener"
                            // onClick={() => router.push(`/data/${value}`)}
                        >
                            View
                        </Button>
                    );
                },
            },
        },
        {
            name: "species",
            label: "Species",
        },
        {
            name: "molecule",
            label: "Molecule",
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
            options: {
                filter: false,
            },
        },
        {
            name: "resolution",
            label: "Resolution(nm)",
            options: {
                filter: false,
                customBodyRender: (value) => {
                    if (value === -1) {
                        return "Single cell"
                    } else {
                        return value
                    }
                },
            },
        },
        {
            name: "cell_count",
            label: "Cell",
            options: {
                filter: false,
            },
        },
        {
            name: "marker_count",
            label: "Marker",
            options: {
                filter: false,
            },
        },
        {
            name: "source_url",
            label: "Link",
            options: {
                sort: false,
                filter: false,
                customBodyRender: (value) => {
                    return (
                        <IconButton
                            color="primary"
                            href={value}
                            target="_blank"
                            rel="noreferrer noopener"
                        >
                            <LinkIcon/>
                        </IconButton>
                    );
                },
            },
        },
        {
            name: "data_id",
            label: "Download",
            options: {
                sort: false,
                filter: false,
                customBodyRender: (value) => {
                    return (
                        <IconButton
                            color="primary"
                            href={`/static/${value}.zip`}
                            rel="noreferrer noopener"
                            download
                        >
                            <GetApp/>
                        </IconButton>
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
        responsive: "standard",
        tableBodyHeight: "50%",
        sortOrder: {
                    name: 'year',
                    direction: 'desc',
                },
    };

    return (
        <MUIDataTable
            title="Data Portal"
            data={data}
            columns={columns}
            options={options}
        />
    );
}
