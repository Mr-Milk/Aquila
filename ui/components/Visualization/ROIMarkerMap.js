import EChartsReact from "echarts-for-react";
import {expInfo} from "../../data/api";
import Skeleton from "@material-ui/lab/Skeleton";
import React from "react";
import assignColor from "./assignColors";
import {max, min, round} from "mathjs";

// Palette name: red_16
const color_pool = [
    "#FFFFFF",
    "#F2EEDB",
    "#ECDBBD",
    "#E8C4A4",
    "#E5AC93",
    "#E19488",
    "#D87C82",
    "#CC6680",
    "#B9537E",
    "#A2437C",
    "#863576",
    "#68296B",
    "#49205A",
    "#2C1641",
    "#130C23",
    "#000000",
];

export default function ROIMarkerMap(props) {
    const {roiID, marker, cellInfo, ...leftProps} = props;

    const {data: exp, isLoading, isError} = expInfo(roiID, marker);

    if (isLoading || isError) {
        return <Skeleton height={"550px"} width={"650px"}/>;
    }

    const cell_x = cellInfo["cell_x"];
    const cell_y = cellInfo["cell_y"];
    const cell_exp = exp["expression"];
    const colors = assignColor(color_pool, cell_exp);
    const min_exp = min(cell_exp);
    const max_exp = max(cell_exp);

    const data = cell_x.map((c, i) => {
        return {
            x: c,
            y: cell_y[i],
            value: cell_exp[i],
            itemStyle: {
                color: colors[i],
            },
        };
    });

    const option = {
        title: {
            text: `Expression of ${marker}`,
            left: "center",
        },
        visualMap: {
            min: min_exp,
            max: max_exp,
            precision: 3,
            calculable: false,
            inRange: {
                color: color_pool,
            },
            text: [round(max_exp, 3), round(min_exp, 3)],
        },
        series: [
            {
                type: "graph",
                layout: "none",
                animation: false,
                symbolSize: 3,
                data: data,
                // links: [],
            },
        ],
    };

    return (
        <EChartsReact
            option={option}
            style={{width: "650px", height: "550px"}}
            {...leftProps}
        />
    );
}
