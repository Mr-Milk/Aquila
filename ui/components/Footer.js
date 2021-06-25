import React from 'react';
import {makeStyles} from '@material-ui/core/styles';
import {Typography} from "@material-ui/core";


const useStyles = makeStyles((theme) => ({
    footer: {
        width: '100%',
        height: '100px',
        borderTop: '1px solid #eaeaea',
        display: 'inline-block',
        textAlign: 'center',
        verticalAlign: 'middle',
        marginTop: theme.spacing(4),
    },
    text: {
        color: 'grey',
        marginTop: theme.spacing(2),
    }
}));


export default function Footer() {
    const classes = useStyles();
    const year = new Date().getFullYear();

    return (
        <footer className={classes.footer}>
            <Typography className={classes.text}>
                &copy; {year} Copyright:{' '}
                <a href="https://cheunglab.org" target="_blank">
                    <strong>Cheunglab</strong>
                </a>
            </Typography>
        </footer>
    )
}

