// import React from "react";
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer } from "recharts";

const pieData = [
  { name: "TLS1.3", value: 27 },
  { name: "TLS1.2", value: 23 },
  { name: "TLS1.1", value: 18 },
  { name: "Old SSL", value: 32 },
];

const COLORS = ["#00BFFF", "#32CD32", "#FFD700", "#FF7F7F"];

const TlsPieChart = () => (
  <div>
    <h2 className="title">This chart for TLS version</h2>
    <ResponsiveContainer width="100%" height={250}>
      <PieChart>
        <Pie
          data={pieData}
          dataKey="value"
          nameKey="name"
          cx="50%"
          cy="50%"
          outerRadius={80}
          innerRadius={40}
          label={(entry) => `${entry.name} - ${entry.value}%`}
        >
          {pieData.map((_, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index]} />
          ))}
        </Pie>
        <RechartsTooltip />
      </PieChart>
    </ResponsiveContainer>
  </div>
);

export default TlsPieChart;