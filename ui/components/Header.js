import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Toolbar from "@material-ui/core/Toolbar";
import { GitHub as GitHubIcon } from "@material-ui/icons";
import BookIcon from "@material-ui/icons/LibraryBooks";
import Tooltip from "@material-ui/core/Tooltip";
import Link from "next/link";
import { IconButton } from "@material-ui/core";

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
            <img src="/header-logo.png" alt="logo" height="50px" />
          </a>

          <Link href="/about">
            <Tooltip title="Manual & API doc">
              <IconButton aria-label="Help" color="inherit">
                <BookIcon />
              </IconButton>
            </Tooltip>
          </Link>

          <a href="https://github.com" target="_blank">
            <Tooltip title="Star us!">
              <IconButton aria-label="Github" color="inherit">
                <GitHubIcon />
              </IconButton>
            </Tooltip>
          </a>
        </Toolbar>
      </AppBar>
    </div>
  );
}
