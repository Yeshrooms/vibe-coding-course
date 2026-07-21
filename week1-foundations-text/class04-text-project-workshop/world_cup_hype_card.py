"""
GSET Vibe Coding — Class 4 Project: World Cup Hype Card ⚽🔥
============================================================

What this program does:
  1. You pick the two finalist teams (below).
  2. Gemini writes a fun hype paragraph + fun facts + a score prediction.
  3. Gemini's "Nano Banana" image model draws a match poster (saved as poster.png).

------------------------------------------------------------
WHAT YOU NEED (requirements)
------------------------------------------------------------
  • The course libraries. If you followed the README setup, you already have them.
    If not, from the project's main folder run:

        conda activate gset-vibes
        pip install -r requirements.txt

    (This program uses two of those libraries: `google-genai` and `pillow`.)

  • Your Gemini API key saved in the `.env` file (see README Step 5). This program
    reads it automatically — you don't paste your key into the code. 🎉

------------------------------------------------------------
HOW TO RUN IT
------------------------------------------------------------
  From the project's main folder, with your `gset-vibes` environment active:

      python week1-foundations-text/class04-text-project-workshop/world_cup_hype_card.py

  The poster is saved as `poster.png` in whatever folder you ran the command from.
"""

# --- Libraries we use -------------------------------------------------------
import os
from dotenv import load_dotenv     # reads your GEMINI_API_KEY from the .env file
from google import genai           # the Gemini AI library
from PIL import Image              # Pillow: lets us save the generated poster image
from io import BytesIO             # turns raw image bytes into something Pillow can open

# Load the secret key from your .env file into the program.
load_dotenv()


# --- 0. Your settings — change these! ---------------------------------------
TEAM_A = "Argentina"          # <-- change to a real finalist
TEAM_B = "Spain"             # <-- change to the other finalist

TEXT_MODEL = "gemini-3.5-flash"          # the AI that writes the hype text
IMAGE_MODEL = "gemini-2.5-flash-image"   # "Nano Banana" — the AI that draws the poster


# --- 1. Connect to Gemini ---------------------------------------------------
# The client automatically finds your key from the .env file (the GEMINI_API_KEY line).
client = genai.Client()


# --- 2. Ask Gemini to write the hype text -----------------------------------
def get_hype_text(team_a, team_b):
    """Ask Gemini for a hype paragraph, fun facts, and a score prediction."""
    prompt = (
        f"You are a hype announcer for the {team_a} vs {team_b} World Cup final.\n"
        f"Write, in an energetic but friendly tone:\n"
        f"1. A 3-sentence hype paragraph for the match.\n"
        f"2. Two fun facts about each team (real, well-known facts).\n"
        f"3. A playful predicted final score, with one sentence explaining why.\n"
        f"Keep it appropriate for a classroom."
    )
    reply = client.models.generate_content(model=TEXT_MODEL, contents=prompt)
    return reply.text


# --- 3. Ask Gemini to draw the poster ---------------------------------------
def make_poster(team_a, team_b, filename="spain_vs_argentina.png"):
    """Ask Nano Banana to draw a match poster and save it to a file."""
    art_prompt = (
        f"A vibrant, exciting soccer match poster for the World Cup final: "
        f"{team_a} versus {team_b}. Show both teams' colors, a packed stadium "
        f"at night, dramatic lighting, bold graphic-design style. No real faces."
        f"yo its not in qatar its somewhere in new jersey or new york 2026 or sum"
        f"predict the score to be 1-0 spain"
        f"make it in a minimalistic absstract kinda art deco kinda vibe"
    )
    response = client.models.generate_content(model=IMAGE_MODEL, contents=art_prompt)

    # A response can contain several "parts" — some text, some image data.
    # We loop through them and save the first image we find.
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(filename)
            return filename   # success — hand back the file name

    return None               # no image came back this time


# --- 4. Put it all together -------------------------------------------------
def main():
    print(f"\n=== Making a hype card: {TEAM_A} vs {TEAM_B} ===\n")

    # The AI-written hype
    print(">> Asking Gemini for the hype...\n")
    hype = get_hype_text(TEAM_A, TEAM_B)
    print(hype)

    # The AI-generated poster
    print("\n>> Generating your match poster (this can take a few seconds)...\n")
    saved = make_poster(TEAM_A, TEAM_B)

    if saved:
        print(f">> Poster saved as {saved} — open it to see your card!")
    else:
        print(">> No image came back this time. Try running it again, or tweak the prompt.")

    print("\nDone! Now make it yours — see the stretch goals in this folder's README. 🚀\n")


# This line means: only run main() when we execute this file directly.
if __name__ == "__main__":
    main()
