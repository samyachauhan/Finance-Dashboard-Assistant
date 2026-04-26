import numpy as np
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import time



def calculate_metrics(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)

    return {
        "MSE": round(mse, 4),
        "RMSE": round(rmse, 4),
        "MAE": round(mae, 4),
        "R2": round(r2, 4)
    }


# Baseline: predict tomorrow = today
def baseline_model(test_df):
    y_true = test_df["Target"].values

    start = time.time()
    y_pred = test_df["Close"].values
    end = time.time()

    return {
        "model": "Baseline",
        "features": ["Close"],
        "alpha": None,
        "metrics": calculate_metrics(y_true, y_pred),
        "predictions": y_pred.tolist(),
        "inference_time": round(end - start, 6)
    }


def train_and_evaluate(model, train_df, test_df, feature_cols, model_name, alpha=None):
    X_train = train_df[feature_cols].values
    y_train = train_df["Target"].values

    X_test = test_df[feature_cols].values
    y_test = test_df["Target"].values

    model.fit(X_train, y_train)
    start = time.time()
    y_pred = model.predict(X_test)
    end = time.time()

    inference_time = end - start

    return {
        "model": model_name,
        "features": feature_cols,
        "alpha": alpha,
        "metrics": calculate_metrics(y_test, y_pred),
        "predictions": y_pred.tolist(),
        "inference_time": round(inference_time, 6)
    }


def run_model_experiments(train_df, test_df):
    results = []

    basic_features = ["Close"]
    advanced_features = [
        "Close",
        "Return",
        "MA_7",
        "MA_20",
        "Volatility_7",
        "High_Low_Range"
    ]

    # v1 baseline
    results.append(baseline_model(test_df))

    # v2 linear regression
    results.append(
        train_and_evaluate(
            LinearRegression(),
            train_df,
            test_df,
            basic_features,
            "Linear Regression: basic features"
        )
    )

    # v3 linear regression with engineered features
    results.append(
        train_and_evaluate(
            LinearRegression(),
            train_df,
            test_df,
            advanced_features,
            "Linear Regression: engineered features"
        )
    )

    # v4 Ridge regularization / tuning
    for alpha in [0.1, 1.0, 10.0]:
        results.append(
            train_and_evaluate(
                Ridge(alpha=alpha),
                train_df,
                test_df,
                advanced_features,
                f"Ridge Regression alpha={alpha}",
                alpha
            )
        )

    # v5 Lasso regularization / tuning
    for alpha in [0.001, 0.01, 0.1]:
        results.append(
            train_and_evaluate(
                Lasso(alpha=alpha, max_iter=10000),
                train_df,
                test_df,
                advanced_features,
                f"Lasso Regression alpha={alpha}",
                alpha
            )
        )

    results = sorted(results, key=lambda x: x["metrics"]["R2"], reverse=True)

    return results


def create_error_analysis(test_df, predictions):
    analysis_df = test_df.copy()
    analysis_df["Prediction"] = predictions
    analysis_df["Error"] = analysis_df["Target"] - analysis_df["Prediction"]
    analysis_df["Absolute_Error"] = abs(analysis_df["Error"])

    worst_errors = analysis_df.sort_values(
        "Absolute_Error",
        ascending=False
    ).head(5)

    return {
        "mean_error": round(analysis_df["Error"].mean(), 4),
        "mean_absolute_error": round(analysis_df["Absolute_Error"].mean(), 4),
        "worst_errors": worst_errors[
            ["Date", "Close", "Target", "Prediction", "Error", "Absolute_Error"]
        ].astype({"Date": str}).to_dict(orient="records")
    }