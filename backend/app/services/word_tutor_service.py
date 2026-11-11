import difflib
import re
from typing import Dict, Any, List, Optional
from app.models.words_expressions import WordItem
from app.services.ai_service import ai_service
from app.utils.text_utils import normalize_text


class WordTutorService:
    """
    Beginner-friendly evaluator for Words & Expressions sessions.
    Evaluates English translations by meaning, valid synonyms/alternatives,
    and basic grammar without enforcing only a single rigid string.
    """

    @staticmethod
    def get_valid_english_options(item: WordItem) -> List[str]:
        options = [item.english_text]
        if item.valid_alternatives_json:
            options.extend([str(x) for x in item.valid_alternatives_json if x])
        if item.synonyms_json:
            options.extend([str(x) for x in item.synonyms_json if x])
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for opt in options:
            norm = normalize_text(opt)
            if norm and norm not in seen:
                seen.add(norm)
                unique.append(opt.strip())
        return unique

    @staticmethod
    def evaluate_answer(item: WordItem, user_answer: str) -> Dict[str, Any]:
        cleaned = user_answer.strip()
        norm_user = normalize_text(cleaned)
        valid_options = WordTutorService.get_valid_english_options(item)
        norm_options = [normalize_text(opt) for opt in valid_options]

        examples = item.examples_json or []
        primary_example = (
            examples[0]["english"]
            if examples and isinstance(examples[0], dict) and "english" in examples[0]
            else f"Try using '{item.english_text}' in your daily conversation."
        )

        # 1. Empty or non-meaningful answer check
        if not norm_user:
            return {
                "is_correct": False,
                "matched_option": None,
                "accepted_answer": item.english_text,
                "valid_alternatives": valid_options,
                "feedback": "You submitted an empty answer. Let's learn the correct English expression!",
                "correction_details": f"The correct English equivalent for '{item.telugu_text}' is '{item.english_text}'.",
                "example_sentence": primary_example,
            }

        # 2. Direct normalized match against primary or any valid alternative / synonym
        for raw_opt, norm_opt in zip(valid_options, norm_options):
            if norm_user == norm_opt:
                alt_note = ""
                if norm_opt != normalize_text(item.english_text):
                    alt_note = f" Another common way is '{item.english_text}'."
                return {
                    "is_correct": True,
                    "matched_option": raw_opt,
                    "accepted_answer": item.english_text,
                    "valid_alternatives": valid_options,
                    "feedback": f"Correct! '{cleaned}' is a natural and accurate English answer.{alt_note}",
                    "correction_details": None,
                    "example_sentence": primary_example,
                }

        # 3. Handle helper prefixes like "it means X", "we say X", "to postpone"
        stripped_prefix = re.sub(
            r"^(it means|we say|in english it is|to|the word is|you can say)\s+",
            "",
            norm_user,
        ).strip()
        for raw_opt, norm_opt in zip(valid_options, norm_options):
            if stripped_prefix == norm_opt:
                return {
                    "is_correct": True,
                    "matched_option": raw_opt,
                    "accepted_answer": item.english_text,
                    "valid_alternatives": valid_options,
                    "feedback": f"Correct! '{cleaned}' captures the right meaning ('{raw_opt}').",
                    "correction_details": None,
                    "example_sentence": primary_example,
                }

        # 4. High similarity tolerance for minor spelling slips OR multi-word sentence equivalence
        best_ratio = 0.0
        best_opt = item.english_text
        for raw_opt, norm_opt in zip(valid_options, norm_options):
            ratio = difflib.SequenceMatcher(None, norm_user, norm_opt).ratio()
            # Also check word-level Jaccard overlap for longer sentences/expressions
            user_tokens = set(norm_user.split())
            opt_tokens = set(norm_opt.split())
            # Remove tiny filler words for semantic overlap check
            stop_words = {"a", "an", "the", "to", "i", "is", "are", "for", "of", "in", "on", "please"}
            core_opt = opt_tokens - stop_words
            core_user = user_tokens - stop_words
            token_overlap = (
                len(core_user & core_opt) / max(1, len(core_opt))
                if core_opt
                else 0.0
            )
            combined_score = max(ratio, token_overlap if len(norm_opt.split()) >= 3 else ratio)
            if combined_score > best_ratio:
                best_ratio = combined_score
                best_opt = raw_opt

        # Check grammar on longer inputs first so glaring grammar bugs still get taught
        grammar_check = None
        if len(cleaned.split()) >= 3:
            grammar_check = ai_service.analyze_english_built_in(cleaned, item.telugu_text, item.level)

        has_grammar_mistake = grammar_check and not grammar_check.get("is_correct", True)

        if best_ratio >= 0.80 and not has_grammar_mistake:
            return {
                "is_correct": True,
                "matched_option": best_opt,
                "accepted_answer": item.english_text,
                "valid_alternatives": valid_options,
                "feedback": f"Well done! Your answer is close and natural ('{best_opt}').",
                "correction_details": None,
                "example_sentence": primary_example,
            }

        # 5. If a single-word prompt was used naturally inside a valid grammatical sentence
        if item.mode == "words" and normalize_text(item.english_text) in norm_user.split() and not has_grammar_mistake:
            return {
                "is_correct": True,
                "matched_option": item.english_text,
                "accepted_answer": item.english_text,
                "valid_alternatives": valid_options,
                "feedback": f"Great! You correctly used '{item.english_text}' in your response.",
                "correction_details": None,
                "example_sentence": primary_example,
            }

        # 6. Otherwise, answer is incorrect -> prepare helpful explanation + example + ask for 2 repetitions
        if has_grammar_mistake and grammar_check.get("mistakes"):
            m = grammar_check["mistakes"][0]
            why = m.get("explanation", "Watch sentence grammar and phrasing.")
            correction_details = (
                f"Issue spotted: '{m.get('incorrect_part', cleaned)}' -> {why} "
                f"Natural answer: '{item.english_text}'."
            )
        else:
            definition = item.english_definition or f"means '{item.telugu_text}'."
            when = f" {item.when_to_use}" if item.when_to_use else ""
            correction_details = (
                f"'{cleaned}' does not accurately convey '{item.telugu_text}'. "
                f"'{item.english_text}' means: {definition}{when}"
            )

        alts_display = ", ".join(valid_options[:4])
        feedback = (
            f"Not quite. For '{item.telugu_text}', the natural English is '{item.english_text}' "
            f"(also valid: {alts_display})."
        )

        return {
            "is_correct": False,
            "matched_option": None,
            "accepted_answer": item.english_text,
            "valid_alternatives": valid_options,
            "feedback": feedback,
            "correction_details": correction_details,
            "example_sentence": primary_example,
        }

    @staticmethod
    def evaluate_repetition(target_answer: str, valid_alternatives: List[str], repeated_text: str) -> Dict[str, Any]:
        """Verifies a learner's correction repetition against the corrected English answer."""
        norm_rep = normalize_text(repeated_text)
        if not norm_rep:
            return {
                "is_successful": False,
                "accuracy_score": 0.0,
                "feedback": f"Please say or type the corrected answer: '{target_answer}'.",
            }

        candidates = [target_answer] + [a for a in (valid_alternatives or []) if a]
        best_score = 0.0
        for cand in candidates:
            norm_cand = normalize_text(cand)
            if not norm_cand:
                continue
            if norm_rep == norm_cand:
                best_score = 1.0
                break
            ratio = difflib.SequenceMatcher(None, norm_rep, norm_cand).ratio()
            if ratio > best_score:
                best_score = ratio

        accuracy = round(best_score * 100.0, 1)
        is_ok = best_score >= 0.80
        if is_ok:
            return {
                "is_successful": True,
                "accuracy_score": accuracy,
                "feedback": f"Accurate repetition! ({accuracy}% match)",
            }
        return {
            "is_successful": False,
            "accuracy_score": accuracy,
            "feedback": f"Almost there! Make sure to repeat carefully: \"{target_answer}\"",
        }


word_tutor_service = WordTutorService()
