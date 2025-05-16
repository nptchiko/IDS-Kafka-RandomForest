// import React from "react";
import { useEffect, useRef, useState } from "react";
import { AreaChart, Area, XAxis, YAxis, Tooltip as RechartsTooltip, ResponsiveContainer } from "recharts";

interface MissedBytesData {
  id: string;
  time: string;
  missed_bytes: number;
}

const MissedBytesChart = ({missedBytesData}:{missedBytesData: MissedBytesData}) => {
  const [internalMissedBytesData, setinternalMissedBytesData] = useState<MissedBytesData[]>([]);
  const missedBytesRef = useRef<MissedBytesData[]>([]);
  
    useEffect(() => {
      if (missedBytesData && 
        missedBytesData.id != 'unknown' && 
        missedBytesData.time != 'unknown' ) {
        missedBytesRef.current.push(missedBytesData)
        setinternalMissedBytesData([...missedBytesRef.current]);
        console.log('Missed bytes data - Dữ liệu cập nhật:', missedBytesRef.current);
      }
    }, [missedBytesData]);

  return (
    <div className="full-screen">
    <h2 className="title">Missed byte chart</h2>
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={internalMissedBytesData}>
        <XAxis dataKey="time" />
        <YAxis />
        <RechartsTooltip />
        <Area type="monotone" dataKey="missed_bytes" stroke="#82ca9d" fill="#82ca9d" />
      </AreaChart>
    </ResponsiveContainer>
  </div>
  );
};

export default MissedBytesChart;