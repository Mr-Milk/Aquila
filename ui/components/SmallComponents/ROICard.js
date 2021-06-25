import React from "react";
import {Card} from "@material-ui/core";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import {round} from "mathjs";

export default function ROICard(props) {
    const {MetaTable, roiID, ...leftProps} = props;

    const infoMapper = {};
    MetaTable.map((roi) => {
        infoMapper[roi["roi_id"]] = roi;
    });

    let currentROI = [];
    infoMapper[roiID]["meta"].slice(1).map((m, i) => {
        let head = infoMapper[roiID]["header"].slice(1)[i];
        currentROI.push(`${head}: ${m}`)
    })

    const currentROI_name = currentROI.join("\n")

    return (
        <Card variant="outlined" {...leftProps}>
            <CardContent>
                <Typography variant="h6">
                    <strong>Current ROI:</strong>{" "}
                    {currentROI_name}
                </Typography>
                <Typography>
                    <strong>Shannon entropy:</strong>{" "}
                    {round(infoMapper[roiID]["shannon_entropy"], 3)}
                </Typography>
                <Typography>
                    <strong>Spatial entropy:</strong>{" "}
                    {round(infoMapper[roiID]["spatial_entropy"], 3)}
                </Typography>
            </CardContent>
        </Card>
    );
}
