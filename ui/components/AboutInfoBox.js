import {Accordion, AccordionDetails, AccordionSummary} from "@material-ui/core";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";
import Typography from "@material-ui/core/Typography";


export default function AboutInfoBox(props) {
    return <Accordion expanded={true}>
        <AccordionSummary
            expandIcon={<ExpandMoreIcon/>}
        >
            <Typography style={{"font-style": "italic"}}>{props.title}</Typography>
        </AccordionSummary>
        <AccordionDetails>
            <Typography>
                {props.children}
            </Typography>
        </AccordionDetails>
    </Accordion>
}