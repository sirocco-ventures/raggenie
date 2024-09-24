import style from "../style.module.css";
import { AreaChart as ReAreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';

function AreaChart({ title = "Area Chart", data = [], xAxis = "name", yAxis = "value"},  dataLength = 12) {
  return (
    <>
      <div className={style.ChartContainer}>
        <span className={style.ChartTitle}>{title}</span>
        <div className={style.BarChartResponsive}>
          <ReAreaChart data={data.slice(0, dataLength)}  width={450} height={183}>
            <CartesianGrid vertical={false} strokeDasharray="3 3" />
            <XAxis dataKey={xAxis} axisLine={false} tickLine={false} tick={<CustomTick axis="x" />} />
            <YAxis axisLine={false} tickLine={false} tick={<CustomTick axis="y" />} />
            <Tooltip />
            <Area type="monotone" dataKey={yAxis} strokeWidth={3} stroke="#3893FF" fillOpacity={0.1} fill="#3893FF" />
          </ReAreaChart>
        </div>
      </div></>
  );
}

const CustomTick = ({ x, y, payload, axis }) => {
  const commonProps = {
    color: "rgba(28, 28, 28, 0.40",
    textAlign: "center",
    opacity: "40%",
    fontFamily: "Inter",
    fontSize: "11px",
    fontStyle: "normal",
    fontWeight: "400",
    lineHeight: "18px", /* 180% */
  };

  return (
    <text
      x={axis === 'x' ? x : x - (axis === 'y' ? 5 : 0)} // Adjust horizontal position for Y-axis
      y={axis === 'x' ? y + 15 : y} // Adjust vertical position for X-axis
      textAnchor={axis === 'y' ? "end" : "middle"} // Text alignment for Y and X axis
      {...commonProps}
    >
     <tspan> {payload.value}</tspan>
    </text>
  );
};


export default AreaChart;
