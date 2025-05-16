import { useEffect, useState } from "react";

interface FlowData {
    id: String
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
      data.id !== 'unknown' &&
      data.time !== 'unknown' &&
      data.src_ip !== 'unknown' &&
      data.dst_ip !== 'unknown' &&
      data.protocol !== 'unknown' &&
      data.status !== 'unknown' 
    ) {
      console.log('RealtimeLogtable - Dữ liệu cập nhật:', [data]);
      setInternalLogData((prevData) => {
        const updatedData = [data, ...prevData];
        updatedData.sort((a, b) => parseInt(String(b.id), 16) - parseInt(String(a.id), 16));
        return updatedData;
      });
    }
  }, [data]);

  return (
    <div className="full-screen">
      <h2 className="title">Table capture flow</h2>
      <div className="responsive-table">

        <table className="w-full table-auto border">
          <thead className="sticky">
            <tr>
            {/* <th className="border px-4 py-2">Id</th> */}
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
                {/* <td className="border px-4 py-1">{entry.id}</td> */}
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