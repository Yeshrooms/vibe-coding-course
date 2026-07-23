"""
Self-check for the Wordle building blocks 🟩
============================================

Run this to make sure the game logic works. It does NOT need your API key and does
NOT talk to the AI — it just checks the plain Python function `validate_word`.

HOW TO RUN (from the project's ROOT folder, with (gset-vibes) active):

    python week1-foundations-text/class05-function-calling-agents/test_wordle.py

You should see a row of ✅ PASS lines. If you see a ❌ FAIL, read the message —
it tells you what was expected.
"""

import os

# The starter file connects to Gemini when it loads, which normally needs your key.
# These tests don't use the AI, so we set a fake key just so the import works.
os.environ.setdefault("GEMINI_API_KEY", "not-needed-for-this-test")

from wordle_agent_starter import validate_word, get_secret_word


def check(name, condition):
    """Print a friendly PASS/FAIL line and remember the result."""
    print(("✅ PASS" if condition else "❌ FAIL"), "-", name)
    return condition


print("\nChecking the Wordle game logic...\n")

results = []

# 1) A perfect guess should be all green and say CORRECT.
out = validate_word("CRANE", "CRANE")
results.append(check("Correct word -> all green + 'CORRECT'",
                     "🟩 🟩 🟩 🟩 🟩" in out and "CORRECT" in out))

# 2) Mixed feedback. Secret = CRANE, guess = TRAIN:
#      T(not in word)=⬜  R(right spot)=🟩  A(right spot)=🟩  I(not in word)=⬜  N(wrong spot)=🟨
out = validate_word("TRAIN", "CRANE")
results.append(check("Mixed guess -> ⬜ 🟩 🟩 ⬜ 🟨",
                     "⬜ 🟩 🟩 ⬜ 🟨" in out))

# 3) A letter that is NOT in the word should be gray.
out = validate_word("ZZZZZ", "CRANE")
results.append(check("Letters not in word -> all gray",
                     "⬜ ⬜ ⬜ ⬜ ⬜" in out))

# 4) A guess that isn't 5 letters should be rejected.
out = validate_word("CAT", "CRANE")
results.append(check("Too-short guess -> asks to try again",
                     "not 5 letters" in out))

# 5) get_secret_word() should return a real 5-letter word.
word = get_secret_word()
results.append(check("get_secret_word() returns a 5-letter word",
                     isinstance(word, str) and len(word) == 5))

print(f"\n{sum(results)} / {len(results)} checks passed.\n")
if all(results):
    print("🎉 Your Wordle building blocks work! Now finish the TODOs and play the game.\n")
else:
    print("Some checks failed — read the ❌ lines above to see what to fix.\n")