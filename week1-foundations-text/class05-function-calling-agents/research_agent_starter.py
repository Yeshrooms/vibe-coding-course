"""
GSET Vibe Coding — Class 5 Starter: Wikipedia Research Agent 📚🔎
================================================================

WHAT YOU'RE BUILDING
  Ask a factual question and the AI answers it by *looking it up on Wikipedia*
  instead of guessing from memory. It searches, reads the article, and then
  answers WITH A SOURCE LINK — in a LOOP, until it has a grounded answer.

  This is called RAG (Retrieval-Augmented Generation): the AI "retrieves" real
  facts first, then writes its answer using them. RAG is one of the best ways to
  STOP an AI from "hallucinating" (making things up). See the README for more.

  Once this works in the terminal, hand it to Antigravity to make a web app.

TWO+ONE BIG IDEAS
  • FUNCTION CALLING  -> the AI can run our search_wikipedia() tool.
  • AGENTIC LOOP      -> it can search again and again until it can answer.
  • RAG (grounding)   -> it answers ONLY from what it looked up, and cites the source.

HOW TO RUN IT
  1. Copy .env.example to .env and paste your Gemini key in.
  2. From the project's ROOT folder, with (gset-vibes) active (needs internet):

       python week1-foundations-text/class05-function-calling-agents/research_agent_starter.py

------------------------------------------------------------------------------
YOUR STEP-BY-STEP CHECKLIST  (search the file for "TODO")
------------------------------------------------------------------------------
  TODO 1 — Write the system prompt (this is where you tell the AI to use ONLY the
           Wikipedia results and to CITE the source — the anti-hallucination rule!).
  TODO 2 — Finish the description of the give_answer tool.
  TODO 3 — Ask the AI what to do (make the model call inside the loop).
  TODO 4 — When the AI calls give_answer, print the answer and its source.
  TODO 5 — Stop the loop once the AI has answered.

  💡 Parts labeled "BUILDING BLOCK" are done for you. Read the comments!
"""

# --- Libraries we use -------------------------------------------------------
import os
import json
import requests                    # lets us call Wikipedia over the internet
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
# BUILDING BLOCK — the RAG tool: search Wikipedia (already done for you)
# This finds the best matching article and returns a short, plain-text summary
# PLUS the article's URL, so the AI can cite where the facts came from.
# ============================================================================
def search_wikipedia(query):
    """Search Wikipedia and return {title, url, content} as text."""
    api = "https://en.wikipedia.org/w/api.php"
    # Wikipedia asks every program to identify itself with a "User-Agent".
    headers = {"User-Agent": "GSET-Vibe-Coding-Course/1.0 (classroom project)"}

    # 1) Find the best-matching article title for the search.
    search = requests.get(api, headers=headers, params={
        "action": "query", "list": "search", "srsearch": query,
        "format": "json", "srlimit": 1,
    }).json()
    hits = search.get("query", {}).get("search", [])
    if not hits:
        return f"No Wikipedia article was found for '{query}'. Try different keywords."

    title = hits[0]["title"]

    # 2) Get a clean, plain-text summary (the article's intro).
    summary = requests.get(api, headers=headers, params={
        "action": "query", "prop": "extracts", "exintro": True,
        "explaintext": True, "titles": title, "redirects": 1, "format": "json",
    }).json()
    pages = summary.get("query", {}).get("pages", {})
    page = next(iter(pages.values()), {})
    content = page.get("extract", "")[:2000]   # keep it short so the AI reads it easily

    return json.dumps({
        "title": title,
        "url": f"https://en.wikipedia.org/wiki/{title.replace(' ', '_')}",
        "content": content,
    })


# ============================================================================
# BUILDING BLOCK — the menu of tools we give the AI (function calling)
# ============================================================================
tools = [
    {
        # 👇 This first tool is filled in for you as a WORKED EXAMPLE.
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": "Search Wikipedia for facts about a topic and get a "
                           "summary plus the source URL. Use this to look things "
                           "up instead of guessing. You can call it more than once.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Keywords to search for, e.g. 'tallest mountain'",
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "give_answer",
            # ----------------------------------------------------------------
            # TODO 2: Describe this tool. It's how the AI delivers its FINAL
            #   answer, along with the Wikipedia URL it used as a source. Hint:
            #   "Give the final answer to the user, based ONLY on the Wikipedia
            #   results, and include the source URL you used."
            # ----------------------------------------------------------------
            "description": "TODO 2: describe this tool here",
            "parameters": {
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": "The final answer, using only what you found",
                    },
                    "source_url": {
                        "type": "string",
                        "description": "The Wikipedia URL the answer came from",
                    },
                },
                "required": ["answer", "source_url"],
            },
        },
    },
]


# ============================================================================
# THE MAIN EVENT — the agentic loop (this is where YOUR steps go)
# ============================================================================
def research():
    question = input("Ask a factual question: ").strip()

    # ------------------------------------------------------------------------
    # TODO 1: Write the system prompt. THIS is the anti-hallucination part!
    #   Tell the AI:
    #     - It is a careful research assistant.
    #     - It must NOT use its own memory — facts may be outdated or wrong.
    #     - It must call search_wikipedia to find facts FIRST.
    #     - It must answer ONLY using what the search returned.
    #     - If the search doesn't contain the answer, it should search again with
    #       different keywords, or say it couldn't find it (never make it up).
    #     - When ready, it calls give_answer with the answer AND the source URL.
    # ------------------------------------------------------------------------
    system_prompt = "TODO 1: write the AI's grounding instructions here"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question},
    ]

    # ---- THE AGENTIC LOOP --------------------------------------------------
    # Let the AI search as many times as it needs (up to a safety limit).
    for step in range(6):
        # --------------------------------------------------------------------
        # TODO 3: Ask the AI what to do next. Call the model with our tools.
        #   Hint:
        #     response = client.chat.completions.create(
        #         model=MODEL, messages=messages, tools=tools,
        #     )
        # --------------------------------------------------------------------
        response = None  # TODO 3: replace None with the real model call (see hint)

        ai_message = response.choices[0].message
        messages.append({
            "role": "assistant",
            "content": ai_message.content or "",
            "tool_calls": ai_message.tool_calls,
        })

        # If the AI replied with plain text (no tool), just show it and stop.
        if not ai_message.tool_calls:
            print(f"\n🤖 {ai_message.content}\n")
            return

        # Otherwise, run whichever tool(s) the AI asked for.
        for tool_call in ai_message.tool_calls:
            name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)

            if name == "search_wikipedia":
                # 👇 WORKED EXAMPLE — copy this pattern for TODO 4 below.
                print(f"   🔎 Searching Wikipedia for: {args['query']}")
                result = search_wikipedia(args["query"])
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": name,
                    "content": result,
                })

            elif name == "give_answer":
                # ------------------------------------------------------------
                # TODO 4: The AI is delivering its final answer. Print it nicely
                #   for the user, including the source link. Use the values in
                #   args["answer"] and args["source_url"].
                #   Example:
                #     print("\n🤖", args["answer"])
                #     print("📖 Source:", args["source_url"], "\n")
                # ------------------------------------------------------------
                pass  # TODO 4: print the answer and the source here

                # ------------------------------------------------------------
                # TODO 5: We have a grounded answer — stop.
                #   Hint: use `return` to end the function (and the loop).
                # ------------------------------------------------------------
                return  # (leave this so the file runs; TODO 4 fills in the printing)


if __name__ == "__main__":
    research()