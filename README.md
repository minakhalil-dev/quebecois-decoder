# Québécois Decoder — c'est quoi, ça?

A tiny, offline dictionary + quiz for Quebec French expressions.
Type a word you heard on the street, at work, or in a show, and get
a plain-English meaning, a Quebec example, and — most importantly —
how polite (or not) the word actually is.

```bash
python decoder.py lookup tabarnak
# tabarnak [vulgar] — Swear word — do NOT use at work or with strangers.
#   Meaning: A strong exclamation, like 'damn!' — from 'tabernacle'.
```

No API key, no account. Python standard library only.

## Quickstart (3 commands)

```bash
python decoder.py lookup "cinq à sept"
python decoder.py search car
python decoder.py quiz --questions 5
```

Lookup is accent- and case-insensitive, so `depanneur`, `DÉPANNEUR`,
and `dépanneur` all work. A miss gives you "did you mean?" suggestions
instead of silence.

## Why the register matters

Quebec French is full of words that are fine with friends and a swear
word at work. "Tabarnak" is not a job-interview word; "câline" is its
polite cousin. A decoder that only translates, without the register,
would get a newcomer into trouble — so every entry is labelled:

- `polite` — safe anywhere
- `familiar` — fine with friends, not in a formal email
- `vulgar` — swear word, do not use at work or with strangers

The dictionary is original writing for this project — definitions and
examples written here, not copied from a published dictionary. It is a
starter set for learners (37 entries: 28 familiar, 5 polite, 4 vulgar),
not a scholarly lexicon. The tricky ones are flagged in the notes, like
"écoeurant", which can mean disgusting *or* amazing depending on tone.

## Results (measured, 2026-10-29)

```bash
python -m unittest test_decoder -v
# Ran 9 tests — OK
```

Tests cover: exact lookup, accent/case-insensitive lookup, unknown
words returning suggestions, search by meaning, vulgar entries carrying
a warning, and quiz questions having 4 distinct options with the
correct meaning in them (deterministic with a seed, so the quiz is
testable, not just random).

## Project structure

```
decoder.py          # lookup, search, list, quiz (stdlib only)
data/words.json     # 37 entries: term, meaning, examples, register
test_decoder.py     # 9 tests
```

## Add a word

Add an entry to `data/words.json` with `term`, `meaning_en`,
`example_qc`, `example_en`, and `register` (polite / familiar / vulgar),
then run the tests — a missing field or a duplicate term fails loudly
instead of shipping a half-empty entry.
