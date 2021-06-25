import EChartsReact from "echarts-for-react";
import assignColor from "./assignColors";

// Palette name: LaJolla_20
const color_pool = [
    '#2166ac',
    '#67a9cf',
    '#d1e5f0',
    '#f7f7f7',
    '#fddbc7',
    '#ef8a62',
    '#b2182b'
];

export default function CellInteractionMap(props) {
    const {data, ...leftProps} = props;
    const cell_types = data["cell_types"];
    const relationship = data["relationship"];

    const nodes = [];
    cell_types.map((c) => {
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
            text: "Cell-Cell Interaction",
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
            text: ["+1 Association", "-1 Avoidance"],
        },
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
