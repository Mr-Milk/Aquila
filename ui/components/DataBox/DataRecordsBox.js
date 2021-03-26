import { Chip, IconButton, Paper, SvgIcon } from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import Launch from "@material-ui/icons/Launch";
import { dataRecord } from "../../data/api";
import { makeStyles } from "@material-ui/core/styles";

const useStyles = makeStyles((theme) => ({
  link: {
    cursor: "pointer",
  },
  pb2: {
    paddingBottom: theme.spacing(2),
  },
  pb: {
    paddingBottom: theme.spacing(1),
  },
  mr: {
    marginRight: theme.spacing(1),
  },
  alignMiddle: {
    display: "inline-block",
    textAlign: "middle",
  },
}));

export default function DataRecordsBox(props) {
  const { data } = dataRecord(props.dataID);
  const classes = useStyles();

  let technology = "";
  let molecular = "";
  let tissue = "";
  let disease = "";
  let article = "";
  let article_url = "";
  let journal = "";
  let year = "";
  let cell_count = "";
  let marker_count = "";

  let title = "Data title";

  if (data) {
    technology = data["technology"];
    molecular = data["molecular"];
    disease = data["disease_subtype"];
    tissue = data["tissue"];
    article = data["source_name"];
    article_url = data["source_url"];
    journal = data["journal"];
    year = data["year"];
    cell_count = data["cell_count"];
    marker_count = data["marker_count"];

    title = `${disease}, ${molecular} | ${technology} (${journal}, ${year})`;
  }

  return (
    <>
      <Typography variant="h5" className={classes.pb2}>
        {title}
      </Typography>

      <Typography variant="body1" className={classes.pb}>
        <ItemTitle>Title:</ItemTitle> {article}{" "}
        <IconButton
          href={article_url}
          target="_blank"
          rel="noreferrer noopener"
          size="small"
        >
          <Launch fontSize="small" color="primary" />
        </IconButton>
      </Typography>

      <Typography variant="body1" className={classes.pb}>
        <ItemTitle>Technology:</ItemTitle>
        <TechChip label={technology} />
      </Typography>

      <Typography variant="body1" className={classes.pb}>
        <ItemTitle>Molecular:</ItemTitle>
        {molecular}
      </Typography>

      <Typography variant="body1" className={classes.pb}>
        <ItemTitle>Cells:</ItemTitle>
        {cell_count}
      </Typography>

      <Typography variant="body1" className={classes.pb}>
        <ItemTitle>Markers:</ItemTitle>
        {marker_count}
      </Typography>
    </>
  );
}

function TechChip(props) {
  const linkPool = {
    MIBI: "https://www.ionpath.com/",
  };
  const link = linkPool[props.label];
  const pointerCursor = { cursor: "pointer" };
  return (
    <a href={link} target="_blank" rel="noreferrer noopener">
      <Chip
        label={props.label}
        color="primary"
        size="small"
        style={pointerCursor}
      />
    </a>
  );
}

function ItemTitle({ children }) {
  const classes = useStyles();
  return <strong className={classes.mr}>{children}</strong>;
}
