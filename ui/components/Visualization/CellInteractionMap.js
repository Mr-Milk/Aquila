import EChartsReact from "echarts-for-react";
import { sort } from "mathjs";

function assign_colors(colors, arr) {
  const cut = colors.length;
  const bin = 2 / cut;
  let ranges = {};
  let start = -1;
  colors.map((c) => {
    ranges[c] = [start, start + bin];
    start += bin;
  });
  let colors_arr = [];
  arr.map((a) => {
    if (a === 1) {
      colors_arr.push(colors.slice(-1)[0]);
    } else {
      Object.keys(ranges).forEach((k) => {
        let r = ranges[k];
        if (a >= r[0] && a < r[1]) {
          colors_arr.push(k);
        }
      });
    }
  });

  return colors_arr;
}

export default function CellInteractionMap(props) {
  const data = props.data;
  const cell_types = data["cell_types"];
  const relationship = data["relationship"];

  const nodes = [];
  cell_types.map((c) => {
    nodes.push({ name: c });
  });

  const color_pool = [
    "#F3E79B",
    "#FAC484",
    "#F8A07E",
    "#EB7F86",
    "#CE6693",
    "#A059A0",
    "#5C53A5",
  ];

  const values = [];
  relationship.map((i) => {
    values.push(i[2]);
  });
  let colors = assign_colors(color_pool, values);

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
    <EChartsReact option={option} style={{ width: "650px", height: "500px" }} />
  );
}
