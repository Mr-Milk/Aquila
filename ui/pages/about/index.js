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
            margin: theme.spacing(6),
            [theme.breakpoints.up["xl"]]: {
                margin: theme.spacing(12),
            }
        },
        title: {
            marginBottom: theme.spacing(2),
        },
        questionBox: {
            width: "90%",
            marginBottom: theme.spacing(4),
        }
    })
)

export default function AboutPage() {
    const classes = useStyles();

    return (
        <Layout>
            <Container className={classes.container}>
                <Typography variant={"h3"} className={classes.title} color={"#555555"}>Manual</Typography>
                <div className={classes.questionBox}>
                    <AboutInfoBox title={"How to view the data?"}>
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
                                            'color': '#b2182b',
                                            'font-weight': 'bold'
                                        }}>{" association "}</Typography>
                                        and <Typography component={"span"} style={{
                                            'color': '#2166ac',
                                            'font-weight': 'bold'
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
                </div>

                <Typography variant={"h3"} className={classes.title} color={"#555555"}>API Documents</Typography>
                <Typography>Please refer to API documents here.</Typography>

            </Container>
        </Layout>
    );
}
