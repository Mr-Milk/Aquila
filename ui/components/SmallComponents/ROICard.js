import React from "react";
import {Card, List, ListItem, ListItemIcon, ListItemText} from "@material-ui/core";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import {round} from "mathjs";

export default function ROICard(props) {
    const {MetaTable, roiID, ...leftProps} = props;

    const infoMapper = {};
    MetaTable.map((roi) => {
        infoMapper[roi["roi_id"]] = roi;
    });

    let currentROI = {};
    infoMapper[roiID]["meta"].slice(1).map((m, i) => {
        let head = infoMapper[roiID]["header"].slice(1)[i];
        currentROI[head] = m
    })

    return (
        <Card variant="outlined" {...leftProps}>
            <CardContent>
                <div style={{"textAlign": "center", "textWeight": "bold"}}>
                    <Typography variant={"h6"}>Selected ROI</Typography>
                </div>
                <List>

                    {Object.entries(currentROI).map(([h, m]) => {
                        return <ListItem key={m}>
                            <ListItemIcon>
                                <Typography style={{"fontWeight": "bold"}}>{String(h).toUpperCase()}&nbsp;</Typography>
                            </ListItemIcon>
                            <ListItemText>
                                <Typography>{String(m)}</Typography>
                            </ListItemText>
                        </ListItem>

                    })}
                    <ListItem>
                        <ListItemIcon>
                            <Typography style={{"fontWeight": "bold"}}>SHANNON ENTROPY&nbsp;</Typography>
                        </ListItemIcon>
                        <ListItemText>
                            {round(infoMapper[roiID]["shannon_entropy"], 3)}
                        </ListItemText>
                    </ListItem>
                    <ListItem>
                        <ListItemIcon>
                            <Typography style={{"fontWeight": "bold"}}>SPATIAL ENTROPY&nbsp;</Typography>
                        </ListItemIcon>
                        <ListItemText>
                            {round(infoMapper[roiID]["spatial_entropy"], 3)}
                        </ListItemText>
                    </ListItem>
                </List>
            </CardContent>
        </Card>
    );
}
