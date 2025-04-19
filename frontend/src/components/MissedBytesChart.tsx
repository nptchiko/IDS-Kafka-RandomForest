// import React from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer } from "recharts";

const areaData = [
  { time: "8:00", missed: 20 },
  { time: "8:15", missed: 55 },
  { time: "8:30", missed: 35 },
  { time: "8:45", missed: 30 },
];

const MissedBytesChart = () => (
  <div>
    <h2 className="title">This chart for missed_bytes realtime</h2>
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={areaData}>
        <XAxis dataKey="time" />
        <YAxis />
        <RechartsTooltip />
        <Area type="monotone" dataKey="missed" stroke="#82ca9d" fill="#82ca9d" />
      </AreaChart>
    </ResponsiveContainer>
  </div>
);

export default MissedBytesChart;