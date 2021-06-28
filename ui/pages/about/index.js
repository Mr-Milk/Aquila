import Layout from "../../components/layout";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import {makeStyles} from "@material-ui/core/styles";
import AboutInfoBox from "../../components/AboutInfoBox";
import Visibility from "@material-ui/icons/Visibility";
import React from "react";
import {Link as LinkMUI, List, ListItem, ListItemIcon, ListItemText} from "@material-ui/core";
import GetApp from "@material-ui/icons/GetApp";
import Link from 'next/link';
import LinkIcon from "@material-ui/icons/Link";

const useStyles = makeStyles((theme) => ({
        container: {
            display: "flex",
            flexDirection: "column",
            marginTop: theme.spacing(4),
        },
        title: {
            marginBottom: theme.spacing(2),
            fontSize: 36,
            color: '#555555',
            [theme.breakpoints.down("sm")]: {
                fontSize: 28,
            }
        },
        questionBox: {
            marginBottom: theme.spacing(4),
            marginRight: 0,
        },
        gif: {
            height: "500px",
            margin: "2rem",
            [theme.breakpoints.down("sm")]: {
                width: "150px",
                height: "100%"
            }
        },
        gifBlock: {
            textAlign: "center",
            display: "block"
        }
    })
)

export default function AboutPage() {
    const classes = useStyles();

    return (
        <Layout>
            <Container className={classes.container}>
                <Typography variant={"h3"} className={classes.title}>Manual</Typography>
                <div className={classes.questionBox}>
                    <AboutInfoBox title={"How to view the data?"} >
                        <div style={{"display": "block"}}>
                            <Typography variant={"body1"}>
                            Go to the <Link href="/"><LinkMUI>main page</LinkMUI></Link>, the data table contains all
                            the data we currently stored.
                            You can sort or search the table. Click on the following button to view the data.
                        </Typography>
                            <List dense={true}>
                            <ListItem>
                                <ListItemIcon>
                                    <Visibility color="primary"/>
                                </ListItemIcon>
                                <ListItemText>
                                    View the data
                                </ListItemText>
                            </ListItem>
                            <ListItem>
                                <ListItemIcon>
                                    <GetApp color="primary"/>
                                </ListItemIcon>
                                <ListItemText>
                                    Download the data
                                </ListItemText>
                            </ListItem>
                            <ListItem>
                                <ListItemIcon>
                                    <LinkIcon color="primary"/>
                                </ListItemIcon>
                                <ListItemText>
                                    View the source paper
                                </ListItemText>
                            </ListItem>
                        </List>
                        </div>

                    </AboutInfoBox>

                    <AboutInfoBox title={"How to read the analysis?"}>
                        <List>
                            <ListItem>
                                <ListItemText>
                                    <Typography variant={"h6"}>Cell components</Typography>
                                    <Typography>Cell components tells the composition of different cell
                                        types.</Typography>
                                </ListItemText>
                            </ListItem>

                            <ListItem>
                                <ListItemText>
                                    <Typography variant={"h6"}>Cell density</Typography>
                                    <Typography>The density of each cell type.</Typography>
                                </ListItemText>
                            </ListItem>

                            <ListItem>
                                <ListItemText>
                                    <Typography variant={"h6"}>Cell-Cell Interaction</Typography>
                                    <Typography>There are two types of cell-cell relationship,
                                        <Typography component={"span"} style={{
                                            color: '#b2182b',
                                            fontWeight: 'bold'
                                        }}>{" association "}</Typography>
                                        and <Typography component={"span"} style={{
                                            color: '#2166ac',
                                            fontWeight: 'bold'
                                        }}>{" avoidance"}</Typography>.
                                        Association means the two types of cell are very likely to meet each other at
                                        the neighborhood.
                                        Avoidance means they are not welcome to each other. </Typography>

                                    <Typography>This analysis is calculated using permutation test, the significance of
                                        cell-cell interaction will calculate in each ROI.
                                        The value is calculated by The number of ROI that are significant divided by all
                                        ROI. The sign is used
                                        to determine the direction. Positive value is association and negative value is
                                        avoidance. For example:, if cell
                                        A and Cell B is association in 4 ROI, avoidance in 1 ROI and show no
                                        relationship in 2 ROI. The value is 4 / (4+1+2)
                                        around 0.57. If avoidance in 4 ROI, association in 1 ROI and show no
                                        relationship in 2 ROI, the value is -0.57</Typography>
                                </ListItemText>
                            </ListItem>

                            <ListItem>
                                <ListItemText>
                                    <Typography variant={"h6"}>Cell neighbors</Typography>
                                    <Typography>Turn on the show neighbors to show neighbors relationship. Cell
                                        neighbors is searched using KD-tree.</Typography>
                                </ListItemText>
                            </ListItem>
                        </List>
                    </AboutInfoBox>

                    <AboutInfoBox title={"How to navigate between ROI?"} className={classes.gifBlock}>
                        <img src={"/navigate-roi.gif"} alt={"how to navigate between roi"} className={classes.gif}/>
                        <Typography>Click on the View button to navigate between ROI.</Typography>
                    </AboutInfoBox>

                    <AboutInfoBox title={"How to view cell neighbors?"} className={classes.gifBlock}>
                        <img src={"/toggle-neighbors.gif"} alt={"how to view cell neighbors"} className={classes.gif}/>
                        <Typography>Toggle the "Show neighbors" switch to view neighbors relationship in a ROI.</Typography>
                    </AboutInfoBox>

                    <AboutInfoBox title={"How to view a marker expression?"} className={classes.gifBlock}>
                        <img src={"/view-markers.gif"} alt={"how to view markers"} className={classes.gif}/>
                        <Typography>Search or select the interested marker in a ROI.</Typography>
                    </AboutInfoBox>
                </div>

                <Typography variant={"h3"} className={classes.title}>API Documents</Typography>
                <Typography>Please refer to API documents <LinkMUI href={"https://github.com/Mr-Milk/Aquila/blob/master/api.md"}>here</LinkMUI>.</Typography>

            </Container>
        </Layout>
    );
}
