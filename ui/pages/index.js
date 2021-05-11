import Layout from "../components/layout";
import DBStats from "../components/DBStats";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import RecordsTable from "../components/RecordsTable";
import { Paper } from "@material-ui/core";

import Particles from "react-particles-js";

const useStyles = makeStyles((theme) => ({
  titleBox: {
    height: "550px",
    display: "flex",
    flexDirection: "column",
    flexWrap: "wrap",
    flexGrow: 1,
    alignItems: "center",
    justifyContent: "center",
  },
  title: {
    color: "#26a69a",
    marginTop: theme.spacing(2),
  },
  bg: {
    position: "absolute",
    zIndex: -1,
    top: "50px",
    left: "0px",
    height: "550px",
  },
  intro: {},
}));

export default function Home() {
  const classes = useStyles();
  return (
    <Layout>
      <Container className={classes.titleBox}>
        <Particles
          params={{
            particles: {
              number: {
                value: 150,
                density: {
                  enable: true,
                  value_area: 1200,
                },
              },
              color: {
                value: "#ff8f00",
              },
              move: {
                direction: "right",
                speed: 0.1,
              },
              size: {
                value: 3,
              },
              line_linked: {
                enable: true,
                color: "#dddddd",
              },
            },
            interactivity: {
              events: {
                onclick: {
                  enable: true,
                  mode: "push",
                },
              },
              modes: {
                push: {
                  particles_nb: 1,
                },
              },
            },
            retina_detect: true,
          }}
          className={classes.bg}
        />
        <Typography variant="h4" className={classes.title}>
          Aquila: Spatial Single Cell Pathology Database
        </Typography>
      </Container>

      <DBStats />
      <RecordsTable />
    </Layout>
  );
}
