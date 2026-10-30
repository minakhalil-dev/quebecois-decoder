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

## Why this project exists

This is a **learning project, not an authoritative dictionary** —
and it is small on purpose.

The point is to show, in one readable file (`decoder.py`), how a
useful language tool works on a real local problem: understanding
Quebec French is not just translation, it is register. That is why
the repo keeps everything visible and testable, instead of hiding
it behind an API:

- **Offline data + lookup** — 37 original entries in
  `data/words.json`, no account, no network, standard library only.
- **Accent- and case-insensitive matching** — `depanneur`,
  `DÉPANNEUR`, and `dépanneur` all resolve, with "did you mean?"
  suggestions on a miss instead of silence.
- **Register as a safety feature** — every entry is labelled polite,
  familiar, or vulgar, because a word that is fine with friends can
  be a swear word at work. That label is the point of the tool, not
  a footnote.
- **A testable quiz** — questions have 4 distinct options with the
  correct meaning in them, deterministic with a seed, so the quiz
  is tested, not just random.

If you are learning from this, read it in this order:
`data/words.json` (the entries), `decoder.py` (lookup, search,
quiz), then `test_decoder.py` (did the lookups, suggestions, and
quiz actually work?). If you wanted to turn this into a real
product, the next steps would be a larger verified lexicon, audio
and pronunciation, and region notes — all listed as future work,
not silently skipped. The definitions here are original, informal
writing for learners, and meanings vary by region, generation,
context, and tone.

## Disclaimer

This project is for education only. It is not an authoritative
dictionary or professional language advice, its definitions are
informal and may vary by region, context, and tone, and vulgar
entries are quoted so learners can recognise them — not as an
endorsement or a recommendation to use them. Use any expression at
your own discretion and risk. The full text is in
[DISCLAIMER.md](DISCLAIMER.md), and the software is provided "AS IS"
under the MIT LICENSE.

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
DISCLAIMER.md       # full disclaimer — read before using
decoder.py          # lookup, search, list, quiz (stdlib only)
data/words.json     # 37 entries: term, meaning, examples, register
test_decoder.py     # 9 tests
```

## Add a word

Add an entry to `data/words.json` with `term`, `meaning_en`,
`example_qc`, `example_en`, and `register` (polite / familiar / vulgar),
then run the tests — a missing field or a duplicate term fails loudly
instead of shipping a half-empty entry.
