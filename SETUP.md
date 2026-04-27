# SETUP.md

## Installation and Setup Instructions

This project is an AI Finance Dashboard with a Flask backend and React frontend. It retrieves stock data, runs machine learning models, and optionally uses the OpenAI API to generate AI explanations.

---

## 1. Clone the Repository

git clone https://github.com/samyachauhan/Finance-Dashboard-Assistant
cd Finance-Dashboard-Assistant

---

## 2. Backend Setup

cd backend  

Create a virtual environment:  
python3 -m venv .venv  

Activate it:  
source .venv/bin/activate  

Install dependencies:  
pip install -r requirements.txt  

---

## 3. API Key Setup

This project uses the OpenAI API for AI-generated explanations.

Inside the `backend` folder, create a `.env` file:

touch .env  

Add this line inside the file:

OPENAI_API_KEY=your_openai_api_key_here  

Replace `your_openai_api_key_here` with your own OpenAI API key.

- The API key is NOT included in the repository for security reasons.
- If no API key is provided, the rest of the app (stock data, ML models, charts, recommendations) will still work.
- To test without a key, simply run the app and use the stock dashboard features.

Please refer back to the demo video to see how the app works with successful API integration.

---

## 4. Run the Backend

From the backend folder:

python app.py  

The backend will run at:  
http://127.0.0.1:5000  

---

## 5. Frontend Setup

Open a new terminal.

From the main project folder:

npm install  
npm start  

The frontend will run at:  
http://localhost:3000  

---

## 6. How to Use the App

1. Open http://localhost:3000  
2. Enter a stock ticker (e.g., AAPL, MSFT, TSLA)  
3. Click the button to fetch data  
4. View:
   - Stock data preview  
   - Model predictions  
   - Evaluation metrics (R², MAE, etc.)  
   - Charts  
   - Buy / Hold / Sell recommendation  
5. If an API key is added, an AI explanation will also appear  

---

## 7. External APIs and Tools Used

- yfinance (Yahoo Finance data)
- OpenAI API (AI explanations)
- Flask (backend)
- React (frontend)
- scikit-learn (machine learning models)

---

## 8. Troubleshooting

Backend not running:
- Make sure virtual environment is activated  
- Run: pip install -r requirements.txt  

Frontend not running:
- Make sure you are in the folder with package.json  
- Run: npm install then npm start  

AI explanation not working:
- Ensure backend/.env exists  
- Ensure it contains:
  OPENAI_API_KEY=your_openai_api_key_here  

If no API key is provided, the rest of the project can still be fully tested.