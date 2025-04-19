// import React from "react";

type Log = {
  protocol: string;
  status: string;
};

const RealtimeLogTable = ({ logs }: { logs: Log[] }) => (
  <div>
    <h2 className="title">This table show log realtime</h2>
    <table className="w-full table-auto border">
      <thead>
        <tr>
          <th className="border px-4 py-2">Protocol</th>
          <th className="border px-4 py-2">Safe/Unsafe</th>
        </tr>
      </thead>
      <tbody>
        {logs.map((log, index) => (
          <tr key={index}>
            <td className="border px-4 py-1">{log.protocol}</td>
            <td className="border px-4 py-1">{log.status}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </div>
);

export default RealtimeLogTable;
