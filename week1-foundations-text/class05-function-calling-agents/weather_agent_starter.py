"""
GSET Vibe Coding — Class 5 Starter: Weather Assistant ⛅🌧️
==========================================================

WHAT YOU'RE BUILDING
  Ask a weather question in plain English ("Do I need an umbrella in Paris
  tomorrow?") and the AI answers by using TOOLS in a LOOP: first it looks up the
  city's map coordinates, THEN it fetches the forecast, THEN it answers you.

  Uses the free Open-Meteo API — NO API key or credit card needed for weather! ✅
  (You still need your GEMINI_API_KEY for the AI part.)

  Once this works in the terminal, hand it to Antigravity to turn it into a web
  app — see the README.

TWO BIG IDEAS
  • FUNCTION CALLING  -> we hand the AI Python functions ("tools") it can run.
  • AGENTIC LOOP      -> the AI takes MULTIPLE steps on its own (find city -> get
                         forecast -> answer) without you editing code in between.

HOW TO RUN IT
  1. Copy .env.example to .env and paste your Gemini key in.
  2. From the project's ROOT folder, with (gset-vibes) active:

       python week1-foundations-text/class05-function-calling-agents/weather_agent_starter.py

------------------------------------------------------------------------------
YOUR STEP-BY-STEP CHECKLIST  (search the file for "TODO")
------------------------------------------------------------------------------
  TODO 1 — Write the system prompt (tell the AI its job and the order of steps).
  TODO 2 — Finish the description of the get_forecast tool.
  TODO 3 — Ask the AI what to do (make the model call inside the loop).
  TODO 4 — When the AI calls get_forecast, run it and hand back the result.
  TODO 5 — Stop the loop once the AI gives a normal text answer (no tool call).

  💡 Parts labeled "BUILDING BLOCK" are done for you. Read the comments!
"""

# --- Libraries we use -------------------------------------------------------
import os
import json
import requests                    # lets us call the free weather API over the internet
from dotenv import load_dotenv     # reads your GEMINI_API_KEY from the .env file
from openai import OpenAI          # we talk to Gemini through its OpenAI-compatible endpoint

load_dotenv()

MODEL = "gemini-3.5-flash"


# ============================================================================
# BUILDING BLOCK — connect to Gemini (already done for you)
# ============================================================================
client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


# ============================================================================
# BUILDING BLOCK — tool #1: turn a city name into map coordinates
# (already done for you). Calls Open-Meteo's free geocoding API.
# ============================================================================
def find_city(name):
    """Look up a city and return its coordinates (latitude/longitude)."""
    url = "https://geocoding-api.open-meteo.com/v1/search"
    response = requests.get(url, params={"name": name, "count": 1})
    data = response.json()

    if not data.get("results"):
        return f"Could not find a city called '{name}'. Ask the user to check the spelling."

    place = data["results"][0]
    return json.dumps({
        "city": place.get("name"),
        "country": place.get("country"),
        "latitude": place.get("latitude"),
        "longitude": place.get("longitude"),
    })


# ============================================================================
# BUILDING BLOCK — tool #2: get the weather forecast for coordinates
# (already done for you). Calls Open-Meteo's free forecast API.
# ============================================================================
def get_forecast(latitude, longitude):
    """Get a simple 3-day forecast for a latitude/longitude."""
    url = "https://api.open-meteo.com/v1/forecast"
    response = requests.get(url, params={
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max",
        "current": "temperature_2m",
        "timezone": "auto",
        "forecast_days": 3,
    })
    data = response.json()
    # Temperatures are in °C, precipitation is a % chance of rain.
    return json.dumps({
        "current_temperature_C": data.get("current", {}).get("temperature_2m"),
        "dates": data.get("daily", {}).get("time"),
        "high_temp_C": data.get("daily", {}).get("temperature_2m_max"),
        "low_temp_C": data.get("daily", {}).get("temperature_2m_min"),
        "chance_of_rain_percent": data.get("daily", {}).get("precipitation_probability_max"),
    })


# ============================================================================
# BUILDING BLOCK — the menu of tools we give the AI (function calling)
# ============================================================================
tools = [
    {
        # 👇 This first tool is filled in for you as a WORKED EXAMPLE.
        "type": "function",
        "function": {
            "name": "find_city",
            "description": "Look up a city by name to get its latitude and "
                           "longitude. Call this FIRST, before getting weather.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "The city name, e.g. 'Paris' or 'Tokyo'",
                    }
                },
                "required": ["name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_forecast",
            # ----------------------------------------------------------------
            # TODO 2: Describe WHAT this tool does and WHEN to use it. The AI
            #   reads this to decide to call it. Hint: it gets the weather for a
            #   latitude/longitude, so it should be called AFTER find_city.
            # ----------------------------------------------------------------
            "description": "This tool gets the weather for a latitude/longitude"
            "It should be called AFTER find_city",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {
                        "type": "number",
                        "description": "The city's latitude (from find_city)",
                    },
                    "longitude": {
                        "type": "number",
                        "description": "The city's longitude (from find_city)",
                    },
                },
                "required": ["latitude", "longitude"],
            },
        },
    },
]


# ============================================================================
# THE MAIN EVENT — the agentic loop (this is where YOUR steps go)
# ============================================================================
def answer_weather_question():
    question = input("Ask a weather question: ").strip()

    # ------------------------------------------------------------------------
    # TODO 1: Write the system prompt (the AI's job description). Tell it:
    #   it's a friendly weather assistant; to answer, it must FIRST call
    #   find_city to get coordinates, THEN call get_forecast, THEN reply with a
    #   short, helpful answer to the user's question. It must not make up
    #   weather — only use the tools.
    # ------------------------------------------------------------------------
    system_prompt = "You are a friendly weather assistant; to answer, you must FIRST call find_city to get coordinates, THEN call get_forecast, THEN reply with a short, helpful answer to the user's question. It must not make up weather — only use the tools."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    # ---- THE AGENTIC LOOP --------------------------------------------------
    # Keep letting the AI take steps until it gives a normal text answer
    # (no more tools). The safety limit stops us from ever looping forever.
    for step in range(6):
        # --------------------------------------------------------------------
        # TODO 3: Ask the AI what to do next. Call the model with our tools.
        #   Hint:
        #     response = client.chat.completions.create(
        #         model=MODEL, messages=messages, tools=tools,
        #     )
        # --------------------------------------------------------------------
        response = client.chat.completions.create(
            model = MODEL, messages = messages, tools = tools,
        )  # TODO 3: replace None with the real model call (see hint)

        ai_message = response.choices[0].message
        messages.append({
            "role": "assistant",
            "content": ai_message.content or "",
            "tool_calls": ai_message.tool_calls,
        })

        # If the AI did NOT ask for a tool, it's giving us the final answer.
        if not ai_message.tool_calls:
            print(f"\n🤖 {ai_message.content}\n")
            # ----------------------------------------------------------------
            # TODO 5: We have our answer — stop the loop.
            #   Hint: use `break` to leave the for-loop.
            # ----------------------------------------------------------------
            break  # TODO 5: break out of the loop here
            break  # (leave this so the file runs even before you finish TODO 5)

        # Otherwise, run whichever tool(s) the AI asked for.
        for tool_call in ai_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)   # the AI's chosen inputs
            print(f"   🔧 AI is using tool: {name}({args})")

            if name == "find_city":
                # 👇 WORKED EXAMPLE — copy this pattern for TODO 4 below.
                result = find_city(args["name"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": result,
                })

            elif name == "get_forecast":
                # ------------------------------------------------------------
                # TODO 4: Run get_forecast() and hand the result back to the AI.
                #   Copy the find_city example just above.
                #   a) call get_forecast(args["latitude"], args["longitude"])
                #   b) append a {"role": "tool", ...} message with the result
                # ------------------------------------------------------------
                result = find_city(args["name"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": result,
                })


if __name__ == "__main__":
    answer_weather_question()