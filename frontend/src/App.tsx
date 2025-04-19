import { useEffect, useState } from "react";
import "./assets/css/style.css"
import TlsPieChart from "./components/TlsPieChart";
import SafeAlert from "./components/SafeAlert";
import MissedBytesChart from "./components/MissedBytesChart";
import RealtimeTable from "./components/RealtimeTable";

function App() {
  const [status, setStatus] = useState("");
  const [logs, setLogs] = useState<Array<{ protocol: string; status: string }>>([]);

  useEffect(() => {
    setStatus("safe")
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