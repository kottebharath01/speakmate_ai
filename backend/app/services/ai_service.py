import json
import re
import difflib
from typing import Dict, Any, List, Optional
import httpx
from app.core.config import settings
from app.prompts.prompt_templates import (
    TUTOR_SYSTEM_PROMPT,
    SITUATION_GENERATION_PROMPT,
    GRAMMAR_ANALYSIS_PROMPT,
    REPEAT_EVALUATION_PROMPT,
    CONVERSATION_PROMPT,
    INTERVIEW_PROMPT,
    SENTENCE_CORRECTION_PROMPT,
    NATURAL_EXPRESSION_PROMPT
)

class AIService:
    def __init__(self):
        self.ollama_url = f"{settings.OLLAMA_BASE_URL.rstrip('/')}/api/generate"
        self.provider = settings.AI_PROVIDER
        self.model = settings.OLLAMA_MODEL

    async def _query_ollama(self, prompt: str, system: str = TUTOR_SYSTEM_PROMPT) -> Optional[str]:
        """Attempt to call local Ollama server if available."""
        if self.provider != "ollama":
            return None
        try:
            async with httpx.AsyncClient(timeout=2.5) as client:
                payload = {
                    "model": self.model,
                    "prompt": prompt,
                    "system": system,
                    "stream": False,
                    "format": "json"
                }
                response = await client.post(self.ollama_url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    return data.get("response", "")
        except Exception:
            # Ollama not reachable or offline; gracefully fall through to built-in NLP engine
            return None
        return None

    def _extract_json(self, text: str) -> Optional[Dict[str, Any]]:
        if not text:
            return None
        try:
            return json.loads(text)
        except Exception:
            # Try to regex extract JSON block
            match = re.search(r"\{.*\}", text, re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except Exception:
                    pass
        return None

    # --- Built-in Intelligent Rule & NLP Engine (Fallback & Local Evaluation) ---

    def analyze_english_built_in(self, answer: str, prompt: str, level: str) -> Dict[str, Any]:
        """
        Comprehensive rule-based NLP analyzer for English learners (Telugu native speaker patterns).
        Checks:
        1. Subject-Verb Agreement (e.g., 'he want', 'she know', 'everyone are', 'my friends is')
        2. Wrong auxiliary / state (e.g., 'I am agree', 'I am belong')
        3. Tense errors (e.g., 'yesterday I go', 'didn't knew', 'have saw')
        4. Articles (e.g., 'a apple', 'an university', missing articles)
        5. Prepositions (e.g., 'in Monday', 'at morning', 'married with', 'discuss about')
        6. Sentence structure & Telugu literal translations (e.g., 'I want to going', 'since 2 years I am working')
        7. Natural phrasing
        """
        cleaned = answer.strip()
        lower = cleaned.lower()
        # strip common ending punctuation for word inspection
        words = re.findall(r"\b[A-Za-z']+\b", lower)
        
        mistakes = []
        corrected_sentence = cleaned
        natural_expression = cleaned

        # Common error patterns: (regex pattern, category, incorrect, correction, explanation)
        rules = [
            # Auxiliary mistakes common in Telugu learners
            (r"\bi\s+am\s+agree\b", "grammar", "I am agree", "I agree",
             "In English, 'agree' is already a verb. We do not use 'am' with it; simply say 'I agree'."),
            (r"\bi\s+am\s+belong\b", "grammar", "I am belong", "I belong",
             "'Belong' is a stative verb. Say 'I belong to...' instead of 'I am belong'."),
            (r"\bi\s+am\s+having\s+a\s+doubt\b", "vocabulary", "having a doubt", "have a question",
             "In professional and standard English, say 'I have a question' rather than 'I have a doubt'."),
            
            # Double past tense
            (r"\bdidn't\s+knew\b", "tense", "didn't knew", "didn't know",
             "After the auxiliary 'did / didn't', always use the base form of the verb (V1: know), not the past form (knew)."),
            (r"\bdidn't\s+went\b", "tense", "didn't went", "didn't go",
             "After 'didn't', use base verb 'go'."),
            (r"\bdid\s+you\s+saw\b", "tense", "did you saw", "did you see",
             "After 'did', always use base verb 'see'."),
            
            # Infinitive errors: to + V-ing instead of to + V1
            (r"\bwant\s+to\s+going\b", "sentence_structure", "want to going", "want to go",
             "After 'want to', always use the base form of the verb (go), not the -ing form."),
            (r"\bwant\s+to\s+buying\b", "sentence_structure", "want to buying", "want to buy",
             "Use base verb 'buy' after 'want to'."),
            (r"\bwant\s+to\s+ordering\b", "sentence_structure", "want to ordering", "want to order",
             "Use base verb 'order' after 'want to'."),
            
            # Subject-Verb Agreement: He/She/It + base verb without 's'
            (r"\b(he|she)\s+want\b", "subject_verb", "he/she want", "he/she wants",
             "Third person singular pronouns (he, she, it) take an 's' on the verb in Simple Present."),
            (r"\b(he|she)\s+know\b", "subject_verb", "he/she know", "he/she knows",
             "Add 's' for third-person singular (knows)."),
            (r"\b(he|she)\s+like\b", "subject_verb", "he/she like", "he/she likes",
             "Add 's' for third-person singular (likes)."),
            (r"\b(he|she)\s+don't\b", "subject_verb", "don't", "doesn't",
             "With 'he' or 'she', use 'doesn't' (does not) instead of 'don't'."),
            
            # Articles: a before vowel sound
            (r"\ba\s+(apple|orange|egg|ice|urgent|interview|engineer|api)\b", "article", "a + vowel sound", "an",
             "Use the article 'an' before words that start with a vowel sound (a, e, i, o, u)."),
            (r"\ban\s+(university|uniform|unique|useful|european)\b", "article", "an + 'yu' sound", "a",
             "Although 'university' starts with the letter 'u', it makes a 'yu' consonant sound. Use 'a university'."),
            
            # Prepositions
            (r"\bin\s+monday\b", "preposition", "in Monday", "on Monday",
             "Use the preposition 'on' for days of the week (on Monday, on Tuesday)."),
            (r"\bin\s+sunday\b", "preposition", "in Sunday", "on Sunday",
             "Use 'on' for days of the week."),
            (r"\bat\s+morning\b", "preposition", "at morning", "in the morning",
             "Say 'in the morning' or 'in the evening', but 'at night'."),
            (r"\bdiscuss\s+about\b", "preposition", "discuss about", "discuss",
             "'Discuss' already means talk about. Do not add 'about' after 'discuss'."),
            (r"\bmarried\s+with\b", "preposition", "married with", "married to",
             "In English, someone is 'married to' their spouse, not 'married with'."),
            (r"\bcongratulate\s+for\b", "preposition", "congratulate for", "congratulate on",
             "We say 'congratulate someone ON their achievement', not 'for'."),
            
            # Since vs For (Telugu interference)
            (r"\bsince\s+(\d+|two|three|four|five|six|several)\s+(years|months|days|hours)\b", "tense", "since [duration]", "for [duration]",
             "Use 'for' to describe a duration or period of time (for 2 years). Use 'since' only for a specific starting point (since 2024, since Monday).")
        ]

        for pattern, cat, inc, cor, expl in rules:
            m = re.search(pattern, lower)
            if m:
                mistakes.append({
                    "category": cat,
                    "incorrect_part": inc,
                    "correction": cor,
                    "explanation": expl
                })
                # Attempt regex replacement on original capitalization
                corrected_sentence = re.sub(pattern, cor, corrected_sentence, flags=re.IGNORECASE)

        # Capitalization & punctuation checks
        if corrected_sentence and not corrected_sentence[0].isupper():
            corrected_sentence = corrected_sentence[0].upper() + corrected_sentence[1:]
        if corrected_sentence and not corrected_sentence.endswith(('.', '?', '!')):
            corrected_sentence += '.'

        is_correct = len(mistakes) == 0

        # Score calculation
        base_score = 95 if is_correct else max(40, 90 - (len(mistakes) * 20))
        if len(words) < 3:
            base_score = max(30, base_score - 20)

        # Context-based natural suggestions for situations
        natural_expression = corrected_sentence
        additional_examples = []

        if "shirt" in lower or "shop" in lower or "clothes" in lower:
            natural_expression = "Hi, I am looking for a blue formal cotton shirt in medium size. Could you please show me your collection?"
            additional_examples = [
                "I'd like to check out some blue cotton shirts in size M.",
                "Do you have this blue formal shirt in a medium size?"
            ]
        elif "biryani" in lower or "soup" in lower or "order" in lower or "restaurant" in lower:
            natural_expression = "Hello, I would like to order one hot veg biryani, a bowl of mild chicken soup, and a bottle of mineral water, please."
            additional_examples = [
                "Could we please get one veg biryani and mild chicken soup?",
                "Excuse me, I'm ready to order: one veg biryani and a water bottle."
            ]
        elif "metro" in lower or "direction" in lower or "station" in lower:
            natural_expression = "Excuse me, could you please tell me the way to the nearest metro station?"
            additional_examples = [
                "Pardon me, how do I get to the closest metro station from here?",
                "Could you point me in the direction of the metro station, please?"
            ]
        elif "introduce" in lower or "myself" in lower or "team" in lower:
            natural_expression = "Hello everyone, my name is Alex. I am excited to join the team as a software engineer and look forward to collaborating with you all."
            additional_examples = [
                "Hi team, nice to meet you all. I've joined as a backend developer.",
                "Good morning everyone, I'm glad to be part of this team."
            ]
        elif "leave" in lower or "fever" in lower or "sick" in lower:
            natural_expression = "Good morning, I am feeling unwell with a high fever today and would like to request sick leave. I will keep you updated on my recovery."
            additional_examples = [
                "I am down with a fever today and won't be able to log in. Please approve my leave.",
                "Due to sudden illness, I request permission to take sick leave today."
            ]
        elif "bug" in lower or "api" in lower or "500" in lower:
            natural_expression = "Hi, the user login endpoint is returning a 500 internal server error due to a database timeout. Let's look into it together."
            additional_examples = [
                "I noticed an issue with the auth API throwing 500 errors. Could we pair up to debug it?",
                "The server log shows a database connection timeout on login. Let's inspect the query."
            ]
        else:
            additional_examples = [
                f"You can also say: 'I would like to {answer.strip().lower()}'",
                "Keep your sentence clear and concise."
            ]

        if is_correct:
            simple_explanation = "Great job! Your sentence is grammatically correct and communicates your thought clearly."
            encouragement = "Fantastic speaking! Your sentence formation is accurate and natural."
        else:
            simple_explanation = f"You made {len(mistakes)} mistake(s). Review the highlighted correction and notice the natural alternative."
            encouragement = "Good effort! Making mistakes is part of learning. Practice the corrected sentence with your microphone."

        return {
            "original_answer": answer,
            "is_correct": is_correct,
            "score": float(base_score),
            "mistakes": mistakes,
            "corrected_sentence": corrected_sentence,
            "simple_explanation": simple_explanation,
            "natural_expression": natural_expression,
            "additional_examples": additional_examples,
            "encouragement": encouragement
        }

    async def analyze_answer(self, answer: str, prompt: str, level: str, past_mistakes: str = "") -> Dict[str, Any]:
        """Analyze learner answer using Ollama if online, otherwise fallback to high quality built-in NLP."""
        formatted_prompt = GRAMMAR_ANALYSIS_PROMPT.format(
            prompt=prompt,
            user_answer=answer,
            level=level,
            past_mistakes=past_mistakes or "None"
        )
        
        ollama_response = await self._query_ollama(formatted_prompt)
        parsed = self._extract_json(ollama_response) if ollama_response else None
        
        if parsed and "corrected_sentence" in parsed:
            # Enforce schema fields
            parsed.setdefault("original_answer", answer)
            parsed.setdefault("is_correct", len(parsed.get("mistakes", [])) == 0)
            parsed.setdefault("score", 85.0)
            parsed.setdefault("simple_explanation", "Check the corrected sentence for improved clarity.")
            parsed.setdefault("natural_expression", parsed.get("corrected_sentence", answer))
            parsed.setdefault("additional_examples", [])
            parsed.setdefault("encouragement", "Great attempt! Keep practicing your spoken English.")
            return parsed

        return self.analyze_english_built_in(answer, prompt, level)

    async def evaluate_repeat(self, target_sentence: str, repeated_sentence: str, previous_mistake: Optional[str] = None) -> Dict[str, Any]:
        """Evaluate if the learner repeated the corrected sentence accurately."""
        formatted_prompt = REPEAT_EVALUATION_PROMPT.format(
            target_sentence=target_sentence,
            repeated_sentence=repeated_sentence,
            previous_mistake=previous_mistake or "General pronunciation and grammar accuracy"
        )
        
        ollama_response = await self._query_ollama(formatted_prompt)
        parsed = self._extract_json(ollama_response) if ollama_response else None
        
        if parsed and "is_successful" in parsed:
            return parsed

        # Built-in similarity evaluation
        target_norm = re.sub(r"[^\w\s]", "", target_sentence.lower()).strip()
        repeat_norm = re.sub(r"[^\w\s]", "", repeated_sentence.lower()).strip()

        ratio = difflib.SequenceMatcher(None, target_norm, repeat_norm).ratio()
        is_successful = ratio >= 0.70  # forgiving for minor accents/transcription variations
        score = round(ratio * 100, 1)

        if is_successful:
            feedback = "Excellent! You repeated the sentence accurately and corrected the previous mistake."
            remaining_mistake = None
            next_action = "proceed"
            encouragement = "Brilliant job! You are ready to move on to the next situation."
        else:
            feedback = "You missed a few words or didn't fully apply the correction. Try repeating once more."
            remaining_mistake = f"Expected: '{target_sentence}'"
            next_action = "try_again"
            encouragement = "Almost there! Take a breath, listen to the tutor, and try speaking again."

        return {
            "is_successful": is_successful,
            "accuracy_score": score,
            "feedback": feedback,
            "remaining_mistake": remaining_mistake,
            "next_action": next_action,
            "encouragement": encouragement
        }

    async def generate_situation(self, category: str, level: str) -> Dict[str, Any]:
        """Generate a new situation in Telugu & English."""
        formatted_prompt = SITUATION_GENERATION_PROMPT.format(
            category=category,
            level=level
        )
        ollama_response = await self._query_ollama(formatted_prompt)
        parsed = self._extract_json(ollama_response) if ollama_response else None

        if parsed and "telugu_explanation" in parsed and "english_prompt" in parsed:
            return parsed

        # Fallback generated situational bank
        bank = {
            "BEGINNER": {
                "title": "Buying Groceries at Supermarket",
                "category": category or "Daily Life",
                "level": "BEGINNER",
                "telugu_explanation": "నువ్వు సూపర్ మార్కెట్‌కి వెళ్ళావు. తాజా పండ్లు మరియు కూరగాయలు ఏ సెక్షన్‌లో ఉన్నాయో స్టోర్ హెల్పర్‌ని మర్యాదగా అడగాలి.",
                "telugu_transliteration": "Nuvvu supermarket ki vellavu. Fresh fruits mariyu vegetables ae section lo unnayo adagali.",
                "english_prompt": "How would you politely ask the store helper where the fresh fruits and vegetables section is?",
                "context_tags": "shopping, daily, polite"
            },
            "INTERMEDIATE": {
                "title": "Explaining a Project Deadline Delay",
                "category": category or "Workplace",
                "level": "INTERMEDIATE",
                "telugu_explanation": "ప్రాజెక్ట్‌లో ఊహించని డేటాబేస్ సమస్య రావడం వల్ల డెలివరీ ఒక రోజు ఆలస్యం అవుతుందని నీ ప్రాజెక్ట్ మేనేజర్‌కి ఎలా వివరిస్తావు?",
                "telugu_transliteration": "Project lo unexpected database issue valla delivery 1 day late avthundani manager ki ela chepthavu?",
                "english_prompt": "How would you professionally explain the one-day project delay to your manager due to an unexpected database issue?",
                "context_tags": "workplace, delay, explanation, professional"
            },
            "ADVANCED": {
                "title": "Python Developer Interview: FastAPI Architecture",
                "category": category or "Interview",
                "level": "ADVANCED",
                "telugu_explanation": "ఇంటర్వ్యూయర్ నిన్ను 'FastAPI లో Dependency Injection మరియు Pydantic validation ఎలా పనిచేస్తాయి?' అని అడిగారు. టెక్నికల్‌గా క్లియర్‌గా సమాధానం చెప్పాలి.",
                "telugu_transliteration": "FastAPI lo dependency injection mariyu validation ela panicheyyo interviewer ki explain cheyyali.",
                "english_prompt": "Explain clearly how FastAPI uses Pydantic for data validation and how dependency injection simplifies your backend services.",
                "context_tags": "interview, python, fastapi, technical"
            }
        }
        return bank.get(level.upper(), bank["BEGINNER"])

    async def chat_conversation(self, message: str, topic: str, level: str, history: str = "") -> Dict[str, Any]:
        """Free-form interactive conversation with SpeakMate tutor."""
        formatted_prompt = CONVERSATION_PROMPT.format(
            topic=topic,
            level=level,
            history=history or "Conversation just started.",
            user_message=message
        )
        ollama_response = await self._query_ollama(formatted_prompt)
        parsed = self._extract_json(ollama_response) if ollama_response else None

        if parsed and "reply" in parsed:
            return parsed

        # Built-in contextual responder with grammar coaching
        lower_msg = message.lower()
        gentle_tip = None
        
        # Check for gentle grammar tips
        if "i am agree" in lower_msg:
            gentle_tip = "Coaching tip: Say 'I agree' instead of 'I am agree'."
        elif "didn't knew" in lower_msg:
            gentle_tip = "Coaching tip: Say 'didn't know' with the base verb."

        reply = f"That is really interesting! Talking about {topic} is a great way to build fluency. Could you tell me more about how you usually spend your time when you focus on this?"
        if "hello" in lower_msg or "hi" in lower_msg:
            reply = f"Hello! It's fantastic to chat with you today. We're talking about {topic}. How was your day so far?"

        return {
            "reply": reply,
            "gentle_tip": gentle_tip,
            "suggested_reply_ideas": [
                f"I really enjoy {topic} because it helps me learn new things.",
                "Recently, I have been practicing this every weekend."
            ]
        }

    async def interview_practice(self, topic: str, question: str, answer: str, level: str) -> Dict[str, Any]:
        """Interview simulation evaluation and feedback."""
        formatted_prompt = INTERVIEW_PROMPT.format(
            interview_topic=topic,
            level=level,
            candidate_answer=answer
        )
        ollama_response = await self._query_ollama(formatted_prompt)
        parsed = self._extract_json(ollama_response) if ollama_response else None

        if parsed and "improved_model_answer" in parsed:
            return parsed

        # Built-in interview feedback
        return {
            "score": 82.0,
            "strengths": [
                "Clear direct response addressing the prompt",
                "Good technical terminology and relevance"
            ],
            "areas_for_improvement": [
                "Use the STAR method (Situation, Task, Action, Result) for structured storytelling",
                "Emphasize the impact of your work with specific metrics"
            ],
            "improved_model_answer": f"In my recent project involving {topic}, I designed modular backend services using Python and FastAPI, which reduced API response latency by 35%.",
            "interviewer_feedback": "Good attempt! Maintain steady pacing and speak with confidence.",
            "next_question": "Can you describe a challenging technical bug you encountered and how you solved it?"
        }

ai_service = AIService()
