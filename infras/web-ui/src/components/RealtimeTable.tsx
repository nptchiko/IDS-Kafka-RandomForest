// import React from "react";

import { useEffect, useState } from "react";

interface LogEntry {
  id: string;
  protocol: string;
  status: string;
}

const RealtimeLogTable = ({ log }: { log: LogEntry }) => {
  const [internalLogEntry, setInternalLogEntry] = useState<LogEntry[]>([]);

  useEffect(() => {
    if (log) {
      setInternalLogEntry((prevData) => [...prevData, log]);
      console.log('RealtimeLogtable - Dữ liệu cập nhật:', [...internalLogEntry, log]);
    }
  }, [log]);

  return (
    <div>
      <h2 className="title">This table show log realtime</h2>
      <div className="responsive-table">

        <table className="w-full table-auto border">
          <thead>
            <tr>
              <th className="border px-4 py-2">Protocol</th>
              <th className="border px-4 py-2">Safe/Unsafe</th>
            </tr>
          </thead>
          <tbody>
            {internalLogEntry.map((entry) => (
              <tr key={entry.id}>
                <td className="border px-4 py-1">{entry.protocol}</td>
                <td className="border px-4 py-1">{entry.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}



export default RealtimeLogTable;
