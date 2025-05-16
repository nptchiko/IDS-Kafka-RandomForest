import { useEffect, useState } from "react";

interface FlowData {
    time: String;
    src_ip: String;
    dst_ip: String;
    protocol: String;
    version: String;
    status: String;
}

const CaptureFlowTable = ({ data }: { data: FlowData }) => {
  const [internalLogData, setInternalLogData] = useState<FlowData[]>([]);

  useEffect(() => {
    if (data && 
        data.time !== 'unknown' &&
        data.src_ip !== 'unknown' &&
        data.dst_ip !== 'unknown' &&
        data.protocol !== 'unknown' &&
        data.status !== 'unknown' 
    ) {
        setInternalLogData((prevData) => [data, ...prevData]);
      console.log('RealtimeLogtable - Dữ liệu cập nhật:', [...internalLogData, data]);
    }
  }, [data]);

  return (
    <div className="full-screen">
      <h2 className="title">Table show log realtime</h2>
      <div className="responsive-table">

        <table className="w-full table-auto border">
          <thead className="sticky">
            <tr>
              <th className="border px-4 py-2">Time</th>
              <th className="border px-4 py-2">Source IP</th>
              <th className="border px-4 py-2">Destination IP</th>
              <th className="border px-4 py-2">Protocol</th>
              <th className="border px-4 py-2">Version</th>
              <th className="border px-4 py-2">Status</th>
            </tr>
          </thead>
          <tbody>
            {internalLogData.map((entry) => (
              <tr key={String(entry.time) || undefined}>
                <td className="border px-4 py-1">{entry.time}</td>
                <td className="border px-4 py-1">{entry.src_ip}</td>
                <td className="border px-4 py-1">{entry.dst_ip}</td>
                <td className="border px-4 py-1">{entry.protocol}</td>
                <td className="border px-4 py-1">{entry.version}</td>
                <td className="border px-4 py-1">{entry.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}



export default CaptureFlowTable;