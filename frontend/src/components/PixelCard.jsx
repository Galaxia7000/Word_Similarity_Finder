import React from "react";

function PixelCard({ children, className = "" }) {
  return (
    <div className={`pixel-card ${className}`}>
      {children}
    </div>
  );
}

export default PixelCard;