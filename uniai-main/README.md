# UniAi 🎓 – AI-Powered University Finder

> Find the best international universities tailored to your course, budget, and preferences — powered by **Google Gemini AI**.

## 🚀 Live Demo
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

---

## 📦 Project Structure
```
uniai-main/
├── streamlit_app.py      ← Main Streamlit app (entry point)
├── requirements.txt      ← Python dependencies
├── .streamlit/
│   ├── config.toml       ← Theme & UI config
│   └── secrets.toml      ← API keys (local only, DO NOT commit)
└── README.md
```

---

## 🔧 Local Setup

### 1. Clone & enter the project
```bash
git clone <your-repo-url>
cd uniai-main
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your Gemini API Key
Edit `.streamlit/secrets.toml`:
```toml
GEMINI_API_KEY = "your_actual_gemini_api_key"
```
> Get a free key at https://aistudio.google.com/app/apikey

### 4. Run locally
```bash
streamlit run streamlit_app.py
```

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this folder to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub
3. Click **New app** → select your repo → set **Main file path** to `streamlit_app.py`
4. Go to **Advanced settings → Secrets** and add:
   ```
   GEMINI_API_KEY = "your_actual_gemini_api_key"
   ```
5. Click **Deploy!** 🎉

---

## ✨ Features
- 🤖 **Gemini AI** recommendations (10 universities per search)
- 🌍 Choose target country, degree type, budget, and field of study
- 💡 Beautiful dark-blue gold premium UI
- 🔗 Direct links to official university websites
- ⚡ Fast & free deployment via Streamlit Cloud