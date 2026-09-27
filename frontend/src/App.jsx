
import { useState } from "react";
import "./App.css";

// Production backend on Render.
// VITE_API_URL can override this when deployed.
const API_URL =
  import.meta.env.VITE_API_URL ||
  "https://verbo-backend-velk.onrender.com";

function App() {
  const [topic, setTopic] = useState("");
  const [mode, setMode] = useState("Normal / General");
  const [length, setLength] = useState("Medium");
  const [tone, setTone] = useState("Neutral");
  const [audience, setAudience] = useState("General Public");
  const [complexity, setComplexity] = useState("Intermediate");

  const [result, setResult] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const [history, setHistory] = useState([]);
  const [copied, setCopied] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  // ============================================================
  // GENERATE CONTENT
  // ============================================================

  async function generateContent() {
    if (!topic.trim()) {
      setError("Please enter a topic first.");
      return;
    }

    setLoading(true);
    setError("");
    setResult("");
    setCopied(false);

    try {
      const response = await fetch(`${API_URL}/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic: topic,
          mode: mode,
          length: length,
          tone: tone,
          audience: audience,
          complexity: complexity,
          custom_instructions: "",
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to generate content."
        );
      }

      const generatedContent = data.content;

      setResult(generatedContent);

      const newEntry = {
        id: Date.now(),
        timestamp: new Date().toLocaleString(),
        type: "Generation",
        topic: topic,
        mode: mode,
        length: length,
        tone: tone,
        result: generatedContent,
      };

      setHistory((prev) => [newEntry, ...prev].slice(0, 20));
    } catch (err) {
      console.error("Generation error:", err);

      if (err.name === "TypeError" || err.message === "Failed to fetch") {
        setError(
          "Could not connect to the server. Please try again."
        );
      } else {
        setError(
          err.message || "Something went wrong. Please try again."
        );
      }
    } finally {
      setLoading(false);
    }
  }

  // ============================================================
  // TRANSFORM TEXT
  // ============================================================

  async function transformText() {
    if (!topic.trim()) {
      setError("Please enter text before transforming.");
      return;
    }

    setLoading(true);
    setError("");
    setResult("");
    setCopied(false);

    try {
      const response = await fetch(`${API_URL}/transform`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          text: topic,
          transform_type: mode,
          target_tone: tone,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to transform text."
        );
      }

      const transformedContent = data.result;

      setResult(transformedContent);

      const newEntry = {
        id: Date.now(),
        timestamp: new Date().toLocaleString(),
        type: "Transformation",
        topic: topic,
        mode: mode,
        length: length,
        tone: tone,
        result: transformedContent,
      };

      setHistory((prev) => [newEntry, ...prev].slice(0, 20));
    } catch (err) {
      console.error("Transformation error:", err);

      if (err.name === "TypeError" || err.message === "Failed to fetch") {
        setError(
          "Could not connect to the server. Please try again."
        );
      } else {
        setError(
          err.message || "Something went wrong. Please try again."
        );
      }
    } finally {
      setLoading(false);
    }
  }

  // ============================================================
  // COPY
  // ============================================================

  async function handleCopy() {
    if (!result) return;

    try {
      await navigator.clipboard.writeText(result);
      setCopied(true);

      setTimeout(() => {
        setCopied(false);
      }, 1500);
    } catch (err) {
      console.error("Copy error:", err);
      setError("Could not copy the content.");
    }
  }

  // ============================================================
  // DOWNLOAD
  // ============================================================

  function handleDownload() {
    if (!result) return;

    const blob = new Blob([result], {
      type: "text/plain",
    });

    const url = URL.createObjectURL(blob);

    const link = document.createElement("a");
    link.href = url;
    link.download = "verbo-output.txt";

    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    URL.revokeObjectURL(url);
  }

  // ============================================================
  // HISTORY
  // ============================================================

  function loadHistory(entry) {
    setResult(entry.result);
    setError("");
    setCopied(false);
  }

  function clearHistory() {
    setHistory([]);
  }

  // ============================================================
  // UI
  // ============================================================

  return (
    <div className={`app ${darkMode ? "dark" : ""}`}>

      {/* HEADER */}
      <header className="header">

        <div className="header-left">
          <div className="logo">Verbo</div>

          <p>AI Text Generation Studio</p>
        </div>

        <button
          type="button"
          className="theme-button"
          onClick={() => setDarkMode(!darkMode)}
        >
          {darkMode ? "☀ Light" : "🌙 Dark"}
        </button>

      </header>

      {/* MAIN */}
      <main className="container">

        {/* HERO */}
        <section className="hero">

          <h1>Create better content with AI</h1>

          <p>
            Generate research, professional, creative,
            and everyday content with the right structure,
            tone, and length.
          </p>

        </section>

        {/* WORKSPACE */}
        <section className="workspace">

          {/* LEFT PANEL */}
          <div className="panel">

            <h2>What do you want to write?</h2>

            <label>Topic or instructions</label>

            <textarea
              value={topic}
              onChange={(e) => {
                setTopic(e.target.value);
                setError("");
              }}
              placeholder="Example: Impact of Artificial Intelligence on Education"
            />

            {/* SETTINGS */}
            <div className="settings">

              <div>
                <label>Mode</label>

                <select
                  value={mode}
                  onChange={(e) => setMode(e.target.value)}
                >
                  <option>Normal / General</option>
                  <option>Detailed Explanation</option>
                  <option>Summary</option>
                  <option>Research Article</option>
                  <option>Literature Review</option>
                  <option>Abstract</option>
                  <option>Professional Email</option>
                  <option>Resume Content</option>
                  <option>LinkedIn Post</option>
                  <option>Story</option>
                  <option>Blog</option>
                  <option>Social Media Caption</option>
                </select>
              </div>

              <div>
                <label>Length</label>

                <select
                  value={length}
                  onChange={(e) => setLength(e.target.value)}
                >
                  <option>Very Short</option>
                  <option>Short</option>
                  <option>Medium</option>
                  <option>Long</option>
                  <option>Very Long</option>
                </select>
              </div>

              <div>
                <label>Tone</label>

                <select
                  value={tone}
                  onChange={(e) => setTone(e.target.value)}
                >
                  <option>Neutral</option>
                  <option>Professional</option>
                  <option>Academic</option>
                  <option>Friendly</option>
                  <option>Persuasive</option>
                  <option>Casual</option>
                  <option>Creative</option>
                </select>
              </div>

              <div>
                <label>Audience</label>

                <select
                  value={audience}
                  onChange={(e) => setAudience(e.target.value)}
                >
                  <option>General Public</option>
                  <option>School Student</option>
                  <option>College Student</option>
                  <option>Professional</option>
                  <option>Researcher</option>
                  <option>Customer</option>
                </select>
              </div>

              <div>
                <label>Complexity</label>

                <select
                  value={complexity}
                  onChange={(e) => setComplexity(e.target.value)}
                >
                  <option>Beginner</option>
                  <option>Intermediate</option>
                  <option>Advanced</option>
                </select>
              </div>

            </div>

            {/* GENERATE */}
            <button
              type="button"
              className="generate-button"
              onClick={generateContent}
              disabled={loading || !topic.trim()}
            >
              {loading ? "Generating..." : "Generate Content"}
            </button>

            {/* TRANSFORM */}
            <button
              type="button"
              className="transform-button"
              onClick={transformText}
              disabled={loading || !topic.trim()}
            >
              {loading ? "Processing..." : "Transform Text"}
            </button>

            {/* ERROR */}
            {error && (
              <div className="error-message">
                {error}
              </div>
            )}

          </div>

          {/* RIGHT PANEL */}
          <div className="panel output-panel">

            <div className="output-header">

              <h2>Generated Content</h2>

              <span>AI Output</span>

            </div>

            {/* ACTION BUTTONS */}
            {result && !loading && (
              <div className="output-actions">

                <button
                  type="button"
                  onClick={handleCopy}
                >
                  {copied ? "Copied!" : "Copy"}
                </button>

                <button
                  type="button"
                  onClick={handleDownload}
                >
                  Download TXT
                </button>

              </div>
            )}

            {/* LOADING */}
            {loading && (
              <div className="empty-output">

                <div className="empty-icon spinning">
                  ✦
                </div>

                <h3>
                  Generating your content...
                </h3>

                <p>
                  Please wait while Gemini creates your response.
                </p>

              </div>
            )}

            {/* RESULT */}
            {!loading && result && (
              <div className="result">
                {result}
              </div>
            )}

            {/* EMPTY */}
            {!loading && !result && !error && (
              <div className="empty-output">

                <div className="empty-icon">
                  ✦
                </div>

                <h3>
                  Your content will appear here
                </h3>

                <p>
                  Enter a topic, choose your settings,
                  and click Generate Content.
                </p>

              </div>
            )}

          </div>

        </section>

        {/* HISTORY */}
        <section className="history-section">

          <div className="history-header">

            <div>
              <h2>Recent History</h2>

              <p>
                Your latest generations and transformations
              </p>
            </div>

            {history.length > 0 && (
              <button
                type="button"
                className="clear-history-button"
                onClick={clearHistory}
              >
                Clear History
              </button>
            )}

          </div>

          {history.length === 0 ? (

            <div className="history-empty">
              No generations yet. Your recent results will appear here.
            </div>

          ) : (

            <div className="history-list">

              {history.map((entry) => (

                <div
                  key={entry.id}
                  className="history-item"
                  onClick={() => loadHistory(entry)}
                >

                  <div className="history-item-top">

                    <strong>
                      {entry.type}
                    </strong>

                    <span>
                      {entry.timestamp}
                    </span>

                  </div>

                  <p>
                    {entry.topic.length > 80
                      ? `${entry.topic.slice(0, 80)}...`
                      : entry.topic}
                  </p>

                  <span>
                    {entry.mode}
                  </span>

                </div>

              ))}

            </div>

          )}

        </section>

      </main>

    </div>
  );
}

export default App;

