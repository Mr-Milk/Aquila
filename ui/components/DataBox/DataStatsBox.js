import {dataRecord, dataStats} from "../../data/api";
import {makeStyles} from "@material-ui/core/styles";
import Skeleton from "@material-ui/lab/Skeleton";

import CellComponentsPie from "../Visualization/CellComponentsPie";
import CellDensityBoxPlot from "../Visualization/CellDensityBoxPlot";
import CellInteractionMap from "../Visualization/CellInteractionMap";
import MarkerCoExpMap from "../Visualization/MarkerCoExpMap";
import Typography from "@material-ui/core/Typography";

const useStyles = makeStyles((theme) => ({
    root: {
        margin: theme.spacing(2),
        display: "flex",
        flexWrap: "wrap",
        justifyContent: "center",
    },
    pie: {
        marginRight: theme.spacing(2),
    },
    graph: {
        marginTop: theme.spacing(2),
    },
}));

export default function DataStatsBox(props) {
    const {data} = dataStats(props.dataID);
    const {data: recordData} = dataRecord(props.dataID);
    const classes = useStyles();

    if (data !== undefined) {
        const has_cell_type = recordData["has_cell_type"];

        if (has_cell_type) {
            return (
                <div className={classes.root}>
                    <CellComponentsPie
                        data={data["cell_components"]}
                        className={classes.pie}
                    />
                    <CellDensityBoxPlot data={data["cell_density"]}/>
                    <CellInteractionMap
                        data={data["cell_interaction"]}
                        className={classes.graph}
                    />
                    {/*<MarkerCoExpMap*/}
                    {/*    data={data["co_expression"]}*/}
                    {/*    className={classes.graph}*/}
                    {/*/>*/}
                </div>
            );
        } else {
            return (
                <Typography color={"textSecondary"}>No available statistic results due to lack of cell type in this dataset</Typography>
                // <div className={classes.root}>
                //     <MarkerCoExpMap
                //         data={data["co_expression"]}
                //         className={classes.graph}
                //     />
                // </div>
            );
        }
    } else {
        return (
            <Skeleton height={"400px"}/>
        );
    }
}
