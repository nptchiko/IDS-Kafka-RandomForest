import { useEffect, useState } from "react";
import "./assets/css/style.css"
import TlsPieChart from "./components/TlsPieChart";
import SafeAlert from "./components/SafeAlert";
import MissedBytesChart from "./components/MissedBytesChart";
import RealtimeTable from "./components/RealtimeTable";
import Socket from "./socket/socket";

interface RealTimeData {
  id: number;
  key: string;
  value: string;
}


function App() {
  const [data, setData] = useState<RealTimeData | null>(null)

  const [logs, setLogs] = useState<Array<{ protocol: string; status: string }>>([]);

  useEffect(() => {
    Socket.on('initial_data', (payload) => {
      console.log('📦 Received initial data:', payload);

      if (payload && payload.data) {
        setLogs(payload.data.map((item: any) => ({
          protocol: item.protocol,
          status: item.status
        })));
      }
    })

    return () => {
      Socket.off('initial_data');
    };
  }, [])

  useEffect(() => {
    const interval = setInterval(() => {
      setLogs((prev) => [
        ...prev,
        { protocol: "TLS1.2", status: "Safe" },
      ]);
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    Socket.on('status', (incomingData: RealTimeData) => {
      setData(incomingData);
      console.log(incomingData)
    });

    return () => {
      Socket.off('status')
    }
  }, [])

  return (
    <div className="container">
      <div className="row">
        <div className="col box">
          <TlsPieChart />
        </div>
        <div className="col box flex justify-center items-center">
          <SafeAlert status={status} />
        </div>
      </div>
      <div className="row">
        <div className="col box">
          <MissedBytesChart />
        </div>
        <div className="col box">
          <RealtimeTable logs={logs} />
        </div>
      </div>
    </div>
  );
}

export default App;