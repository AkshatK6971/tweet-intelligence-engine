# 🚀 Tweet Intelligence Engine

**AI-powered Tweet Generator & Engagement Predictor**  
Generate tweets and predict their popularity using machine learning!

---

## 🌟 Features

- 🎉 **Tweet Generator**: AI-generated tweets using your company name, brand voice, industry, and sentiment target.
- 📊 **Like Predictor**: Predicts expected likes using a **Random Forest Regressor** model.
- ⚡ **Interactive React UI**: Modern, clean web interface for real-time generation and predictions.
- 📡 **REST API** backend with Flask.

---

## 🔗 Live Demo

👉 [**Live Demo Here**](https://tweet-intelligence-engine-kw21.onrender.com/)

---

## 🛠️ Tech Stack

### Frontend

- React.js (Vite)
- Tailwind CSS
- Axios (for HTTP requests)

### Backend

- Python + Flask + Flask-CORS
- REST API endpoints (`/generate` and `/predict`)

### Machine Learning

- **Random Forest Regressor** (trained using scikit-learn)
- Sentiment analysis using TextBlob
- Pretrained model artifacts:
  - `like_predictor.pkl`
  - `le_company.pkl`
  - `le_day.pkl`
  - `le_username.pkl`

---

## 📊 How It Works

1. User submits inputs via the React frontend.
2. React app sends POST requests to the Flask backend:
    - `/generate`: Generates a tweet based on inputs using pre-made templates.
    - `/predict`: Predicts expected likes using Random Forest Regressor.
3. Results are displayed as styled cards with prediction details.

---

## 📦 Project Structure

```bash
tweet-intelligence-engine/
├── backend/
│   ├── api.py
│   ├── like_predictor.pkl
│   ├── le_company.pkl
│   ├── le_day.pkl
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   └── package.json
└── README.md
```

## 🚀 Running Locally

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AkshatK6971/tweet-intelligence-engine
cd tweet-intelligence-engine
```

### 2️⃣ Backend Setup (Flask + ML Model)

```bash
cd backend
pip install -r requirements.txt
python api.py
```

Backend will run at:

```bash
http://localhost:5000
```

---

### 3️⃣ Frontend Setup (React + Vite)

```bash
cd ../frontend
npm install
```

Then update the backend API URL in:

```js
src/App.js
```

Change this line:

```js
const API_BASE = "https://tweet-intelligence-engine-backend.onrender.com";
```

To:

```js
const API_BASE = "http://localhost:5000";
```

After changing the API URL, start the frontend:

```bash
npm run dev
```

Frontend will run at:

```js
http://localhost:5173
```

Now your full system runs locally.
