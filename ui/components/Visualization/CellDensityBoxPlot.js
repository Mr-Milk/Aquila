import EChartsReact from "echarts-for-react";
import {median, sort} from "mathjs";

function BoxStats(arr) {
    arr.map((i) => {
        if (i < 0) {
            console.log("Negative in array");
        }
    });
    const sortArr = sort(arr);
    const len = arr.length;
    const arr_median = median(sortArr);
    const q1 = sortArr[Math.round(len * 0.25)];
    const q3 = sortArr[Math.round(len * 0.75)];
    const IQR = q3 - q1;
    const min = sortArr[0];
    const max = sortArr.slice(-1);
    let lower = q1 - 1.5 * IQR;
    let upper = q3 + 1.5 * IQR;
    lower = lower > min ? lower : min;
    upper = upper < max ? upper : max;
    let outliers = [];
    sortArr.map((i) => {
        if (i < lower && i > upper) {
            outliers.push(i);
        }
    });

    return {
        boxStats: [lower, q1, arr_median, q3, upper],
        outliers: outliers,
    };
}

export default function CellDensityBoxPlot(props) {
    const {data, ...leftProps} = props;
    const cell_types = data["cell_types"];
    const density = data["density"];

    const boxData = [];
    const outliersData = [];
    density.map((arr, i) => {
        let {boxStats, outliers} = BoxStats(arr);
        boxData.push({
            name: cell_types[i],
            value: boxStats,
        });
        outliersData.push({
            name: cell_types[i],
            value: outliers,
        });
    });

    const option = {
        title: [
            {
                text: "Cell Density",
                left: "center",
            },
        ],
        tooltip: {
            trigger: "item",
            axisPointer: {
                type: "shadow",
            },
        },
        grid: {
            left: "10%",
            right: "10%",
            bottom: "15%",
        },
        xAxis: {
            type: "category",
            splitNumber: cell_types.length,
            axisTick: {
                alignWithLabel: true,
            },
            axisLabel: {
                interval: 0,
                rotate: 30,
            },
            nameRotate: 30,
            nameGap: 30,
            splitArea: {
                show: false,
            },
            splitLine: {
                show: false,
            },
            nameTextStyle: {
                align: "center",
            },
            data: cell_types,
        },
        yAxis: {
            type: "value",
            name: "Density",
            splitArea: {
                show: true,
            },
        },
        series: [
            {
                name: "outlier",
                type: "scatter",
                data: outliersData,
            },
            {
                name: "boxplot",
                type: "boxplot",
                data: boxData,
            },
        ],
    };

    return (
        <EChartsReact
            option={option}
            style={{width: "650px", height: "500px"}}
            {...leftProps}
        />
    );
}
