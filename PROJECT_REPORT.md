# MedDetect AI (v2.0.0) - Technical Report

MedDetect AI is a state-of-the-art, AI-powered multi-disease detection system designed to assist users in identifying potential health conditions based on symptoms. It combines machine learning for diagnosis, generative AI for empathetic interaction, and a premium "Glassmorphism" user interface for an elite user experience.

---

## 🚀 How It Works (Core Workflows)

### 1. Secure Authentication & User Profiling
- **Onboarding**: Users sign in via **Supabase Auth** (supporting Email/Password and Google OAuth).
- **History Tracking**: All previous predictions are securely stored in a **PostgreSQL** database, allowing users to track their health trends over time via the **Report History** page.
v
### 2. Intelligent Symptom Extraction
- **Multimodal Input**: Users can type symptoms, select them from an exhaustive list of 382+ options, or speak directly to the AI.
- **Voice-to-Text**: **Groq Whisper (large-v3)** provides near-instant transcription of patient descriptions.
- **Translation Engine**: A rotation pool of **Google Gemini 2.0 Flash** keys translates non-English (including Hindi/Hinglish) descriptions into clinical English.
- **NLP Logic**: Custom logic in `nlp_extractor.py` handles:
    - **Synonym Mapping**: (e.g., "tummy ache" → `stomach_pain`).
    - **Negation Detection**: Correctly ignores symptoms like "I do **not** have a cough".

### 3. Machine Learning Diagnosis
- **The Brain**: A **Random Forest Classifier** trained on 9,400+ medical samples for 221+ unique diseases.
- **Inference**: The model processes the extracted symptom vector and returns top predictions with confidence scores.
- **Severity Analysis**: Every prediction is cross-referenced with a severity database to categorize risk (Low, Moderate, High, or **Critical**).

### 4. Professional Reporting & Tele-health
- **Dynamic PDF Generation**: The `pdf_generator.py` uses the **FPDF** library to create custom clinical reports including patient details, predictions, and precautions.
- **SMTP Emailing**: Reports are automatically emailed to the user using **SMTPlib**.
- **Doctor Locator**: Uses IP-geolocation and **Groq/Llama-3** to find the nearest real-world specialists for the predicted condition.
- **Emergency Consults**: If high-risk conditions are detected, the app generates a direct **Jitsi Meet** link for instant video consultation.

---

## 🛠️ Technology Stack

### Core Technologies
- **Python (3.x)**: Primary backend and logic language.
- **Streamlit**: Modern web framework for data applications.
- **JavaScript/CSS**: Used for the premium "Glassmorphism" UI and the "Dr. Docyote" floating chatbot injection.

### AI & Machine Learning
- **Scikit-Learn**: Powering the Random Forest disease classification engine.
- **Joblib**: Used for high-efficiency model serialization and loading.
- **Google Gemini (2.0-Flash)**: Primary NLP engine for translation and symptom extraction.
- **Groq (Llama-3 & Whisper)**: Lightning-fast fallback LLM and voice transcription.

### Backend & Cloud
- **Supabase**: Handles PostgreSQL database management and user authentication.
- **Jitsi Meet API**: Provides open-source, secure video conferencing for health consultations.

### Document Processing
- **FPDF2**: Modern PDF generation for clinical reports.
- **SMTPlib/EmailMessage**: Standard Python library for reliable medical report mailing.

---

## 📂 File-by-File Breakdown

### 🎯 Root Directory
- [`app.py`](file:///d:/DSP/app.py): The main entry point. Orchestrates the layout, premium design system (CSS), and home page dashboard.
- `requirements.txt`: Defines all Python dependencies (Streamlit, Scikit-learn, Supabase, etc.).
- `.env`: (User Managed) Stores sensitive API keys for Gemini, Groq, and Supabase.
- `google_credentials.json`: Configuration for Google service integrations.

### ⚙️ `modules/` (The Core Logic)
- [`ml_engine.py`](file:///d:/DSP/modules/ml_engine.py): Loads the trained joblib model and performs disease prediction inference.
- [`nlp_extractor.py`](file:///d:/DSP/modules/nlp_extractor.py): The NLP powerhouse. Handles translation, synonym mapping, and negation logic.
- [`floating_chat.py`](file:///d:/DSP/modules/floating_chat.py): "Dr. Docyote" chatbot. Injects a persistent floating widget into the Streamlit UI using direct DOM manipulation.
- [`database.py`](file:///d:/DSP/modules/database.py): Supabase client wrapper with custom retry decorators for robust cloud connectivity.
- [`pdf_generator.py`](file:///d:/DSP/modules/pdf_generator.py): Class-based FPDF generator for professional medical reports.
- [`email_service.py`](file:///d:/DSP/modules/email_service.py): Service for sending report emails and appointment confirmations via SMTP.
- [`doctor_locator.py`](file:///d:/DSP/modules/doctor_locator.py): Geolocation-based specialist finder using Groq Llama-3.
- [`shared_ui.py`](file:///d:/DSP/modules/shared_ui.py): Reusable UI components and the premium "Glassmorphism" CSS injection.
- [`disease_info.py`](file:///d:/DSP/modules/disease_info.py): Comprehensive metadata (specialists, remedies, precautions) for every disease.

### 📄 `pages/` (Streamlit Interface)
- [`0_🔑_Sign_In.py`](file:///d:/DSP/pages/0_🔑_Sign_In.py): Secure login/signup portal via Supabase.
- [`1_🔍_Symptom_Checker.py`](file:///d:/DSP/pages/1_🔍_Symptom_Checker.py): The primary tool. Integrates voice/text input, ML prediction, and PDF downloading.
- [`2_📊_Report_History.py`](file:///d:/DSP/pages/2_📊_Report_History.py): Displays a user's chronological diagnosis history fetched from the database.
- [`3_👨‍⚕️_Book_Appointment.py`](file:///d:/DSP/pages/3_👨‍⚕️_Book_Appointment.py): Clinic booking portal with dynamic specialist discovery.

### 🧪 Other Directories
- `models/`: Stores the `.pkl` binary files and metadata. Includes `train_model.py` for training the classifier from scratch.
- `data/`: Contains the primary medical datasets (`dataset.csv`).
- `logs/`: Real-time application event logging for debugging and audit trails.
- `scripts/`: Internal utilities for data generation and notebook creation.
- `tests/`: Unit testing suite ensuring the reliability of ML and NLP pipelines.

---

## 🛠️ Setup & Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment (`.env`)**:
   Add following keys:
   - `GEMINI_API_KEYS`: (Comma separated list for rotation)
   - `GROQ_API_KEY`: (For Voice & Fallback NLP)
   - `SUPABASE_URL` / `SUPABASE_KEY`: (For Auth & History)
   - `SMTP_USER` / `SMTP_PASSWORD`: (For Emailing)

3. **Run Application**:
   ```bash
   streamlit run app.py
   ```

---

> [!NOTE]
> **Disclaimer**: This system is designed for informational and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment.
