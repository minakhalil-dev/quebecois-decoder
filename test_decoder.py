"""Tests for Quebecois Decoder."""

import unittest

from decoder import (
    _normalize,
    format_entry,
    load_words,
    lookup,
    make_quiz,
    search,
    suggest,
)


class TestDictionary(unittest.TestCase):
    def setUp(self):
        self.words = load_words()

    def test_dictionary_loads_and_has_entries(self):
        self.assertGreaterEqual(len(self.words), 30)

    def test_all_registers_valid(self):
        for w in self.words:
            self.assertIn(w["register"], ("polite", "familiar", "vulgar"))

    def test_lookup_exact(self):
        entry = lookup(self.words, "tabarnak")
        self.assertIsNotNone(entry)
        self.assertEqual(entry["register"], "vulgar")

    def test_lookup_accent_insensitive_simple(self):
        self.assertIsNotNone(lookup(self.words, "depanneur"))
        self.assertIsNotNone(lookup(self.words, "Cinq À Sept"))

    def test_lookup_unknown_returns_none_and_suggests(self):
        self.assertIsNone(lookup(self.words, "tabarnakk"))
        suggestions = suggest(self.words, "tabarnakk")
        self.assertIn("tabarnak", suggestions)

    def test_search_finds_by_meaning(self):
        results = search(self.words, "car")
        terms = [w["term"] for w in results]
        self.assertIn("char", terms)

    def test_format_includes_register_warning_for_vulgar(self):
        entry = lookup(self.words, "tabarnak")
        text = format_entry(entry)
        self.assertIn("Swear word", text)


class TestQuiz(unittest.TestCase):
    def setUp(self):
        self.words = load_words()

    def test_quiz_has_four_options_and_correct_answer(self):
        questions = make_quiz(self.words, n=5, seed=42)
        self.assertEqual(len(questions), 5)
        for q in questions:
            self.assertEqual(len(q["options"]), 4)
            self.assertEqual(len(set(q["options"])), 4)
            entry = lookup(self.words, q["term"])
            self.assertEqual(q["options"][q["answer_index"]], entry["meaning_en"])

    def test_quiz_is_deterministic_with_seed(self):
        q1 = make_quiz(self.words, n=5, seed=123)
        q2 = make_quiz(self.words, n=5, seed=123)
        self.assertEqual(q1, q2)


if __name__ == "__main__":
    unittest.main()
