// import React from "react";
import { useEffect, useState } from "react";
import { PieChart, Pie, Cell, Tooltip as RechartsTooltip, ResponsiveContainer } from "recharts";

interface TlsPieData {
  id: string;
  name: string;
  value: number;
}

const COLORS = ["#00BFFF", "#32CD32", "#FFD700", "#FF7F7F"];

const TlsPieChart = ({ pieData }: { pieData: TlsPieData[] }) => {
  const [internalPieData, setInternalPieData] = useState<TlsPieData[]>([]);

  useEffect(() => {
    if (pieData && pieData.length > 0) {
      setInternalPieData((prevData) => [...prevData, ...pieData]);
      // setInternalPieData(pieData)
      console.log('TlsPieChart - Dữ liệu cập nhật:', [...internalPieData, ...pieData]);
    }
  }, [pieData]);

  return (
    <div>
      <h2 className="title">This chart for TLS version</h2>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={internalPieData}
            dataKey="value"
            nameKey="name"
            cx="50%"
            cy="50%"
            outerRadius={80}
            innerRadius={40}
            label={(entry) => `${entry.name} - ${entry.value}%`}
          >
            {internalPieData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <RechartsTooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TlsPieChart;