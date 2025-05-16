// import React from "react";
import { useEffect, useState } from "react";

interface Secure {
  id: string;
  current_status: string;
}

const SafeAlert = ({ status }: { status: Secure }) => {
  const [currentStatus, setCurrentStatus] = useState<string | undefined>()
  useEffect(() => {
    console.log(status)
    if (Array.isArray(status)) {
      if (status.length > 0) {
        console.log(status[status.length-1].current_status)
        setCurrentStatus(status[status.length-1].current_status)
      }
    } else {
      setCurrentStatus(status.current_status)
    }
  }, [status]);
  
  const statusColor = currentStatus === "safe" ? "green" : "red";

  return (
    <>
      <h2 className="title">Status</h2>
      <div className="safe-box">
        <div
          className="safe-sub"
          style={{ backgroundColor: statusColor}}
        >
          <p>{currentStatus}</p>
        </div>
      </div>
    </>
  );
};

export default SafeAlert;
