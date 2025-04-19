// import React from "react";

const SafeAlert = ({ status }: { status: string }) => (

  <>
    <h2 className="title">Safe status</h2>
    <div className="safe-box">
      <div
        className="safe-sub"
        style={{ backgroundColor: (status == "safe" ? "green" : "red") }}
      >
        <p>{status}</p>

      </div>
    </div>
  </>
);

export default SafeAlert;
