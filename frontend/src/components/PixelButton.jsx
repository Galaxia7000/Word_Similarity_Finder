import React from "react";

function PixelButton({
  children,
  onClick,
  type = "button",
  className = "",
}) {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`pixel-button ${className}`}
    >
      {children}
    </button>
  );
}

export default PixelButton;