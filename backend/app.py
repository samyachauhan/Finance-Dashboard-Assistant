from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

client = OpenAI(api_key="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")

from data_pipeline import (
    load_data,
    preprocess_data,
    add_features,
    time_based_split,
    normalize_data
)

from model import (
    run_model_experiments,
    create_error_analysis
)

app = Flask(__name__)
CORS(app)


@app.route("/")
def home():
    return {"message": "Backend is running"}


@app.route("/stock-data", methods=["POST"])
def stock_data():
    try:
        data = request.get_json()
        ticker = data.get("ticker", "").upper().strip()

        if not ticker:
            return jsonify({"error": "Ticker is required."}), 400

        df = load_data(ticker)
        df = preprocess_data(df)
        df = add_features(df)

        train_df, val_df, test_df = time_based_split(df)

        feature_cols = [
            "Close",
            "Return",
            "MA_7",
            "MA_20",
            "Volatility_7",
            "High_Low_Range"
        ]

        train_df, val_df, test_df = normalize_data(
            train_df,
            val_df,
            test_df,
            feature_cols
        )

        results = run_model_experiments(train_df, test_df)
        best_model = results[0]
        r2 = best_model["metrics"]["R2"]
        mae = best_model["metrics"]["MAE"]

        trend_up = df["Close"].iloc[-1] > df["Close"].iloc[-7]

        current_volatility = df["Volatility_7"].iloc[-1]
        average_volatility = df["Volatility_7"].mean()
        high_volatility = current_volatility > average_volatility

        if r2 > 0.6 and trend_up and not high_volatility:
            decision = "BUY"
            reason = "The model is accurate, the stock is trending upward, and volatility is low."
        elif r2 > 0.6 and trend_up and high_volatility:
            decision = "RISKY"
            reason = "The model is accurate and the stock is trending upward, but recent volatility is high."
        elif r2 > 0.6 and not trend_up:
            decision = "HOLD"
            reason = "The model is accurate, but the stock is not trending upward."
        else:
            decision = "RISKY"
            reason = "The model is not reliable enough for a confident recommendation."


        prediction_chart_data = []

        last_10_test = test_df.tail(10).reset_index(drop=True)
        last_10_predictions = best_model["predictions"][-10:]


        for i in range(len(last_10_test)):
            prediction_chart_data.append({
                "Date": str(last_10_test.iloc[i]["Date"]),
                "Actual": float(last_10_test.iloc[i]["Target"]),
                "Predicted": float(last_10_predictions[i])
            })

        chart_data = df.tail(60).copy()
        chart_data["Date"] = chart_data["Date"].astype(str)

        preview = df.tail(5).copy()
        preview["Date"] = preview["Date"].astype(str)

        return jsonify({
            "ticker": ticker,
            "columns": list(df.columns),
            "total_rows": len(df),
            "train_rows": len(train_df),
            "val_rows": len(val_df),
            "test_rows": len(test_df),
            "preview": preview.to_dict(orient="records"),
            "chart_data": chart_data.to_dict(orient="records"),
            "prediction_chart_data": prediction_chart_data,
            "best_model": best_model,
            "model_results": results,
            "recommendation": {
            "decision": decision,
            "reason": reason,
            "r2": r2,
            "mae": mae  
            },
            "volatility": {
                "current": round(float(current_volatility), 4),
                "average": round(float(average_volatility), 4),
                "high_volatility": bool(high_volatility)
            }
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/model-results", methods=["POST"])
def model_results():
    try:
        data = request.get_json()
        ticker = data.get("ticker", "").upper().strip()

        if not ticker:
            return jsonify({"error": "Ticker is required."}), 400

        df = load_data(ticker)
        df = preprocess_data(df)
        df = add_features(df)

        train_df, val_df, test_df = time_based_split(df)

        feature_cols = [
            "Close",
            "Return",
            "MA_7",
            "MA_20",
            "Volatility_7",
            "High_Low_Range"
        ]

        train_df, val_df, test_df = normalize_data(
            train_df,
            val_df,
            test_df,
            feature_cols
        )

        results = run_model_experiments(train_df, test_df)
        best_model = results[0]
        error_analysis = create_error_analysis(
            test_df,
            best_model["predictions"]
        )

        return jsonify({
            "ticker": ticker,
            "total_rows": len(df),
            "train_rows": len(train_df),
            "val_rows": len(val_df),
            "test_rows": len(test_df),
            "results": results,
            "best_model": best_model,
            "error_analysis": error_analysis
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        ticker = data.get("ticker", "").upper().strip()

        if not ticker:
            return jsonify({"error": "Ticker is required."}), 400

        df = load_data(ticker)
        df = preprocess_data(df)
        df = add_features(df)

        train_df, val_df, test_df = time_based_split(df)

        feature_cols = [
            "Close",
            "Return",
            "MA_7",
            "MA_20",
            "Volatility_7",
            "High_Low_Range"
        ]

        train_df, val_df, test_df = normalize_data(
            train_df,
            val_df,
            test_df,
            feature_cols
        )

        results = run_model_experiments(train_df, test_df)
        best_model = results[0]


        return jsonify({
            "ticker": ticker,
            "best_model": best_model["model"],
            "prediction": float(best_model["predictions"][-1]),
            "metrics": best_model["metrics"],
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400



@app.route("/ai-summary", methods=["POST"])
def ai_summary():
    try:
        data = request.get_json()

        ticker = data.get("ticker")
        best_model = data.get("best_model")
        error_analysis = data.get("error_analysis")

        prompts = {
            "Prompt A - Detailed": f"""
            Explain the machine learning results for {ticker} in detail.

            Best model: {best_model}
            Error analysis: {error_analysis}
            """,

            "Prompt B - Beginner Friendly": f"""
            Explain the stock prediction result for a beginner.

            Use 3-5 sentences.
            Avoid very technical language.

            Stock ticker: {ticker}
            Best model: {best_model}
            Error analysis: {error_analysis}
            """,

            "Prompt C - Strict Dashboard": f"""
            Write a simple stock prediction explanation for a beginner.

            Rules:
            - Exactly 3 sentences.
            - No bullet points.
            - No numbered list.
            - No bold text.
            - Avoid technical terms.
            - Mention this is not financial advice.

            Stock ticker: {ticker}
            Best model: {best_model}
            Error analysis: {error_analysis}
            """
        }

        prompt_comparison = []

        for name, prompt in prompts.items():
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You explain ML results clearly for beginner investors."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=150,
                temperature=0.3
            )

            output = response.choices[0].message.content

            prompt_comparison.append({
                "prompt_version": name,
                "output": output,
                "word_count": len(output.split()),
                "chosen_for_final_app": name == "Prompt C - Strict Dashboard"
            })

        return jsonify({
            "summary": prompt_comparison[-1]["output"],
            "prompt_comparison": prompt_comparison
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


    