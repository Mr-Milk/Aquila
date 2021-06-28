import React from "react";
import {makeStyles} from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import {Grid} from "@material-ui/core";

import {dbStats} from "../data/api";

const useStyles = makeStyles((theme) => ({
    root: {
        // marginTop: theme.spacing(3),
        marginBottom: theme.spacing(4),
        flexGrow: 1,
    },
    card: {
        width: "120px",
        height: "120px",
        [theme.breakpoints.down("sm")]: {
            width: "80px",
            height: "80px",
        }
    },
    text: {
        fontSize: "1.3rem",
        paddingBottom: theme.spacing(2),
        [theme.breakpoints.down('sm')]: {
            fontSize: "0.8rem"
        }
    }
}));

function StatsDisplayCard(props) {
    const classes = useStyles();
    return (
        <Card>
            <CardContent className={classes.card}>
                <Typography component="h2" className={classes.text}>
                    {props.title}
                </Typography>
                <Typography color="textSecondary" className={classes.text}>
                    {props.value}
                </Typography>
            </CardContent>
        </Card>
    );
}

export default function DBStats() {
    const classes = useStyles();
    const {data, isLoading, isError} = dbStats();
    const titles = ["Data", "Tissue", "Disease"];

    let dataCount = 0;
    let tissueCount = 0;
    let diseaseCount = 0;

    if (data) {
        dataCount = data["data_count"];
        tissueCount = data["tissue_count"];
        diseaseCount = data["disease_count"];
    }

    return (
        <Grid container className={classes.root}>
            <Grid item xs={12}>
                <Grid container justify="center" spacing={2}>
                    {[dataCount, tissueCount, diseaseCount].map((value, i) => (
                        <Grid key={titles[i]} item>
                            <StatsDisplayCard title={titles[i]} value={value}/>
                        </Grid>
                    ))}
                </Grid>
            </Grid>
        </Grid>
    );
}
