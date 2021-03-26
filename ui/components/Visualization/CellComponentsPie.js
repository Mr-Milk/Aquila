import EChartsReact from "echarts-for-react";

export default function CellComponentsPie(props) {
  const { data, ...leftProps } = props;
  const cell_types = data["cell_types"];
  const components = data["components"];
  const plotData = [];
  cell_types.map((t, i) => {
    plotData.push({ name: t, value: components[i] });
  });

  const option = {
    title: {
      text: "Cell Components",
      left: "center",
    },
    tooltip: {
      trigger: "item",
    },
    legend: {
      show: false,
    },
    series: [
      {
        name: "cell components",
        type: "pie",
        radius: ["30%", "60%"],
        itemStyle: {
          borderRadius: 8,
          borderColor: "#fff",
          borderWidth: 2,
        },
        data: plotData,
        // data: [
        //   { value: 1048, name: "搜索引擎" },
        //   { value: 735, name: "直接访问" },
        //   { value: 580, name: "邮件营销" },
        //   { value: 484, name: "联盟广告" },
        //   { value: 300, name: "视频广告" },
        // ],
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: "rgba(0, 0, 0, 0.5)",
          },
        },
      },
    ],
  };

  return (
    <EChartsReact
      option={option}
      style={{ width: "500px", height: "500px" }}
      {...leftProps}
    />
  );
}
