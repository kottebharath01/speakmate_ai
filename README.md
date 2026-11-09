# SpeakMate AI – Your Personal AI English Tutor 🤖💬

**SpeakMate AI** is an intelligent, voice-first English learning web application designed specifically for native Telugu speakers. 

Rather than functioning as a generic chatbot or static course, SpeakMate works as a **personal English tutor**:
- 🗣️ **Explains real-life situations in Telugu (using Telugu script)**.
- 🎯 **Prompts the learner to explain or respond in English without revealing the answer beforehand**.
- 🎙️ **Captures spoken English via the browser's Web Speech API (with an editable transcript and manual typing fallback)**.
- 🧠 **Analyzes grammar, tenses, subject-verb agreement, articles, prepositions, and natural phrasing**.
- 📋 **Delivers structured feedback (Sections A to G)** with native speech synthesis.
- 🔁 **Evaluates repeat sentences to ensure mastery and positive reinforcement**.
- 📈 **Adapts difficulty levels (Beginner, Intermediate, Advanced) dynamically based on multi-session performance**.

---

## 🌟 Key Features

1. **Core Situation-Based Learning**:
   - Everyday situations (Shopping, Dining, Asking Directions, Workplace Leave, API Bugs, Job Interviews).
   - Telugu explanation in Telugu script with optional phonetic transliteration.
   - Live speech recognition, editable transcript preview, and instant submission.
   - Comprehensive feedback card:
     - **A. Original Answer**
     - **B. Mistakes Identified** (category, incorrect part vs. correction, explanation)
     - **C. Corrected Sentence** (with audio playback)
     - **D. Explanation** in simple English
     - **E. Better Natural Expression**
     - **F. Additional Practical Examples**
     - **G. Practice Again** (repeating the corrected sentence with voice verification)

2. **Interactive 3D-Styled AI Robot Tutor**:
   - Modern blue-and-white aesthetic with gentle floating animations.
   - 7 distinct states: `IDLE`, `GREETING`, `EXPLAINING`, `LISTENING`, `THINKING`, `TEACHING`, `SUCCESS`.
   - Audio-synchronized speaking mouth animation and waveform visualizers.
   - Confetti celebration upon successfully correcting a mistake.

3. **Adaptive Difficulty Engine**:
   - Tracks rolling performance across practice attempts.
   - Promotes learners (Beginner → Intermediate → Advanced) upon consistent high scores (≥ 82%).
   - Avoids demoting on single mistakes; suggests revision only after persistent difficulty.

4. **Additional Learning Modules**:
   - 💬 **AI Conversation Room**: Free-form English chatting with gentle grammar tips.
   - 📚 **Grammar Academy**: Categorized grammar lessons with rules, Telugu learner mistakes, and exercises.
   - 🧩 **Sentence Pattern Practice**: Reusable structures (`I want to + verb`, `I have to + verb`, `I used to + verb`, etc.).
   - 📖 **Vocabulary Trainer**: Daily and workplace words with Telugu meanings and flashcards.
   - 💼 **Interview Preparation**: Mock interviews (Self-Introduction, Python Developer, SQL, HR) with scoring and model answers.
   - 🏆 **Daily Challenges**: Daily speaking tasks with streak and point rewards.
   - 📓 **Mistake Journal**: Persistent log of all identified errors to target recurring weaknesses.
   - 📊 **Progress Centre**: Analytics on speaking minutes, situations completed, accuracy breakdown, and level progression.

---

## 🛠️ Technology Stack

- **Frontend**: React 19, JavaScript, Vite, React Router 7, Lucide React icons, Canvas Confetti.
- **Backend**: Python 3.11, FastAPI, SQLAlchemy, Pydantic V2, JWT Authentication.
- **Database**: SQLite (local development), easily configured for PostgreSQL in production.
- **AI Engine**: Dual-engine architecture:
  - Built-in intelligent English NLP & Grammar engine for 100% offline, zero-latency feedback.
  - Optional plug-and-play **Ollama** integration (`qwen2.5:3b`, `qwen3:4b`, `llama3.2:3b`).
- **Voice**: Browser Web Speech API (`SpeechRecognition` & `SpeechSynthesis`) with text fallback.

---

## 🚀 Setup & Execution Guide

The entire project is built in `D:\speakmate-ai\`.

### 1. Prerequisites
- **Python 3.11+** installed
- **Node.js 18+** & npm installed

### 2. Backend Setup
```bash
# 1. Navigate to the backend directory
cd D:\speakmate-ai\backend

# 2. Activate the virtual environment
.\venv\Scripts\Activate.ps1

# 3. (Optional) Run tests to verify backend
pytest -v

# 4. Start the FastAPI server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
The backend API will be available at:
- **API Base**: `http://127.0.0.1:8000`
- **Interactive Swagger Docs**: `http://127.0.0.1:8000/api/docs`

### 3. Frontend Setup
In a new terminal:
```bash
# 1. Navigate to the frontend directory
cd D:\speakmate-ai\frontend

# 2. (Optional) Run frontend test suite
npm test

# 3. Start the Vite development server
npm run dev
```
Open your browser and navigate to:
👉 **`http://localhost:5173`**

*(Demo learner credentials: `learner@speakmate.ai` / `password123` or click the "Demo Login" button on the login screen).*

---

## 🧪 Running Automated Tests

### Backend Tests (Pytest)
```bash
cd D:\speakmate-ai\backend
.\venv\Scripts\pytest -v
```
Verifies database models, seed data in Telugu and English, AI grammar rules, repeat evaluation, and adaptive progression.

### Frontend Tests (Vitest)
```bash
cd D:\speakmate-ai\frontend
npm test
```
Verifies the Robot Tutor states, Voice Input microphone controls, and Feedback Card sections A through G.

---

## 🦙 Optional: Using Ollama for Local AI

SpeakMate AI operates out-of-the-box using its built-in rule and NLP engine without requiring any external tools. If you wish to enable the local Ollama LLM:
1. Download Ollama from [ollama.com](https://ollama.com).
2. Pull and run a lightweight model:
   ```bash
   ollama run qwen2.5:3b
   ```
3. SpeakMate will automatically connect to `http://localhost:11434` and use the model!
