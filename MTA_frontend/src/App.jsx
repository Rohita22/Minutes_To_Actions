import { useState } from "react";

export default function App() {
  const [title, setTitle] = useState("");
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleGenerate = async () => {
    setError("");
    setLoading(true);
    setResult(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/sessions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, notes }),
      });

      if (!res.ok) throw new Error("Backend error: " + res.status);

      const data = await res.json();
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const kpis = result
    ? [
        { label: "Action Items", value: result.action_items?.length || 0 },
        { label: "Decisions", value: result.decisions?.length || 0 },
        {
          label: "Owners",
          value: new Set((result.action_items || []).map((x) => x.owner)).size,
        },
      ]
    : [];

  return (
    <div style={container}>
      {/* HEADER */}
      <div style={header}>
        <h1 style={titleStyle}>Minutes-to-Actions</h1>
        <p style={subtitle}>Turn Conversations into Actions</p>
      </div>

      {/* MAIN SECTION */}
      <div style={main}>
        {/* LEFT COLUMN */}
        <div style={leftColumn}>
          <div style={card}>
            <h2 style={sectionTitle}>New Session</h2>

            <label style={label}>Meeting Title</label>
            <input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              style={input}
            />

            <label style={{ ...label, marginTop: 20 }}>
              Meeting Notes *
            </label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={16}
              style={textarea}
            />

            <button
              onClick={handleGenerate}
              disabled={loading || notes.trim().length < 20}
              style={button}
            >
              {loading ? "Generating..." : "Generate"}
            </button>

            {error && <p style={errorStyle}>{error}</p>}
          </div>
        </div>

        {/* RIGHT COLUMN */}
        <div style={rightColumn}>
          {!result && (
            <div style={cardCentered}>
              Results will appear here after generating.
            </div>
          )}

          {result && (
            <>
              <div style={kpiRow}>
                {kpis.map((k) => (
                  <div key={k.label} style={kpiCard}>
                    <div style={kpiLabel}>{k.label}</div>
                    <div style={kpiValue}>{k.value}</div>
                  </div>
                ))}
              </div>

              <div style={card}>
                <h2 style={sectionTitle}>Summary</h2>
                <ul>
                  {(result.summary || []).map((s, i) => (
                    <li key={i}>{s}</li>
                  ))}
                </ul>
              </div>

              <div style={card}>
                <h2 style={sectionTitle}>Decisions</h2>
                <ul>
                  {(result.decisions || []).map((d, i) => (
                    <li key={i}>{d}</li>
                  ))}
                </ul>
              </div>
            </>
          )}
        </div>
      </div>

      {result && (
        <div style={{ ...card, margin: "40px 0" }}>
          <h2 style={sectionTitle}>Action Items</h2>
          <table style={table}>
            <thead>
              <tr>
                <th style={th}>Owner</th>
                <th style={th}>Task</th>
                <th style={th}>Due</th>
                <th style={th}>Priority</th>
              </tr>
            </thead>
            <tbody>
              {(result.action_items || []).map((a, i) => (
                <tr key={i}>
                  <td style={td}>{a.owner}</td>
                  <td style={td}>{a.task}</td>
                  <td style={td}>{a.due_date || "—"}</td>
                  <td style={td}>{a.priority}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

/* ===== STYLES ===== */

const container = {
  minHeight: "100vh",
  width: "100%",
  boxSizing: "border-box",
  padding: "40px 60px",
  background: "#0d1117",
  color: "#e6edf3",
  fontFamily: "Inter, sans-serif",
};

const header = {
  marginBottom: 50,
};

const titleStyle = {
  fontSize: 44,
  fontWeight: 800,
  margin: 0,
  background: "linear-gradient(to right, #9ca3af, #ffffff)",
  WebkitBackgroundClip: "text",
  WebkitTextFillColor: "transparent",
};

const subtitle = {
  marginTop: 10,
  color: "#8b949e",
};

const main = {
  display: "grid",
  gridTemplateColumns: "1fr 1fr",
  gap: 50,
  alignItems: "start",
};

const leftColumn = { width: "100%" };
const rightColumn = { width: "100%", display: "flex", flexDirection: "column", gap: 30 };

const card = {
  background: "#161b22",
  border: "1px solid #30363d",
  borderRadius: 18,
  padding: 30,
  width: "100%",
};

const cardCentered = {
  ...card,
  textAlign: "center",
  color: "#6e7681",
};

const sectionTitle = {
  marginBottom: 20,
  fontSize: 18,
};

const label = {
  fontSize: 14,
  color: "#8b949e",
  marginBottom: 8,
  display: "block",
};

const input = {
  width: "100%",
  padding: 14,
  borderRadius: 12,
  border: "1px solid #30363d",
  background: "#0d1117",
  color: "#fff",
};

const textarea = {
  ...input,
  resize: "vertical",
};

const button = {
  marginTop: 20,
  padding: 14,
  borderRadius: 12,
  border: "none",
  background: "linear-gradient(to right, #6366f1, #8b5cf6)",
  color: "#fff",
  fontWeight: 600,
  cursor: "pointer",
  width: "100%",
};

const errorStyle = {
  marginTop: 10,
  color: "#ff6b6b",
};

const kpiRow = {
  display: "grid",
  gridTemplateColumns: "repeat(3, 1fr)",
  gap: 20,
};

const kpiCard = {
  background: "#1c2128",
  border: "1px solid #30363d",
  borderRadius: 16,
  padding: 20,
};

const kpiLabel = { fontSize: 13, color: "#8b949e" };
const kpiValue = { fontSize: 30, fontWeight: 700 };

const table = {
  width: "100%",
  borderCollapse: "collapse",
};

const th = {
  textAlign: "left",
  padding: 14,
  borderBottom: "1px solid #30363d",
  color: "#8b949e",
};

const td = {
  padding: 14,
  borderBottom: "1px solid #21262d",
};
