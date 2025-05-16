import { useEffect, useState } from "react";
import "./assets/css/style.css"
import MissedBytesChart from "./components/MissedBytesChart";
import CaptureFlowTable from "./components/CaptureFlowTable";
import Socket from "./socket/socket";
import SafeAlert from "./components/SafeAlert";


function App() {
  const [safeAlert, setSafeAlert] = useState<{ id: string, current_status: string}>();
  const [missedBytesData, setMissedBytesData] = useState<{ id: string, time: string; missed_bytes: number }>();
  const [flowData, setFlowData] = useState<{id: String, time: String,src_ip: String,dst_ip: String,protocol: String,version: String,status: String}>();

  useEffect(() => {
    Socket.on('status_data', (payload) => {
      console.log('Received status:', payload.data);

      if (payload && payload.data) {
        payload.data.statusInfo.map((p: any) => {
          setSafeAlert({ "id": p["_id"], "current_status": p["current_status"] });
          setMissedBytesData({ "id": p["_id"], "time": p["time"], "missed_bytes": p["missed_bytes"] });
          setFlowData({id: p["_id"],time: p["time"], src_ip: p["id.orig_h"], dst_ip: p["id.resp_h"], protocol: p["proto"], version: p["version"], status: p["current_status"]})
        })
      }
    });

    return () => {
      Socket.off('status_data');
    };
  }, []);

  useEffect(() => {
    if (safeAlert) {
      console.log("✅ Logs đã cập nhật:", safeAlert);
    }
    if (missedBytesData) {
      console.log("✅ Missed Bytes đã cập nhật:", missedBytesData);
    }
    if (flowData) {
      console.log("✅ Table flow cập nhật:", flowData);
    }
  }, [safeAlert, missedBytesData, flowData]);

  return (
    <div className="container">

      <div className="row">
        <div className="col">
          <MissedBytesChart missedBytesData={missedBytesData || { id: 'defaultId', time: 'unknown', missed_bytes: 0 }} />
        </div>
        <div className="col col-3">
          <SafeAlert status={safeAlert || { id: 'defaultId', current_status: 'unknown'}} />
        </div>
      </div>
      <div className="row">
        <CaptureFlowTable data={flowData || {id: "unknown",time: "unknown",src_ip: "unknown",dst_ip: "unknown",protocol: "unknown",version: "unknown",status: "unknown"}} />
      </div>
    </div>
  );
}

export default App;