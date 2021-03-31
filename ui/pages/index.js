import Layout from "../components/layout";
import DBStats from "../components/DBStats";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import RecordsTable from "../components/RecordsTable";

const useStyles = makeStyles((theme) => ({
  titleBox: {
    display: "inline-block",
    textAlign: "center",
  },
  title: {
    color: "grey",
    marginTop: theme.spacing(2),
  },
}));

export default function Home() {
  const classes = useStyles();
  return (
    <Layout>
      <Container className={classes.titleBox}>
        <Typography variant="h4" className={classes.title}>
          Single Cell Pathology Database
        </Typography>
      </Container>

      <DBStats />
      <RecordsTable />
    </Layout>
  );
}
