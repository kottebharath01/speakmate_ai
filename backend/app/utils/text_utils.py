import re

CONTRACTION_MAP = {
    "i'm": "i am",
    "you're": "you are",
    "we're": "we are",
    "they're": "they are",
    "he's": "he is",
    "she's": "she is",
    "it's": "it is",
    "that's": "that is",
    "what's": "what is",
    "there's": "there is",
    "don't": "do not",
    "doesn't": "does not",
    "didn't": "did not",
    "can't": "cannot",
    "couldn't": "could not",
    "won't": "will not",
    "wouldn't": "would not",
    "shouldn't": "should not",
    "i'll": "i will",
    "we'll": "we will",
    "you'll": "you will",
    "i've": "i have",
    "we've": "we have",
    "you've": "you have",
    "let's": "let us",
}


def normalize_text(text: str) -> str:
    """
    Converts English text to a normalized lowercase form for fair duplicate
    checking and semantic answer comparison.
    """
    if not text:
        return ""
    cleaned = text.strip().lower()
    # Expand common English contractions so "I'm fine" matches "I am fine"
    words = cleaned.split()
    expanded_words = [CONTRACTION_MAP.get(w.strip(".,!?;:\"'"), w) for w in words]
    joined = " ".join(expanded_words)
    # Remove punctuation and extra spaces
    joined = re.sub(r"[^a-z0-9\s]", " ", joined)
    joined = re.sub(r"\s+", " ", joined).strip()
    return joined
