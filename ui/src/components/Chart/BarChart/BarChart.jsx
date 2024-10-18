import React from 'react';
import { Bar, BarChart as ReBarChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const BarChart = ({ title = "Bar Chart", data = [], xAxis = "name", yAxis = "value", dataLength = 12 }) => {
  const CustomBar = ({ x, y, height }) => (
    <rect width={30} height={height} x={x + 20} y={y} fill="#74B3FF" rx={4} />
  );

  const CustomLabel = ({ x, y, payload, textAnchor = "middle", offset = 0 }) => (
    <text x={x - offset} y={y + 4} textAnchor={textAnchor} fill="#888787" fontSize={12} opacity={0.8}>
      {payload.value}
    </text>
  );

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '6px' }}>
      <h3 style={{ textAlign: 'center', fontSize: '1.2em', marginBottom: '20px' }}>{title}</h3>
      <ResponsiveContainer width="100%" height={320}>
        <ReBarChart data={data.slice(0, dataLength)} barCategoryGap={10} barGap={2}>
          <XAxis
            dataKey={xAxis}  axisLine={false} tickLine={false}
            tick={<CustomLabel />}
            interval={0}  tickMargin={10} angle={0}
          />
          <YAxis
            axisLine={false}  tickLine={false}
            tick={<CustomLabel textAnchor="end" offset={5} />}
            width={40}  tickMargin={5}
          />
          <Bar dataKey={yAxis} shape={<CustomBar />} />
          <Tooltip cursor={false} />
        </ReBarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default BarChart;



