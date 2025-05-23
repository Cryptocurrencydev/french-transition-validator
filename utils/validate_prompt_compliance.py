import re
from collections import defaultdict, Counter

FRENCH_STOPWORDS = {
    "le", "la", "les", "de", "des", "du", "un", "une", "et", "en", "à", "au",
    "aux", "par", "pour", "sur", "avec", "dans", "ce", "cet", "cette", "qui",
    "que", "quoi", "dont", "où", "mais", "ou", "donc", "or", "ni", "car",
    "si", "ne", "pas", "plus", "moins", "très", "ainsi", "comme", "aussi"
}

def tokenize(text):
    text = text.lower()
    text = re.sub(r"[^\w\s']", '', text)
    return text.split()

def check_transition_group(transitions):
    word_counts = Counter()
    all_tokens = []
    enfin_misplaced = False

    for i, phrase in enumerate(transitions):
        tokens = tokenize(phrase)
        if i != len(transitions) - 1 and "enfin" in tokens:
            enfin_misplaced = True
        all_tokens.extend([t for t in tokens if t not in FRENCH_STOPWORDS])

    repeated_words = [word for word, count in Counter(all_tokens).items() if count > 1]

    violations = {}
    if repeated_words:
        violations["repetition"] = repeated_words
    if enfin_misplaced:
        violations["enfin_misplaced"] = True

    return violations

def validate_batch(batch_outputs):
    summary = {
        "total_outputs": len(batch_outputs),
        "outputs_with_violations": 0,
        "violations_summary": {
            "repetition": {
                "count": 0,
                "affected_outputs": [],
                "violated_words": []
            },
            "enfin_misplaced": {
                "count": 0,
                "affected_outputs": []
            }
        },
        "details": []
    }

    all_violated_words = set()

    for i, transitions in enumerate(batch_outputs, start=1):
        violations = check_transition_group(transitions)
        detail = {
            "output_id": i,
            "transitions": transitions,
            "violations": violations
        }

        if violations:
            summary["outputs_with_violations"] += 1

            if "repetition" in violations:
                summary["violations_summary"]["repetition"]["count"] += 1
                summary["violations_summary"]["repetition"]["affected_outputs"].append(i)
                all_violated_words.update(violations["repetition"])

            if "enfin_misplaced" in violations:
                summary["violations_summary"]["enfin_misplaced"]["count"] += 1
                summary["violations_summary"]["enfin_misplaced"]["affected_outputs"].append(i)

        summary["details"].append(detail)

    summary["violations_summary"]["repetition"]["violated_words"] = sorted(all_violated_words)
    return summary
