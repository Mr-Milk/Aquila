import {Accordion, AccordionDetails, AccordionSummary} from "@material-ui/core";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import Typography from "@material-ui/core/Typography";


export default function AboutInfoBox(props) {
    return <Accordion defaultExpanded={true}>
        <AccordionSummary
            expandIcon={<ExpandMoreIcon/>}
        >
            <Typography style={{"fontStyle": "italic"}}>{props.title}</Typography>
        </AccordionSummary>
        <AccordionDetails className={props.className}>
            {props.children}
        </AccordionDetails>
    </Accordion>
}