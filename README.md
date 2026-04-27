# What it Does
This project aims to answer the question: Can machine learning models accurately predict short-term stock price movements and provide meaningful investment recommendations? To address this, the application builds an end-to-end system that collects historical stock data, applies multiple machine learning models, evaluates their predictive performance, and translates results into a simple “Buy” or “Not Buy” decision. By combining quantitative metrics with volatility analysis and AI-generated explanations, the project bridges the gap between raw financial data and user-friendly investment insights. This project addresses the real-world problem of predicting stock price movements, a central challenge in quantitative finance and algorithmic trading. Accurate short-term forecasting is valuable for investors and financial analysts, but is difficult due to market volatility and noise. This work is closely related to widely studied problems in financial machine learning and is similar to tasks explored in platforms like Kaggle, where competitions focus on time-series forecasting and stock prediction. By applying regression models, feature engineering, and evaluation techniques commonly used in these settings, this project demonstrates how machine learning can be used to extract patterns from financial data and support investment decision-making.


# Quick Start
1. Clone Repository
2. Backend Setup
- Go into the backend folder
- Create and activate a virtual environment
- Install dependencies from requirements.txt
- (Optional) Create a .env file and add your OpenAI API key to enable AI explanations
- Note: If you don’t have an API key, the app will still work for stock predictions and the dashboard. You can refer to the demo video to see the AI explanation feature.
3. Run the backend server with python app.py
4. Frontend Setup 
- Go into the frontend folder
- Install dependencies
- Start the React app with npm start
5. Open your browser and go to http://localhost:3000 to use the application

## HOW TO USE:
1. Enter a stock ticker (e.g., AAPL) in the input box.
2. Click “Get Stock Data” to load and preprocess historical stock data.
3. Click “Run ML Experiments” to train and evaluate models.
4. Click “Generate AI Explanation” (if API key is set) to produce a natural language explanation of the results



# Video Links
Project Demo: https://drive.google.com/file/d/1VZkKQxt0icGlHIcstatOrJcc2dEU-LLY/view?usp=share_link
Technical WalkThrough: https://drive.google.com/file/d/1s9Tm3rV_sYX75PsWzPvqrf9oOD6-EFgY/view?usp=share_link 


# Evaluation
The system was evaluated across multiple stocks using several machine learning models and quantitative metrics. Because stock behavior varies over time, results differ depending on the selected ticker; however, consistent performance trends were observed.

## Models Tested:
Linear Regression
Ridge Regression
Lasso Regression
Baseline model (predict next day price = current price)

## Metrics Used:
R² (Coefficient of Determination)
MAE (Mean Absolute Error)
RMSE (Root Mean Squared Error)
Example Results (AAPL)
Best Model: Linear Regression with engineered features
R²: ~0.99
MAE: ~2.33
RMSE: ~3.34

## Key Observations:
- Linear Regression with engineered features consistently performed best across most stocks
- Ridge and Lasso models performed similarly but slightly worse due to regularization
- The baseline model performed significantly worse, confirming that the ML models learned meaningful patterns
- Model accuracy was highest on stable, trending stocks and decreased during periods of high volatility

## Additional Evaluation:
- Conducted controlled experiments comparing multiple models on the same dataset
- Used time-based train/validation/test split to simulate real-world prediction scenarios
- Measured inference time for each model (all models had low latency)

## Qualitative Results:
The “Should You Buy?” recommendation aligns with model performance and volatility trends
AI-generated explanations improved interpretability and user understanding of predictions
The dashboard interface allows users to easily compare models and explore results



# Individual Contributions
This was a solo project I (Samya Chauhan) completed.