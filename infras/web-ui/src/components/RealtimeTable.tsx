// import React from "react";

interface LogEntry {
  id: string;
  protocol: string;
  status: string;
}

interface RealtimeTableProps {
  logs: LogEntry[];
}

const RealtimeLogTable = ({ logs }: RealtimeTableProps) => (
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
          {logs.map((log) => (
            <tr key={log.id}>
              <td className="border px-4 py-1">{log.protocol}</td>
              <td className="border px-4 py-1">{log.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  </div>
);

export default RealtimeLogTable;
