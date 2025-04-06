import React, { useEffect, useRef, useState } from "react";
import "./Overlay.css";

function isCloseEnough(box1, box2, tolerance = 20) {
  return (
    Math.abs(box1.left - box2.left) < tolerance &&
    Math.abs(box1.top - box2.top) < tolerance &&
    Math.abs(box1.width - box2.width) < tolerance &&
    Math.abs(box1.height - box2.height) < tolerance
  );
}

function mergeRegions(oldRegions, newRegions) {
  const now = Date.now();
  const merged = [...oldRegions];

  newRegions.forEach((newBox) => {
    newBox.timestamp = now;
    const exists = merged.some((oldBox) => isCloseEnough(oldBox, newBox));
    if (!exists) {
      merged.push(newBox);
    }
  });

  return merged;
}

function Overlay() {
  const [regions, setRegions] = useState([]);
  const [connected, setConnected] = useState(false);
  const overlayRef = useRef(null);

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8765");

    socket.onopen = () => {
      console.log("[✓] WebSocket connected");
      setConnected(true);
    };

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("[✓] Received regions:", data);

        if (Array.isArray(data)) {
          setRegions((prev) => mergeRegions(prev, data));
        }
      } catch (err) {
        console.error("[x] Error parsing message:", err);
      }
    };

    socket.onclose = () => {
      console.warn("[x] WebSocket disconnected");
      setConnected(false);
    };

    return () => {
      socket.close();
    };
  }, []);

  // Auto-cleanup regions older than 10 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      setRegions((prev) =>
        prev.filter((box) => Date.now() - box.timestamp < 10000)
      );
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="overlay" ref={overlayRef}>
      {connected && <div className="connection-status">Connected</div>}

      {regions.map((region, index) => (
        <div
          key={index}
          className="blur-box"
          style={{
            position: "absolute",
            left: `${region.left-95}px`,
            top: `${region.top-90}px`,
            width: `${region.width+10}px`,
            height: `${region.height+10}px`,
          }}
        />
      ))}
    </div>
  );
}

export default Overlay;
