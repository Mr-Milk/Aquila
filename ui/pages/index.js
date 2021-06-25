import Layout from "../components/layout";
import DBStats from "../components/DBStats";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import Container from "@material-ui/core/Container";

import RecordsTable from "../components/RecordsTable";

// import ParticlesBg from 'particles-bg'

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
    desc: {
        marginTop: theme.spacing(4),
        marginBottom: theme.spacing(4),
        paddingRight: theme.spacing(14),
        paddingLeft: theme.spacing(14),
        fontSize: "1.5rem",
        lineHeight: "2rem",
        color: "#555555",
        [theme.breakpoints.down('sm')]: {
            paddingRight: theme.spacing(2),
            paddingLeft: theme.spacing(2),
        }
    },
    bg: {
        position: "absolute",
        zIndex: -1,
        top: "50px",
        left: "0px",
        height: "550px",
    },
    logo: {
        marginTop: theme.spacing(3),
        width: "50%",
        [theme.breakpoints.down('sm')]: {
            width: "70%",

        }
    },
    tb: {
        marginTop: theme.spacing(2),
    }
}));

export default function Home() {
    const classes = useStyles();
    return (
        <Layout>
            {/*<ParticlesBg num={200} type="tadpole" bg={true} className={classes.bg}/>*/}
            <Container style={{textAlign: 'center'}}>
                <img src={"/aquila.png"} alt={"logo of aquila"} className={classes.logo}/>

                <Typography variant="body1" className={classes.desc}>
                    Aquila is a spatial single cell pathology database, we collect single cell data with spatial
                    information.
                </Typography>
            </Container>

            <DBStats/>
            <RecordsTable className={classes.tb}/>
        </Layout>
    );
}
