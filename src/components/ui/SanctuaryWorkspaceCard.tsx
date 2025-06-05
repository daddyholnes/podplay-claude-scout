import React from "react";
import { motion } from "framer-motion";

export interface SanctuaryWorkspaceCardProps {
  name: string;
  status: "idle" | "provisioning" | "active" | "error";
  theme?: "sanctuary" | "cyber" | "forest";
  agent?: string;
  stats?: { label: string; value: string }[];
  children?: React.ReactNode;
}

const themeStyles = {
  sanctuary: {
    background:
      "linear-gradient(135deg, rgba(56, 189, 248,0.12) 0%, rgba(139,92,246,0.18) 100%)",
    border: "1.5px solid rgba(139,92,246,0.3)",
    boxShadow: "0 2px 18px #8b5cf633, 0 1.5px 8px #38bdf833",
  },
  cyber: {
    background:
      "linear-gradient(120deg, #23272f 0%, #0fffc3 100%)",
    border: "1.5px solid #0fffc399",
    boxShadow: "0 2px 18px #0fffc344, 0 1.5px 8px #23272f44",
  },
  forest: {
    background:
      "linear-gradient(135deg, #1e3a1e 0%, #b2f5ea 100%)",
    border: "1.5px solid #38b2ac99",
    boxShadow: "0 2px 18px #38b2ac33, 0 1.5px 8px #1e3a1e44",
  },
};

export const SanctuaryWorkspaceCard: React.FC<SanctuaryWorkspaceCardProps> = ({
  name,
  status,
  theme = "sanctuary",
  agent,
  stats = [],
  children,
}) => {
  const style = themeStyles[theme];
  const statusColor =
    status === "active"
      ? "#5f5"
      : status === "provisioning"
      ? "#fa0"
      : status === "error"
      ? "#f55"
      : "#aaa";

  return (
    <motion.div
      initial={{ opacity: 0, y: 40 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      style={{
        ...style,
        borderRadius: 20,
        padding: 28,
        minWidth: 340,
        minHeight: 220,
        position: "relative",
        margin: 8,
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-between",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
        <div
          style={{
            width: 12,
            height: 12,
            borderRadius: "50%",
            background: statusColor,
            boxShadow: status === "active" ? "0 0 8px #5f5" : undefined,
            marginRight: 6,
          }}
        />
        <span style={{ fontWeight: 700, fontSize: 22 }}>{name}</span>
        {agent && (
          <span
            style={{
              marginLeft: 10,
              background: "#23272f88",
              borderRadius: 8,
              padding: "2px 10px",
              fontSize: 13,
              color: "#8b5cf6",
              fontWeight: 600,
              letterSpacing: 0.2,
            }}
          >
            {agent}
          </span>
        )}
      </div>
      <div style={{ color: statusColor, margin: "10px 0 6px 0", fontSize: 15 }}>
        Status: {status}
      </div>
      {stats.length > 0 && (
        <div style={{ display: "flex", gap: 20, marginBottom: 10 }}>
          {stats.map((s) => (
            <div key={s.label} style={{ textAlign: "center" }}>
              <div style={{ fontSize: 20, fontWeight: 700 }}>{s.value}</div>
              <div style={{ fontSize: 12, color: "#8b5cf6" }}>{s.label}</div>
            </div>
          ))}
        </div>
      )}
      <div style={{ flex: 1 }}>{children}</div>
    </motion.div>
  );
};

export default SanctuaryWorkspaceCard;