import Layout from "../layout";
import { useRouter } from "next/router";
import { allDataIDs } from "../../data/api";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Button from "@material-ui/core/Button";
import HomeIcon from "@material-ui/icons/Home";
import { Grid, Paper } from "@material-ui/core";
import DataRecordsBox from "../../components/DataBox/DataRecordsBox";
import DataStatsBox from "../../components/DataBox/DataStatsBox";

const useStyles = makeStyles((theme) => ({
  box: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    color: "grey",
  },
  emptyBox: {
    height: "300px",
  },
  textBox: {
    marginBottom: theme.spacing(2),
  },
  dataBoxRoot: {
    flexGrow: 1,
    marginTop: theme.spacing(4),
  },
  dataBox: {
    padding: theme.spacing(2),
  },
  dataStatsBox: {
    height: "500px",
  },
}));

export default function DataPanel() {
  const router = useRouter();
  const classes = useStyles();
  const { data_id } = router.query;
  const { data } = allDataIDs();

  if (data !== undefined) {
    const correct_data_id = data.includes(data_id);

    if (correct_data_id) {
      return (
        <Layout>
          <div className={classes.dataBoxRoot}>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Paper className={classes.dataBox}>
                  <DataRecordsBox dataID={data_id} />
                </Paper>
              </Grid>
              <Grid item xs={12}>
                <Paper className={`${classes.dataBox}`}>
                  <DataStatsBox dataID={data_id} />
                </Paper>
              </Grid>
              <Grid item xs={12}>
                <Paper className={classes.dataBox}>xs=12</Paper>
              </Grid>
            </Grid>
          </div>
          <p>{`This is a data page of ${data_id}`}</p>
        </Layout>
      );
    } else {
      return (
        <Layout>
          <div className={classes.box}>
            <div className={classes.emptyBox} />
            <Typography
              variant="h4"
              color="textSecondary"
              className={classes.textBox}
            >
              We don't have such data, maybe you are missing?
            </Typography>
            <Button
              startIcon={<HomeIcon />}
              color="inherit"
              variant="outlined"
              href="/"
            >
              Home
            </Button>
            <div className={classes.emptyBox} />
          </div>
        </Layout>
      );
    }
  } else {
    return (
      <Layout>
        <div className={classes.box}>
          <div className={classes.emptyBox} />
          <Typography
            variant="h4"
            color="textSecondary"
            className={classes.textBox}
          >
            Oops! Seems like something went wrong
          </Typography>
          <Button
            startIcon={<HomeIcon />}
            color="inherit"
            variant="outlined"
            href="/"
          >
            Home
          </Button>
          <div className={classes.emptyBox} />
        </div>
      </Layout>
    );
  }
}
