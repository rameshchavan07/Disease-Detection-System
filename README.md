<<<<<<< HEAD

=======
# 🩺 MedDetect AI - Advanced Intelligent Health Companion

![MedDetect AI Banner](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Groq](https://img.shields.io/badge/AI_Powered-Groq-f55036?style=for-the-badge)

MedDetect AI is a state-of-the-art, multi-modal web application built entirely on Python and Streamlit. It modernizes clinical symptom checking by merging traditional ML with extremely fast Generative AI capabilities. Features include voice-to-text symptom parsing, diagnostic probability using Random Forests, dynamic geolocation of real-world doctors, and clinic-grade PDF generation.

---

## 🌟 Core Features

- **🗣️ "Dr. Docyote" Voice Interface:** Fully hands-free symptom checking utilizing **Groq Whisper** to instantly transcribe spoken descriptions with lightning speed and supreme accuracy.
- **🧠 Generative NLP Extraction:** Converts messy, natural-language human complaints into structured medical symptom matrices instantly.
- **📊 Scikit-Learn Random Forest Diagnostic Engine:** A trained Decision Tree array resolving highly accurate multi-class predictions loaded into a cached, instant-prediction memory engine (`@st.cache_resource`).
- **📍 Real-Time Medical Geo-Locator:** Dynamically utilizes IP tracing and **Llama 3 AI** to pinpoint real-world recommended specialists, clinics, and phone numbers directly injected into the results map.
- **📄 Clinic-Grade PDF Documentation:** Generates robust, printable Medical Reports (`FPDF2`). Highlighted dynamic warning severities and interactive Google Maps links natively embedded inside the PDF format.
- **🔐 True Serverless Authentication & Memory:** Backed exclusively by **Supabase**. Implements native JWT magic email & passwordless Google Auth perfectly persisted across sessions and tabs. All results are structurally stored in `postgres` for permanent historical lookup.
- **🤖 Omnipresent AI Assistant:** A custom-engineered Glassmorphism iFrame widget natively injected into the Streamlit DOM tree to provide persistent "Dr. Docyote" chat navigation natively on all pages.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| **Frontend UI/UX** | Streamlit, Custom CSS Injection (Glassmorphism design) |
| **Authentication/DB**| Supabase (Auth & Postgres via REST) |
| **Voice Processing** | `audio-recorder-streamlit`, Groq `whisper-large-v3` |
| **Generative AI** | Groq (`llama-3.3-70b-versatile`), Google Gemini Flash |
| **Machine Learning** | Scikit-Learn (`joblib`, Random Forest), Pandas, Numpy |
| **Document Generator**| `fpdf2` |
| **Environment** | Python 3.10+ |

---

## ⚙️ Environment Configuration

MedDetect relies on `.env` variables to perform Cloud interactions. Create a `.env` file in the root of your directory with the following keys:

```env
# Supabase Configuration
SUPABASE_URL="https://YOUR-URL.supabase.co"
SUPABASE_KEY="YOUR-ANON-PUBLIC-KEY"

# AI Provider Keys
GROQ_API_KEY="gsk_..."
GEMINI_API_KEY="AIza..."
```

---

## 🚀 Installation & Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MedDetect-AI.git
   cd MedDetect-AI
   ```

2. **Establish a Virtual Environment**
   ```bash
   python -m venv .venv
   # Windows Activation:
   .venv\Scripts\activate
   # Mac/Linux Activation:
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Boot the Streamlit Server**
   ```bash
   streamlit run app.py
   ```
   *The application will launch on `http://localhost:8501`.*

---

## 💾 Database Specifics (Supabase)

To properly operate this locally, your Supabase project must be configured with a native table matching this schema:

**Table Name:** `predictions`
| Column Name | Type | Description |
|---|---|---|
| `id` | `uuid` | Primary Key, auto-generated |
| `created_at` | `timestampz` | Defaults to `now()` |
| `user_id` | `uuid` | Maps to the Supabase authenticated User ID |
| `symptoms` | `json` / `text` | Array string of symptoms mapped during the session |
| `predicted_disease` | `text` | The \#1 ranked Scikit-Learn prediction |
| `confidence` | `numeric` | Percentage ratio mapping the prediction array |

*Note: You must also disable Row Level Security (RLS) or accurately implement an RLS policy granting auth users `INSERT` and `SELECT` on `predictions` where `user_id = auth.uid()`.*

---

## ☁️ Deployment instructions (Streamlit Community Cloud)

This framework is 100% capable of Serverless PaaS deployment.

1. Ensure `.env` and `.venv/` are listed in your `.gitignore` file.
2. Push your master branch to GitHub.
3. Establish a new app via **Share.Streamlit.io**.
4. Point the main filepath to `app.py`.
5. Enter your raw `.env` contents natively into the **Streamlit Secrets Advanced Options** block before hitting deploy!

---

*Open Sourced & Built dynamically with Advanced LLM Agentic Coding.*
>>>>>>> 513b8a8 (Launch MedDetect AI)
