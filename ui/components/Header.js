import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import GitHubIcon from '@material-ui/icons/Github';
import BookIcon from '@material-ui/icons/LibraryBooks';
import Tooltip from '@material-ui/core/Tooltip';
import Link from 'next/link';
import {IconButton} from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
    root: {
        flexGrow: 1,
    },
    title: {
        flexGrow: 1,
    },
}));


export default function Header() {
    const classes = useStyles();

    return (
        <div className={classes.root}>
            <AppBar position="static">
                <Toolbar>
                    <a href="/" className={classes.title}>
                        <Typography variant="h6">
                            Baize
                        </Typography>
                    </a>

                    <Link href="/about">
                        <Tooltip title="Manual & API doc">
                            <IconButton aria-label="Help" color="inherit">
                                <BookIcon/>
                            </IconButton>
                        </Tooltip>
                    </Link>

                    <a href="https://github.com" target="_blank">
                        <Tooltip title="Star us!">
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