// import React from "react";
import { useEffect, useState } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer } from "recharts";

interface MissedBytesData {
  id: string;
  time: string;
  missed_bytes: number;
}

const MissedBytesChart = ({missedBytesData}:{missedBytesData: MissedBytesData}) => {
  const [internalMissedBytesData, setinternalMissedBytesData] = useState<MissedBytesData[]>([]);
  
    useEffect(() => {
      if (missedBytesData && missedBytesData.id != 'unknown', missedBytesData.time != 'unknown' ) {
        setinternalMissedBytesData((prevData) => [...prevData, missedBytesData]);
        console.log('Missed bytes data - Dữ liệu cập nhật:', [...internalMissedBytesData, missedBytesData]);
      }
    }, [missedBytesData]);

  return (
    <div className="full-screen">
    <h2 className="title">Chart for missed bytes realtime</h2>
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={internalMissedBytesData}>
        <XAxis dataKey="time" />
        <YAxis />
        <RechartsTooltip />
        <Area type="monotone" dataKey="missed" stroke="#82ca9d" fill="#82ca9d" />
      </AreaChart>
    </ResponsiveContainer>
  </div>
  );
};

export default MissedBytesChart;