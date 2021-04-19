import Skeleton from "@material-ui/lab/Skeleton";
import React, { useState } from "react";
import { roiMeta } from "../../data/api";
import { makeStyles } from "@material-ui/core/styles";
import ROIMetaTable from "../SmallComponents/ROIMetaTable";

import ROICard from "../SmallComponents/ROICard";
import ROICellMapWithSwitch from "../Visualization/ROICellMapWithSwitch";
import ROIMarkerMapWithSelector from "../Visualization/ROIMarkerMapWithSelector";

const useStyles = makeStyles((theme) => ({
  root: {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "center",
  },
  tb: {
    width: "500px",
    marginRight: theme.spacing(2),
    marginBottom: theme.spacing(2),
  },
  cardContainer: {
    display: "flex",
    justifyContent: "center",
    paddingBottom: theme.spacing(2),
  },
  card: {
    textAlign: "center",
    minWidth: 250,
  },
  mapContainer: {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "center",
  },
}));

export default function ROIBox(props) {
  const classes = useStyles();
  const { data: MetaTable, isLoading, isError } = roiMeta(props.dataID);
  const [roiID, setRoiId] = useState("");

  function updateRoiId(roi_id) {
    setRoiId(roi_id);
  }

  if (isLoading || isError) {
    return <Skeleton height={"550px"} width={"1000px"} />;
  }

  if (roiID === "") {
    const default_roiID = MetaTable[0]["roi_id"];
    setRoiId(default_roiID);
  }

  return (
    <>
      <div className={classes.root}>
        <ROIMetaTable
          tableData={MetaTable}
          update={updateRoiId}
          className={classes.tb}
        />
        <div className={classes.cardContainer}>
          <ROICard
            MetaTable={MetaTable}
            roiID={roiID}
            className={classes.card}
          />
        </div>
        <div className={classes.mapContainer}>
          <ROICellMapWithSwitch roiID={roiID} />
          <ROIMarkerMapWithSelector roiID={roiID} />
        </div>
      </div>
    </>
  );
}
