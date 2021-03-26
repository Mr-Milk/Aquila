import { Paper } from "@material-ui/core";
import { dataRecord, dataStats } from "../../data/api";
import EChartsReact from "echarts-for-react";
import { makeStyles } from "@material-ui/core/styles";
import Skeleton from "@material-ui/lab/Skeleton";

import CellComponentsPie from "../Visualization/CellComponentsPie";
import CellDensityBoxPlot from "../Visualization/CellDensityBoxPlot";
import CellInteractionMap from "../Visualization/CellInteractionMap";

const useStyles = makeStyles((theme) => ({
  root: {
    margin: theme.spacing(2),
    display: "flex",
    flexWrap: "wrap",
    alignItems: "middle",
  },
  pie: {
    marginRight: theme.spacing(2),
  },
}));

export default function DataStatsBox(props) {
  const { data } = dataStats(props.dataID);
  const { data: recordData } = dataRecord(props.dataID);
  const classes = useStyles();

  if (data !== undefined) {
    const has_cell_type = recordData["has_cell_type"];

    return (
      <>
        <div className={classes.root}>
          <CellComponentsPie
            data={data["cell_components"]}
            className={classes.pie}
          />
          <CellDensityBoxPlot data={data["cell_density"]} />
          <CellInteractionMap data={data["cell_interaction"]} />
        </div>
      </>
    );
  } else {
    return (
      <>
        <Skeleton width={"400px"} />
      </>
    );
  }
}
