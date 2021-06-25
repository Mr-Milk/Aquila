import React, {useState} from "react";
import {cellInfo} from "../../data/api";
import Skeleton from "@material-ui/lab/Skeleton";
import {FormControlLabel, Switch, withStyles} from "@material-ui/core";
import {makeStyles} from "@material-ui/core/styles";
import ROICellMap from "./ROICellMap";

const useStyles = makeStyles((theme) => ({
    root: {
        display: "inline-block",
        textAlign: "center",
    },
    toggle: {
        marginTop: theme.spacing(2),
        marginBottom: theme.spacing(2),
    },
}));

const NeighborSwitch = withStyles({
    switchBase: {
        "&$checked": {
            color: "#26a69a",
        },
        "&$checked + $track": {
            backgroundColor: "#26a69a",
        },
    },
    checked: {},
    track: {},
})(Switch);

export default function ROICellMapWithSwitch(props) {
    const {roiID, ...leftProps} = props;
    const classes = useStyles();
    const [showNeighbors, setShowNeighbors] = useState(false);

    const {data: cellInfoData, isLoading, isError} = cellInfo(roiID);

    if (isLoading || isError) {
        return <Skeleton height={"550px"} width={"1000px"}/>;
    }

    return (
        <div className={classes.root}>
            <FormControlLabel
                className={classes.toggle}
                control={
                    <NeighborSwitch
                        checked={showNeighbors}
                        onChange={(event) => {
                            setShowNeighbors(event.target.checked);
                        }}
                    />
                }
                label="Show Neighbors"
                style={{}}
            />
            <ROICellMap
                showNeighbors={showNeighbors}
                cellInfoData={cellInfoData}
                {...leftProps}
            />
        </div>
    );
}
