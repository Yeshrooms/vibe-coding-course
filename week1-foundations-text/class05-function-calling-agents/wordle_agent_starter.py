"""
GSET Vibe Coding — Class 5 Starter: AI Wordle Game Master 🟩🟨⬜
================================================================

WHAT YOU'RE BUILDING
  An AI that runs a game of Wordle *for you* in the terminal. You type 5-letter
  guesses; the AI uses TOOLS (functions you give it) to check each guess and it
  keeps the game going in a LOOP until you win or run out of guesses.

  Once this works in the terminal, you'll hand it to Antigravity and say
  "turn this into a web app" — see the README. Get the brain working first! 🧠

TWO BIG IDEAS (this is the whole point of Class 5)
  • FUNCTION CALLING  -> we hand the AI some Python functions ("tools") it can run.
  • AGENTIC LOOP      -> a while-loop that lets the AI keep taking steps on its own.

HOW TO RUN IT
  1. Make sure your key is set:  copy .env.example to .env and paste your key in.
  2. From the project's ROOT folder, with (gset-vibes) active:

       python week1-foundations-text/class05-function-calling-agents/wordle_agent_starter.py

------------------------------------------------------------------------------
YOUR STEP-BY-STEP CHECKLIST  (search the file for "TODO" to find each one)
------------------------------------------------------------------------------
  TODO 1 — Write the system prompt (tell the AI its job + the secret word).
  TODO 2 — Finish the description of the validate_word tool.
  TODO 3 — Ask the AI what to do (make the model call inside the loop).
  TODO 4 — When the AI calls validate_word, run it and hand back the result.
  TODO 5 — Stop the loop when the game is over.

  💡 Everything you DON'T need to change is already written for you below and
     labeled "BUILDING BLOCK". Read the comments — they explain what each part does.
"""

# --- Libraries we use -------------------------------------------------------
import os
import json
import random
from dotenv import load_dotenv     # reads your GEMINI_API_KEY from the .env file
from openai import OpenAI          # we talk to Gemini through its OpenAI-compatible endpoint

# Load your secret key from the .env file into the program.
load_dotenv()

MODEL = "gemini-3.5-flash"         # the AI model that will be our game master
MAX_GUESSES = 6                    # classic Wordle gives you 6 tries


# ============================================================================
# BUILDING BLOCK — connect to Gemini (already done for you)
# The AI is reached through an "OpenAI-compatible" address. You don't need to
# change this. It automatically uses GEMINI_API_KEY from your .env file.
# ============================================================================
client = OpenAI(
    api_key=os.environ["GEMINI_API_KEY"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


# ============================================================================
# BUILDING BLOCK — pick a secret word (already done for you)
# Reads a random 5-letter word from wordle.txt (which is in this folder).
# ============================================================================
def get_secret_word():
    """Return one random 5-letter word from wordle.txt."""
    folder = os.path.dirname(__file__)          # the folder this file lives in
    path = os.path.join(folder, "wordle.txt")
    with open(path, "r") as file:
        words = [line.strip() for line in file if line.strip()]
    return random.choice(words).upper()


# ============================================================================
# BUILDING BLOCK — the game logic (already done for you)
# This is a normal Python function. Later, we let the AI call it as a "tool".
# It compares a guess to the secret word and returns colored feedback:
#     🟩 = right letter, right spot     🟨 = right letter, wrong spot     ⬜ = not in word
# ============================================================================
def validate_word(guess, secret_word):
    """Compare a 5-letter guess to the secret word and return emoji feedback."""
    guess = guess.strip().upper()
    secret_word = secret_word.strip().upper()

    if len(guess) != 5:
        return "That guess is not 5 letters. Ask the player to try again."

    feedback = []
    for i in range(5):
        if guess[i] == secret_word[i]:
            feedback.append("🟩")        # correct letter, correct position
        elif guess[i] in secret_word:
            feedback.append("🟨")        # letter is in the word, wrong position
        else:
            feedback.append("⬜")        # letter is not in the word

    result = " ".join(feedback)
    if guess == secret_word:
        return f"{result}  — CORRECT! The player guessed the word: {secret_word}"
    return f"Hint for '{guess}': {result}"


# ============================================================================
# BUILDING BLOCK — end the game (already done for you)
# Another tool the AI can call when the game is over.
# ============================================================================
def end_game(reason, answer):
    """Return a friendly game-over message."""
    if reason == "WON":
        return f"🎉 You won! The word was {answer}. Nice guessing!"
    elif reason == "LOST":
        return f"😔 Out of guesses! The word was {answer}. Try again!"
    else:
        return f"👋 Game over ({reason}). The word was {answer}."


# ============================================================================
# BUILDING BLOCK — the menu of tools we give the AI (function calling)
# This "tools" list DESCRIBES our Python functions to the AI so it knows they
# exist and what inputs they need. The AI reads these descriptions to decide
# which function to call.
# ============================================================================
tools = [
    {
        "type": "function",
        "function": {
            "name": "validate_word",
            # ----------------------------------------------------------------
            # TODO 2: Write a clear description of WHAT this tool does and WHEN
            #         the AI should use it. The AI reads this to decide to call
            #         it — a good description = the AI uses the tool correctly.
            #   Example idea: "Check the player's 5-letter guess against the
            #   secret word and return color feedback. Call this every time the
            #   player makes a guess."
            # ----------------------------------------------------------------
            "description": "Check the player's 5-letter guess against the"
                "secret word and return color feedback. Call this every time the"
                "player makes a guess.",
            "parameters": {
                "type": "object",
                "properties": {
                    "guess": {
                        "type": "string",
                        "description": "The player's 5-letter guess",
                    }
                },
                "required": ["guess"],
            },
        },
    },
    {
        # 👇 This second tool is filled in for you as a WORKED EXAMPLE.
        #    Notice how it mirrors the shape of the tool above.
        "type": "function",
        "function": {
            "name": "end_game",
            "description": "Call this when the game is over: the player won, "
                           "ran out of guesses, or quit.",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "Why the game ended",
                        "enum": ["WON", "LOST", "QUIT"],
                    },
                    "answer": {
                        "type": "string",
                        "description": "The secret word",
                    },
                },
                "required": ["reason", "answer"],
            },
        },
    },
]


# ============================================================================
# THE MAIN EVENT — the agentic loop  (this is where YOUR steps go)
# ============================================================================
def play_wordle():
    secret_word = get_secret_word()
    print("🟩 Welcome to AI Wordle! I'm thinking of a 5-letter word.")
    print(f"You have {MAX_GUESSES} guesses.\n")
    # (Peeking is cheating, but for testing it helps to see the answer:)
    # print("psst... the word is", secret_word)

    # ------------------------------------------------------------------------
    # TODO 1: Write the system prompt. This is the AI's job description.
    #   Tell it: it is a Wordle game master, the SECRET word is `secret_word`,
    #   the player has MAX_GUESSES guesses, it should call validate_word() for
    #   each guess and call end_game() when the game is over. Use an f-string so
    #   you can drop `secret_word` and `MAX_GUESSES` into the text.
    # ------------------------------------------------------------------------
    system_prompt = (
        f"You are the AI Wordle Game Master. The player is trying to guess a secret 5-letter word.\n"
        f"The SECRET word is: '{secret_word}'\n"
        f"The player has a maximum of {MAX_GUESSES} guesses.\n\n"
        f"Rules of the game you must enforce:\n"
        f"1. When the player makes a guess, you MUST call the `validate_word` tool with their guess.\n"
        f"2. Present the results clearly using the emojis returned by the tool (🟩/🟨/⬜). Explain which letters are correct/misplaced/absent, and remind them of their remaining guesses.\n"
        f"3. If the guess is correct (i.e. all green: 🟩 🟩 🟩 🟩 🟩), you MUST call the `end_game` tool with reason='WON' and answer='{secret_word}'.\n"
        f"4. If they have used up all guesses and not won, you MUST call the `end_game` tool with reason='LOST' and answer='{secret_word}'.\n"
        f"5. If they wish to quit, call `end_game` with reason='QUIT' and answer='{secret_word}'.\n\n"
        f"Keep your responses friendly, encouraging, and clear."
    )

    # "messages" is the running conversation the AI can see. It starts with the
    # system prompt (the rules) and grows as the game is played.
    messages = [
        {"role": "system", "content": system_prompt},
    ]

    game_over = False
    guesses_used = 0

    # ---- THE AGENTIC LOOP --------------------------------------------------
    # Keep going until the game is over (or we hit a safety limit so we never
    # loop forever).
    while not game_over and guesses_used < MAX_GUESSES:
        # 1) Get the player's guess and add it to the conversation.
        guess = input("Your guess: ").strip().upper()
        guesses_used += 1
        messages.append({"role": "user", "content": f"My guess is: {guess}"})

        # --------------------------------------------------------------------
        # TODO 3: Ask the AI what to do. Call the model and let it use our tools.
        #   Fill in the blank so `response` holds the AI's reply. Hint:
        #
        #     response = client.chat.completions.create(
        #         model=MODEL,
        #         messages=messages,
        #         tools=tools,
        #     )
        # --------------------------------------------------------------------
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
        )  # TODO 3: replace None with the real model call (see hint)

        ai_message = response.choices[0].message

        # Save whatever the AI said/decided into the conversation history.
        messages.append({
            "role": "assistant",
            "content": ai_message.content or "",
            "tool_calls": ai_message.tool_calls,
        })

        # Did the AI decide to call one of our tools?
        if ai_message.tool_calls:
            for tool_call in ai_message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)  # the AI's chosen inputs

                if name == "validate_word":
                    # --------------------------------------------------------
                    # TODO 4: Run our validate_word() function and give the
                    #   result back to the AI. Look at the end_game example just
                    #   below to see the exact pattern to copy.
                    #   a) call validate_word(args["guess"], secret_word)
                    #   b) append a {"role": "tool", ...} message with the result
                    # --------------------------------------------------------
                    result = validate_word(args["guess"], secret_word)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": result,
                    })

                elif name == "end_game":
                    # 👇 WORKED EXAMPLE — copy this pattern for TODO 4 above.
                    result = end_game(args["reason"], args["answer"])
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": result,
                    })
                    # --------------------------------------------------------
                    # TODO 5: The game just ended — stop the loop.
                    #   Set game_over = True so the while-loop finishes.
                    # --------------------------------------------------------
                    game_over = True  # TODO 5: set game_over = True

            # After running the tool(s), ask the AI to say something to the
            # player (show the hint, celebrate, etc.). This is a second, quick
            # model call with no tools — just to get friendly text back.
            follow_up = client.chat.completions.create(model=MODEL, messages=messages)
            reply = follow_up.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            print(f"\n🤖 {reply}\n")

        else:
            # The AI just replied with text (no tool). Show it.
            print(f"\n🤖 {ai_message.content}\n")

    print("Thanks for playing! 🎮")


# This runs play_wordle() when you execute the file directly.
if __name__ == "__main__":
    play_wordle()