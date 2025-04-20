import { useEffect, useState } from "react";
import "./assets/css/style.css"
import TlsPieChart from "./components/TlsPieChart";
import SafeAlert from "./components/SafeAlert";
import MissedBytesChart from "./components/MissedBytesChart";
import RealtimeTable from "./components/RealtimeTable";
import Socket from "./socket/socket";

function App() {
  const [logsData, setLogsData] = useState<Array<{ id: string, protocol: string; status: string }>>([]);
  const [statusInfo, setStatusInfo] = useState<{ id: string, status: string } | null>(null);
  const [missedBytesData, setMissedBytesData] = useState<Array<{ id: string, time: string; missed_bytes: number }>>([]);
  const [tlsPieData, setTlsPieData] = useState<Array<{ id: string, name: string; value: number }>>([]);

  useEffect(() => {
    Socket.on('status_data', (payload) => {
      console.log('Received status data:', payload);

      if (payload && payload.data) {
        setLogsData(payload.data.logsData || []);
        setMissedBytesData(payload.data.missedBytesData.map((item: { timestamp: any; missed_bytes: any; }) => ({ time: item.timestamp, missed: item.missed_bytes })) || []);
        setStatusInfo(payload.data.statusInfo || null);
        setTlsPieData(payload.data.tlsPieData || []);
      }
    });

    return () => {
      Socket.off('connect', () => {console.log("Connect successfully.")});
      Socket.off('disconnect', () => {console.log("Disconnect")});
      Socket.off('connect_error', () => {console.log("Error")});
      Socket.off('status_data');
    };
  }, []);

  // useEffect(() => {
  //   const interval = setInterval(() => {
  //     setLogs((prev) => [
  //       ...prev,
  //       { protocol: "TLS1.2", status: "Safe" },
  //     ]);
  //   }, 5000);
  //   return () => clearInterval(interval);
  // }, []);

  return (
    <div className="container">
      <div className="row">
        <div className="col box">
          <TlsPieChart pieData={tlsPieData} />
        </div>
        <div className="col box flex justify-center items-center">
          <SafeAlert status={statusInfo || { id: 'defaultId', status: 'unknown' }} />
        </div>
      </div>
      <div className="row">
        <div className="col box">
          <MissedBytesChart missedBytesData={missedBytesData} />
        </div>
        <div className="col box">
          <RealtimeTable logs={logsData} />
        </div>
      </div>
    </div>
  );
}

export default App;