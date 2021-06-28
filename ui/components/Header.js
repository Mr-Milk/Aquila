import React from "react";
import {makeStyles} from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import {GitHub as GitHubIcon} from "@material-ui/icons";
import BookIcon from "@material-ui/icons/LibraryBooks";
import Tooltip from "@material-ui/core/Tooltip";
import Link from "next/link";
import {IconButton} from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
    bar: {
        flexGrow: 1,
    },
    AppLogo: {
        padding: "0.2rem",
        height: "50px",
        [theme.breakpoints.down('sm')]: {
            height: "40px",
        }
    }
}));

export default function Header() {
    const classes = useStyles();

    return (
        <div className={classes.bar}>
            <AppBar position="static">
                <Toolbar>
                    <a href="/" className={classes.bar}>
                        <img src="/header-logo.png" alt="logo" className={classes.AppLogo}/>
                    </a>

                    <Link href="/about">
                        <Tooltip title="Manual & API doc">
                            <IconButton aria-label="Help" color="inherit">
                                <BookIcon/>
                            </IconButton>
                        </Tooltip>
                    </Link>

                    <a href="https://github.com/Mr-Milk/Aquila" target="_blank">
                        <Tooltip title="Find us on Github!">
                            <IconButton aria-label="Github" color="inherit">
                                <GitHubIcon/>
                            </IconButton>
                        </Tooltip>
                    </a>
                </Toolbar>
            </AppBar>
        </div>
    );
}
