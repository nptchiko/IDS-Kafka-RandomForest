import { useEffect, useState } from "react";
import "./assets/css/style.css"
import TlsPieChart from "./components/TlsPieChart";
import SafeAlert from "./components/SafeAlert";
import MissedBytesChart from "./components/MissedBytesChart";
import RealtimeTable from "./components/RealtimeTable";
import Socket from "./socket/socket";

// interface RealTimeData {
//   id: number;
//   key: string;
//   value: string;
// }


function App() {
  // const [data, setData] = useState<RealTimeData | null>(null)

  // const [logs, setLogs] = useState<Array<{ protocol: string; status: string }>>([]);

  const [logsData, setLogsData] = useState<{ id: string, protocol: string; status: string }>();
  const [missedBytesData, setMissedBytesData] = useState<{ id: string, time: string; missed_bytes: number }>();
  const [statusInfo, setStatusInfo] = useState<{ id: string, current_status: string } | null>(null);
  const [tlsPieData, setTlsPieData] = useState<{ id: string, name: string; value: number }>();

  useEffect(() => {
    Socket.on('status_data', (payload) => {
      console.log('Received status:', payload.data);

      if (payload && payload.data) {
        payload.data.statusInfo.map((p: any) => {
          setLogsData({ "id": p["_id"], "protocol": p["protocol"], "status": p["current_status"] });
          setMissedBytesData({ "id": p["_id"], "time": p["time"], "missed_bytes": p["current_status"] });
          setStatusInfo({ "id": p["_id"], "current_status": p["current_status"] });
          setTlsPieData({ "id": p["_id"], "name": p["protocol"], "value": p["missed_bytes"] });
        })
      }
    });

    return () => {
      Socket.off('status_data');
    };
  }, []);

  useEffect(() => {
    if (logsData) {
      console.log("✅ Logs đã cập nhật:", logsData);
    }
    if (missedBytesData) {
      console.log("✅ Missed Bytes đã cập nhật:", missedBytesData);
    }
    if (statusInfo) {
      console.log("✅ Status Info đã cập nhật:", statusInfo);
    }
    if (tlsPieData) {
      console.log("✅ Pie Chart Data đã cập nhật:", tlsPieData);
    }
  }, [logsData, missedBytesData, statusInfo, tlsPieData]);

  return (
    <div className="container">
      <div className="row">
        <div className="col box">
          <TlsPieChart pieData={tlsPieData || { id: "defaultId", name: "unknow", value: 0 }} />
        </div>
        <div className="col box flex justify-center items-center">
          <SafeAlert status={statusInfo || { id: 'defaultId', current_status: 'unknown' }} />
        </div>
      </div>
      <div className="row">
        <div className="col box">
          <MissedBytesChart missedBytesData={missedBytesData || { id: 'defaultId', time: 'unknown', missed_bytes: 0 }} />
        </div>
        <div className="col box">
          <RealtimeTable log={logsData || { id: "defaultId", protocol: 'unknown', status: 'unknown' }} />
        </div>
      </div>
    </div>
  );
}

export default App;