import {Autocomplete} from "@material-ui/lab";
import {TextField} from "@material-ui/core";
import {makeStyles} from "@material-ui/core/styles";
import {cellInfo} from "../../data/api";
import Skeleton from "@material-ui/lab/Skeleton";
import React, {useState} from "react";
import ROIMarkerMap from "./ROIMarkerMap";

const useStyles = makeStyles((theme) => ({
    root: {
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
    },
    selector: {
        width: "275px",
    },
}));

export default function ROIMarkerMapWithSelector(props) {
    const {roiID, ...leftProps} = props;
    const classes = useStyles();
    const [selectedMarker, setSelectedMarker] = useState("");
    const {data: cellInfoData, isLoading, isError} = cellInfo(roiID);

    if (isLoading || isError) {
        return <Skeleton height={"550px"} width={"1000px"}/>;
    }

    const markers = cellInfoData["markers"];

    if (selectedMarker === "") {
        setSelectedMarker(markers[0]);
    }

    return (
        <div className={classes.root}>
            <Autocomplete
                className={classes.selector}
                renderInput={(params) => (
                    <TextField {...params} label="Select marker" margin="normal"/>
                )}
                options={markers}
                value={selectedMarker}
                onChange={(event, marker) => {
                    setSelectedMarker(marker);
                }}
            />
            <ROIMarkerMap
                roiID={roiID}
                marker={selectedMarker}
                cellInfo={cellInfoData}
            />
        </div>
    );
}
