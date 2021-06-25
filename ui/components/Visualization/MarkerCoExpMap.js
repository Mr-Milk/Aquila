import EChartsReact from "echarts-for-react";
import assignColor from "./assignColors";

// Palette name: Batlow_20
const color_pool = [
    "#011959",
    "#08275C",
    "#0E355E",
    "#134360",
    "#1A5261",
    "#265F5F",
    "#386A58",
    "#4B724E",
    "#5F7843",
    "#757E38",
    "#8B852F",
    "#A88B2F",
    "#C3913B",
    "#DC964F",
    "#F19D6B",
    "#FAA587",
    "#FDAFA4",
    "#FDB8BF",
    "#FCC2DD",
    "#FACCFA",
];

export default function MarkerCoExpMap(props) {
    const {data, ...leftProps} = props;
    const markers = data["markers"];
    const relationship = data["relationship"];

    let graphic = {};

    if (markers.length === 0) {
        graphic = {
            type: "group",
            left: "center",
            top: "center",
            children: [
                {
                    type: "text",
                    z: 100,
                    left: "center",
                    top: "middle",
                    style: {
                        fill: "#333",
                        text: "No relationship to display",
                        fontSize: "24px",
                    },
                },
            ],
        };
    }

    const nodes = [];
    markers.map((c) => {
        nodes.push({name: c});
    });

    const values = [];
    relationship.map((i) => {
        values.push(i[2]);
    });
    let colors = assignColor(color_pool, values, -1, 1);

    const links = [];
    relationship.map((i, ix) => {
        links.push({
            source: i[0],
            target: i[1],
            value: i[2],
            lineStyle: {
                color: colors[ix],
            },
            select: {
                label: {
                    show: false,
                    formatter: "{a} {b} {c}",
                },
            },
        });
    });

    const option = {
        title: {
            text: "Spatially co-expressed markers",
            left: "center",
        },
        tooltip: {},
        visualMap: {
            min: -1,
            max: 1,
            precision: 3,
            calculable: false,
            inRange: {
                color: color_pool,
            },
            text: ["Positive", "Negative"],
        },
        graphic: [graphic],
        animationDurationUpdate: 1500,
        animationEasingUpdate: "quinticInOut",
        series: [
            {
                type: "graph",
                layout: "circular",
                edgeSymbol: ["none", "none"],
                label: {
                    show: true,
                },
                data: nodes,
                links: links,
                lineStyle: {
                    opacity: 0.9,
                    width: 2,
                    curveness: 0,
                },
            },
        ],
    };

    return (
        <EChartsReact
            option={option}
            style={{width: "550px", height: "400px"}}
            {...leftProps}
        />
    );
}
