#!/usr/bin/env python3
"""
Quebecois Decoder — "c'est quoi, ça?"

A tiny, offline dictionary + quiz for Quebec French expressions.
Type a word you heard on the street, at work, or in a show, and get
a plain-English meaning, a Quebec example sentence, and how polite
(or not) the word actually is.

Why the register matters
------------------------
Quebec French is full of words that are perfectly normal in one
context and a swear word in another. "Tabarnak" is not a word to use
in a job interview; "câline" is its polite cousin. A decoder that
only gives a translation, without the register, would get a newcomer
into trouble. So every entry carries one of: polite / familiar / vulgar.

The dictionary is original writing for this project — definitions
and examples written here, not copied from a published dictionary.
It is a starter set for learners, not a scholarly lexicon.

Usage
-----
    python decoder.py lookup tabarnak
    python decoder.py lookup "cinq à sept"
    python decoder.py search char
    python decoder.py list --register vulgar
    python decoder.py quiz --questions 5
    python -m unittest test_decoder -v
"""

from __future__ import annotations

import argparse
import difflib
import json
import random
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent
WORDS_PATH = ROOT / "data" / "words.json"


def _normalize(text: str) -> str:
    """Lowercase, strip accents and extra spaces, for forgiving lookup."""
    text = unicodedata.normalize("NFKD", text.strip().lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return " ".join(text.split())


def load_words(path: Path = WORDS_PATH) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    words = data["words"]
    # Validate the contract every entry must keep, so a bad edit to
    # words.json fails loudly instead of shipping a half-empty entry.
    required = {"term", "meaning_en", "example_qc", "example_en", "register"}
    for entry in words:
        missing = required - entry.keys()
        if missing:
            raise ValueError(f"Entry {entry.get('term', '?')!r} is missing {missing}")
        if entry["register"] not in ("polite", "familiar", "vulgar"):
            raise ValueError(f"Entry {entry['term']!r} has unknown register {entry['register']!r}")
    terms = [_normalize(w["term"]) for w in words]
    if len(set(terms)) != len(terms):
        raise ValueError("Duplicate term in words.json (after accent-insensitive matching)")
    return words


def lookup(words: list[dict], query: str) -> dict | None:
    """Exact lookup, accent- and case-insensitive. Returns the entry or None."""
    needle = _normalize(query)
    for entry in words:
        if _normalize(entry["term"]) == needle:
            return entry
    return None


def suggest(words: list[dict], query: str, n: int = 3) -> list[str]:
    """Closest terms, for 'did you mean?' on a miss."""
    terms = [w["term"] for w in words]
    normalized = { _normalize(t): t for t in terms }
    close = difflib.get_close_matches(_normalize(query), list(normalized), n=n, cutoff=0.5)
    return [normalized[c] for c in close]


def search(words: list[dict], query: str) -> list[dict]:
    """Substring search over terms and meanings."""
    needle = _normalize(query)
    return [
        w for w in words
        if needle in _normalize(w["term"]) or needle in _normalize(w["meaning_en"])
    ]


def format_entry(entry: dict) -> str:
    register_note = {
        "polite": "Safe anywhere.",
        "familiar": "Informal — fine with friends, not in a formal email.",
        "vulgar": "Swear word — do NOT use at work or with strangers.",
    }[entry["register"]]
    return (
        f"{entry['term']} [{entry['register']}] — {register_note}\n"
        f"  Meaning: {entry['meaning_en']}\n"
        f"  Example (QC): {entry['example_qc']}\n"
        f"  Example (EN): {entry['example_en']}"
    )


def make_quiz(words: list[dict], n: int = 5, seed: int | None = None) -> list[dict]:
    """Build a multiple-choice quiz: pick a term, 1 correct meaning + 3 others."""
    rng = random.Random(seed)
    chosen = rng.sample(words, min(n, len(words)))
    questions = []
    for entry in chosen:
        distractors = rng.sample([w for w in words if w is not entry], 3)
        options = [entry["meaning_en"]] + [d["meaning_en"] for d in distractors]
        rng.shuffle(options)
        questions.append({
            "term": entry["term"],
            "options": options,
            "answer_index": options.index(entry["meaning_en"]),
        })
    return questions


def run_quiz_interactive(words: list[dict], n: int = 5) -> int:
    questions = make_quiz(words, n=n)
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"\n{i}. What does '{q['term']}' mean?")
        for j, opt in enumerate(q["options"], 1):
            print(f"   {j}. {opt}")
        try:
            choice = int(input("Your answer (number): ").strip())
        except (ValueError, EOFError):
            print("Skipped.")
            continue
        if 1 <= choice <= len(q["options"]) and choice - 1 == q["answer_index"]:
            print("Correct!")
            score += 1
        else:
            print(f"Not quite — the answer was: {q['options'][q['answer_index']]}")
    print(f"\nScore: {score}/{len(questions)}")
    return score


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Quebecois Decoder")
    sub = parser.add_subparsers(dest="command", required=True)

    p_lookup = sub.add_parser("lookup", help="Look up one expression")
    p_lookup.add_argument("term")

    p_search = sub.add_parser("search", help="Search terms and meanings")
    p_search.add_argument("query")

    p_list = sub.add_parser("list", help="List all entries, optionally by register")
    p_list.add_argument("--register", choices=["polite", "familiar", "vulgar"], default=None)

    p_quiz = sub.add_parser("quiz", help="Interactive multiple-choice quiz")
    p_quiz.add_argument("--questions", type=int, default=5)

    args = parser.parse_args(argv)
    words = load_words()

    if args.command == "lookup":
        entry = lookup(words, args.term)
        if entry:
            print(format_entry(entry))
            return 0
        print(f"No entry for {args.term!r}.")
        suggestions = suggest(words, args.term)
        if suggestions:
            print("Did you mean: " + ", ".join(suggestions) + "?")
        return 1

    if args.command == "search":
        results = search(words, args.query)
        if not results:
            print(f"No matches for {args.query!r}.")
            return 1
        for entry in results:
            print(f"- {entry['term']} [{entry['register']}]: {entry['meaning_en']}")
        return 0

    if args.command == "list":
        entries = [w for w in words if args.register is None or w["register"] == args.register]
        for entry in entries:
            print(f"- {entry['term']} [{entry['register']}]")
        print(f"{len(entries)} entries.")
        return 0

    if args.command == "quiz":
        run_quiz_interactive(words, n=args.questions)
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
