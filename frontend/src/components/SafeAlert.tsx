// import React from "react";

interface Secure {
  id: string;
  status: string
}

const SafeAlert = ({ status }: { status: Secure }) => (

  <>
    <h2 className="title">Safe status</h2>
    <div className="safe-box">
      <div
        className="safe-sub"
        style={{ backgroundColor: (status.status == "safe" ? "green" : "red") }}
      >
        <p>{status.status}</p>

      </div>
    </div>
  </>
);

export default SafeAlert;
