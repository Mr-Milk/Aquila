import EChartsReact from "echarts-for-react";
import { cellInfo } from "../../data/api";
import Skeleton from "@material-ui/lab/Skeleton";

export default function ROICellMap(props) {
  const { showNeighbors, cellInfoData, ...leftProps } = props;

  let hasCellType = true;
  const legend_data = [];
  const data = [];
  const categories = [];
  const links = [];
  const nameMapper = {};

  const cell_types = cellInfoData["cell_type"];
  if (cell_types.length === 0) {
    hasCellType = false;
  }
  const cell_name = cellInfoData["cell_name"];
  const cell_x = cellInfoData["cell_x"];
  const cell_y = cellInfoData["cell_y"];

  const neighbor_one = cellInfoData["neighbor_one"];
  const neighbor_two = cellInfoData["neighbor_two"];

  cell_types.map((t) => {
    if (!legend_data.includes(t)) {
      legend_data.push(t);
    }
  });

  cell_x.map((x, i) => {
    data.push({
      id: i,
      x: x,
      y: cell_y[i],
      value: hasCellType ? cell_types[i] : "unknown",
      category: hasCellType ? cell_types[i] : "unknown",
    });
    categories.push({
      name: hasCellType ? cell_types[i] : "unknown",
    });
    nameMapper[cell_name[i]] = i;
  });

  neighbor_one.map((n, i) => {
    links.push({
      source: nameMapper[n],
      target: nameMapper[neighbor_two[i]],
      lineStyle: {
        width: 1,
      },
    });
  });

  const option = {
    title: {
      text: "Cell Map",
      left: "center",
    },
    tooltip: {
      trigger: "item",
      formatter: "{c}",
    },
    legend: {
      data: legend_data,
      orient: "vertical",
      left: "left",
      top: "center",
      itemHeight: 8,
      itemWidth: 8,
      textStyle: {
        fontSize: 8,
      },
    },
    series: [
      {
        type: "graph",
        layout: "none",
        symbolSize: 3,
        data: data,
        categories: categories,
        links: showNeighbors ? links : [],
      },
    ],
  };

  return (
    <EChartsReact
      option={option}
      style={{ width: "650px", height: "550px" }}
      {...leftProps}
    />
  );
}
