"""
Self-check for the Weather building blocks ⛅
=============================================

Run this to make sure the two weather tools work. It does NOT need your API key
(Open-Meteo is free!), but it DOES use the internet, so make sure you're online.

HOW TO RUN (from the project's ROOT folder, with (gset-vibes) active):

    python week1-foundations-text/class05-function-calling-agents/test_weather.py

You should see ✅ PASS lines. If a check fails because you're offline, connect to
the internet and try again.
"""

import os
import json

# The starter file connects to Gemini when it loads, which normally needs your key.
# These tests don't use the AI, so we set a fake key just so the import works.
os.environ.setdefault("GEMINI_API_KEY", "not-needed-for-this-test")

from weather_agent_starter import find_city, get_forecast


def check(name, condition):
    """Print a friendly PASS/FAIL line and remember the result."""
    print(("✅ PASS" if condition else "❌ FAIL"), "-", name)
    return condition


print("\nChecking the weather tools (this uses the internet)...\n")

results = []

try:
    # 1) find_city("Paris") should return coordinates for Paris, France.
    #    Paris is near latitude 48.85, longitude 2.35.
    city_info = json.loads(find_city("Paris"))
    print("   find_city('Paris') ->", city_info)
    results.append(check("find_city returns Paris' coordinates",
                         city_info.get("city") == "Paris"
                         and 48 < city_info.get("latitude", 0) < 49))

    # 2) A made-up city should return a helpful 'not found' message.
    missing = find_city("asdfghjkl")
    results.append(check("Unknown city -> friendly 'could not find' message",
                         "Could not find" in missing))

    # 3) get_forecast() for Paris should return temperature data.
    forecast = json.loads(get_forecast(48.85, 2.35))
    print("   get_forecast(48.85, 2.35) ->", forecast)
    results.append(check("get_forecast returns high temperatures for 3 days",
                         isinstance(forecast.get("high_temp_C"), list)
                         and len(forecast["high_temp_C"]) == 3))

    print(f"\n{sum(results)} / {len(results)} checks passed.\n")
    if all(results):
        print("🎉 Your weather tools work! Now finish the TODOs and ask a question.\n")
    else:
        print("Some checks failed — read the ❌ lines above to see what to fix.\n")

except Exception as error:
    print(f"\n⚠️  Could not run the weather checks: {error}")
    print("   Are you connected to the internet? Try again once you're online.\n")