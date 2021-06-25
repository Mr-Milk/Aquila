import {Chip, IconButton} from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import Launch from "@material-ui/icons/Launch";
import {dataRecord} from "../../data/api";
import {makeStyles} from "@material-ui/core/styles";

const linkPool = {
    MIBI: "https://www.ionpath.com/",
    IMC: "https://www.fluidigm.com/applications/imaging-mass-cytometry",
    CODEX: "https://www.akoyabio.com/codex/",
    CyCIF: "https://www.cycif.org/",

    seqFISH: "https://www.seqfish.com/",
    osmFISH: "https://linnarssonlab.org/osmFISH/",
    MERFISH: "http://zhuang.harvard.edu/merfish.html",
};

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
    const {data} = dataRecord(props.dataID);
    const classes = useStyles();

    let technology = "";
    let molecule = "";
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
        molecule = data["molecule"];
        disease = data["disease_subtype"];
        tissue = data["tissue"];
        article = data["source_name"];
        article_url = data["source_url"];
        journal = data["journal"];
        year = data["year"];
        cell_count = data["cell_count"];
        marker_count = data["marker_count"];

        title = `${disease}, ${molecule} | ${technology} (${journal}, ${year})`;
    }

    return (
        <>
            <Typography variant="h5" className={classes.pb2}>
                {title}
            </Typography>

            <Typography variant="body1" className={classes.pb} component="div">
                <ItemTitle>Title:</ItemTitle> {article}{" "}
                <IconButton
                    href={article_url}
                    target="_blank"
                    rel="noreferrer noopener"
                    size="small"
                >
                    <Launch fontSize="small" color="primary"/>
                </IconButton>
            </Typography>

            <Typography variant="body1" className={classes.pb} component="div">
                <ItemTitle>Technology:</ItemTitle>
                <TechChip label={technology}/>
            </Typography>

            <Typography variant="body1" className={classes.pb} component="div">
                <ItemTitle>Molecular:</ItemTitle>
                {molecule}
            </Typography>

            <Typography variant="body1" className={classes.pb} component="div">
                <ItemTitle>Number of Cell:</ItemTitle>
                {cell_count}
            </Typography>

            <Typography variant="body1" className={classes.pb}>
                <ItemTitle>Number of Marker:</ItemTitle>
                {marker_count}
            </Typography>
        </>
    );
}

function TechChip(props) {
    const link = linkPool[props.label];
    const pointerCursor = {cursor: "pointer"};
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

function ItemTitle({children}) {
    const classes = useStyles();
    return <strong className={classes.mr}>{children}</strong>;
}
