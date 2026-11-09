# SpeakMate AI – REST API Specification

Base URL: `http://localhost:8000/api`

Interactive Swagger Documentation: `http://localhost:8000/api/docs`

---

## 1. Authentication Endpoints

### `POST /api/auth/register`
Creates a new learner account.
- **Request Body**:
  ```json
  {
    "email": "user@example.com",
    "username": "user",
    "password": "password123",
    "full_name": "Learner Name"
  }
  ```

### `POST /api/auth/login`
Authenticates credentials and returns a JWT access token.
- **Request Body**:
  ```json
  {
    "email": "learner@speakmate.ai",
    "password": "password123"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJ...",
    "token_type": "bearer"
  }
  ```

### `GET /api/auth/me`
Retrieves currently authenticated user details.

---

## 2. Situations Endpoints

### `GET /api/situations`
Query params: `level` (`BEGINNER`, `INTERMEDIATE`, `ADVANCED`), `category`.
Returns list of situations matching criteria.

### `GET /api/situations/{id}`
Returns details of a single situation.

### `POST /api/situations/generate`
Generates a dynamic new real-life situation using AI.
- Query params: `category`, `level`.

### `POST /api/situations/submit`
Analyzes learner's spoken or written answer.
- **Request Body**:
  ```json
  {
    "situation_id": 1,
    "original_answer": "I am want a blue shirt",
    "recognized_transcript": "I am want a blue shirt"
  }
  ```
- **Response (Structured Feedback A to G)**:
  ```json
  {
    "original_answer": "I am want a blue shirt",
    "is_correct": false,
    "score": 70.0,
    "mistakes": [
      {
        "category": "grammar",
        "incorrect_part": "I am want",
        "correction": "I want",
        "explanation": "Do not use 'am' before the verb 'want'. Say 'I want'."
      }
    ],
    "corrected_sentence": "I want a blue shirt.",
    "simple_explanation": "Use Simple Present without auxiliary am.",
    "natural_expression": "I am looking for a blue formal shirt.",
    "additional_examples": [
      "I'd like to check out some blue cotton shirts in size M."
    ],
    "encouragement": "Good effort! Practice the corrected sentence.",
    "attempt_id": 12
  }
  ```

### `POST /api/situations/repeat-evaluation`
Evaluates the learner's repeated pronunciation of the corrected sentence.

---

## 3. AI Modules Endpoints

### `POST /api/ai/chat`
Free-form conversation with SpeakMate tutor, returning replies, gentle coaching tips, and reply ideas.

### `POST /api/ai/correct-sentence`
Direct grammar and sentence structure verification.

### `POST /api/interviews/start`
Starts a mock interview session for a specified track.

### `POST /api/interviews/answer`
Evaluates a candidate's answer for technical interviews (Python, SQL, HR, etc.).

---

## 4. Learning & Progress Endpoints

- `GET /api/lessons`: Grammar academy lessons.
- `GET /api/patterns`: Reusable sentence patterns.
- `GET /api/vocabulary`: Vocabulary flashcards and search.
- `GET /api/daily-challenges`: Daily speaking challenges.
- `GET /api/dashboard-stats`: Overall streak, level, recent mistakes, and weekly trend.
- `GET /api/mistakes`: Mistake journal entries.
- `GET /api/progress`: Historical daily practice records.
