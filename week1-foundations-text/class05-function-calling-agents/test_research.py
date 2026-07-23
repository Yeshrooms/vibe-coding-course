"""
Self-check for the Research (RAG) building block 📚
===================================================

Run this to make sure the Wikipedia search tool works. It does NOT need your API
key, but it DOES use the internet, so make sure you're online.

HOW TO RUN (from the project's ROOT folder, with (gset-vibes) active):

    python week1-foundations-text/class05-function-calling-agents/test_research.py

You should see ✅ PASS lines. If a check fails because you're offline, connect to
the internet and try again.
"""

import os
import json

# The starter connects to Gemini when it loads, which normally needs your key.
# These tests don't use the AI, so we set a fake key just so the import works.
os.environ.setdefault("GEMINI_API_KEY", "not-needed-for-this-test")

from research_agent_starter import search_wikipedia


def check(name, condition):
    """Print a friendly PASS/FAIL line and remember the result."""
    print(("✅ PASS" if condition else "❌ FAIL"), "-", name)
    return condition


print("\nChecking the Wikipedia search tool (this uses the internet)...\n")

results = []

try:
    # 1) A real topic should return a title, a URL, and some content.
    info = json.loads(search_wikipedia("Mount Everest"))
    print("   search_wikipedia('Mount Everest') -> title:", info.get("title"))
    print("   source url:", info.get("url"))
    results.append(check("Returns a title, url, and non-empty content",
                         bool(info.get("title"))
                         and info.get("url", "").startswith("https://en.wikipedia.org/wiki/")
                         and len(info.get("content", "")) > 50))

    # 2) The content should actually mention the topic (real facts, grounded).
    results.append(check("Content is about the topic (mentions 'Everest')",
                         "Everest" in info.get("content", "")))

    # 3) Total nonsense should return a friendly 'not found' message.
    missing = search_wikipedia("zxqwerty nonsense not a real topic 12345")
    results.append(check("Gibberish search -> friendly 'not found' message",
                         "No Wikipedia article" in missing))

    print(f"\n{sum(results)} / {len(results)} checks passed.\n")
    if all(results):
        print("🎉 Your research tool works! Now finish the TODOs and ask a question.\n")
    else:
        print("Some checks failed — read the ❌ lines above to see what to fix.\n")

except Exception as error:
    print(f"\n⚠️  Could not run the research checks: {error}")
    print("   Are you connected to the internet? Try again once you're online.\n")