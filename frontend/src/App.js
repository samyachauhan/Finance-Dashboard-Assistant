import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  ResponsiveContainer,
  Legend
} from "recharts";

import { useState } from "react";
import "./App.css";

function App() {
  const [ticker, setTicker] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [aiSummary, setAiSummary] = useState("");
  const [promptComparison, setPromptComparison] = useState([]);

  const fetchStockData = async () => {
    setError("");
    setResult(null);
    setAiSummary("");

    try {
      const res = await fetch("http://127.0.0.1:5000/stock-data", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to connect to backend");
    }
  };

  const fetchModelResults = async () => {
    setError("");
    setResult(null);
    setAiSummary("");

    try {
      const res = await fetch("http://127.0.0.1:5000/model-results", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ticker }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setResult(data);
    } catch (err) {
      setError(err.message || "Failed to connect to backend");
    }
  };

  const fetchAISummary = async () => {
    setError("");

    try {
      const res = await fetch("http://127.0.0.1:5000/ai-summary", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: result.ticker,
          best_model: result.best_model,
          error_analysis: result.error_analysis,
        }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || "Something went wrong");
      }

      setAiSummary(data.summary);
      setPromptComparison(data.prompt_comparison);
    } catch (err) {
      setError(err.message || "Failed to connect to backend");
    }
  };

  return (
    <div className="container">
      <h1>Samya's Finance Assistant</h1>

      <div className="search-card">
        <input
          type="text"
          placeholder="Enter stock ticker, ex: AAPL"
          value={ticker}
          onChange={(e) => setTicker(e.target.value)}
        />

        <button onClick={fetchStockData}>Get Stock Data</button>
        <button onClick={fetchModelResults}>Run ML Experiments</button>
      </div>

      {error && <p className="error">{error}</p>}

      {result && (
        <div className="section">
          {result.recommendation && (
            <div className="card highlight-card">
              <h3>Should You Buy?</h3>

              <h2
                style={{
                  color:
                    result.recommendation.decision === "BUY"
                      ? "green"
                      : result.recommendation.decision === "HOLD"
                      ? "orange"
                      : "red",
                }}
              >
                {result.recommendation.decision}
              </h2>

              <p>{result.recommendation.reason}</p>

              <p>R²: {result.recommendation.r2}</p>
              <p>MAE: {result.recommendation.mae}</p>
            </div>
          )}
          <div className="card">
            <h2>{result.ticker}</h2>

            <div className="stats-grid">
              <div className="stat-box">
                <h4>Total Rows</h4>
                <p>{result.total_rows}</p>
              </div>

              <div className="stat-box">
                <h4>Train Rows</h4>
                <p>{result.train_rows}</p>
              </div>

              {result.val_rows !== undefined && (
                <div className="stat-box">
                  <h4>Validation Rows</h4>
                  <p>{result.val_rows}</p>
                </div>
              )}

              <div className="stat-box">
                <h4>Test Rows</h4>
                <p>{result.test_rows}</p>
              </div>

              {result.volatility && (
                <>
                  <div className="stat-box">
                    <h4>Current Volatility</h4>
                    <p
                      style={{
                        color: result.volatility.high_volatility ? "red" : "green",
                      }}
                    >
                      {result.volatility.current}
                    </p>
                  </div>

                  <div className="stat-box">
                    <h4>Average Volatility</h4>
                    <p>{result.volatility.average}</p>
                  </div>
                </>
              )}
            </div>

          </div>

          {result.columns && (
            <div className="card">
              <h3>Features Used</h3>

              <div className="tag-grid">
                {result.columns.map((col, index) => (
                  <span key={index} className="tag">
                    {col}
                  </span>
                ))}
              </div>
            </div>
          )}

          {result.preview && (
            <div className="card">

              <h3>Stock Price Chart</h3>

              <div className="chart-box">
                <ResponsiveContainer width="100%" height={300}>
                  <LineChart data={result.chart_data}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="Date" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="Close" />
                  </LineChart>
                </ResponsiveContainer>
              </div>

              {result.prediction_chart_data && (
                <>
                  <h3>Predicted vs Actual Stock Price</h3>

                  <div className="chart-box">
                    <ResponsiveContainer width="100%" height={300}>

                      <LineChart data={result.prediction_chart_data}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="Date" />
                        <YAxis />
                        <Tooltip />
                        <Legend />

                        <Line
                          type="monotone"
                          dataKey="Actual"
                          name="Actual Price"
                          stroke="#2563eb"
                          strokeWidth={3}
                          dot={{ r: 4 }}
                        />

                        <Line
                          type="monotone"
                          dataKey="Predicted"
                          name="Predicted Price"
                          stroke="#ef4444"
                          strokeWidth={3}
                          dot={{ r: 4 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </>
              )}

              <h3>Preview Last 5 Rows</h3>

              <div className="table-wrapper">
                <table>
                  <thead>
                    <tr>
                      {Object.keys(result.preview[0]).map((col) => (
                        <th key={col}>{col}</th>
                      ))}
                    </tr>
                  </thead>

                  <tbody>
                    {result.preview.map((row, i) => (
                      <tr key={i}>
                        {Object.values(row).map((val, j) => (
                          <td key={j}>
                            {typeof val === "number" ? val.toFixed(4) : val}
                          </td>
                        ))}
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

            </div>
          )}

          {result.results && (
            <>
              <div className="card">
                <h3>Model Comparison</h3>

                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Model</th>
                        <th>Alpha</th>
                        <th>MSE</th>
                        <th>RMSE</th>
                        <th>MAE</th>
                        <th>R²</th>
                        <th>Inference Time</th>
                      </tr>
                    </thead>

                    <tbody>
                      {result.results.map((model, index) => (
                        <tr
                          key={index}
                          className={
                            model.model === result.best_model.model
                              ? "best-row"
                              : ""
                          }
                        >
                          <td>{model.model}</td>
                          <td>{model.alpha ?? "N/A"}</td>
                          <td>{model.metrics.MSE}</td>
                          <td>{model.metrics.RMSE}</td>
                          <td>{model.metrics.MAE}</td>
                          <td>{model.metrics.R2}</td>
                          <td>{model.inference_time}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              <div className="card highlight-card">
                <h3>Best Model</h3>
                <p>{result.best_model.model}</p>
              </div>

              <div className="card">
                <h3>Error Analysis</h3>

                <div className="stats-grid">
                  <div className="stat-box">
                    <h4>Mean Error</h4>
                    <p>{result.error_analysis.mean_error}</p>
                  </div>

                  <div className="stat-box">
                    <h4>Mean Absolute Error</h4>
                    <p>{result.error_analysis.mean_absolute_error}</p>
                  </div>
                </div>

                <h4>Worst Prediction Errors</h4>

                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Date</th>
                        <th>Close</th>
                        <th>Actual Target</th>
                        <th>Prediction</th>
                        <th>Error</th>
                        <th>Absolute Error</th>
                      </tr>
                    </thead>

                    <tbody>
                      {result.error_analysis.worst_errors.map((row, index) => (
                        <tr key={index}>
                          <td>{row.Date}</td>
                          <td>{Number(row.Close).toFixed(2)}</td>
                          <td>{Number(row.Target).toFixed(2)}</td>
                          <td>{Number(row.Prediction).toFixed(2)}</td>
                          <td>{Number(row.Error).toFixed(2)}</td>
                          <td>{Number(row.Absolute_Error).toFixed(2)}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <button className="ai-button" onClick={fetchAISummary}>
                  Generate AI Explanation
                </button>

                {aiSummary && (
                  <div className="ai-box">
                    <h3>AI Explanation</h3>
                    <p>{aiSummary}</p>
                  </div>
                )}
                {promptComparison.length > 0 && (
                  <div className="card">
                    <h3>Prompt Engineering Comparison</h3>

                    <div className="table-wrapper">
                      <table>
                        <thead>
                          <tr>
                            <th>Prompt</th>
                            <th>Word Count</th>
                            <th>Chosen?</th>
                            <th>Output</th>
                          </tr>
                        </thead>

                        <tbody>
                          {promptComparison.map((row, index) => (
                            <tr key={index}>
                              <td>{row.prompt_version}</td>
                              <td>{row.word_count}</td>
                              <td>{row.chosen_for_final_app ? "Yes" : "No"}</td>
                              <td>{row.output}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  </div>
                )}




              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
}

export default App;