import os
import uuid
import json
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Import the core logic from our existing terminal agent
# This keeps the EXACT same backend tools and architecture!
from wordle_agent_starter import (
    validate_word,
    end_game,
    get_secret_word,
    tools,
    MODEL,
    MAX_GUESSES,
    client
)

# Load environment variables
load_dotenv()

# Verify API key is present
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

# Initialize Flask application
app = Flask(__name__)
CORS(app)

# In-memory database to store active game sessions
# This allows multiple people to play at the same time without cross-talk
active_sessions = {}

def get_feedback_list(guess, secret):
    """
    Compare a 5-letter guess to the secret word and return a list of color classes
    for CSS styling.
    - 'green': Correct letter, correct position
    - 'yellow': Correct letter, wrong position
    - 'gray': Letter is not in the word
    """
    guess = guess.strip().upper()
    secret = secret.strip().upper()
    feedback = []
    
    # We do a two-pass calculation or standard validation to match Wordle logic
    for i in range(5):
        if guess[i] == secret[i]:
            feedback.append("green")
        elif guess[i] in secret:
            feedback.append("yellow")
        else:
            feedback.append("gray")
    return feedback

@app.route("/")
def home():
    """Serve the main play page."""
    return render_template("index.html")

@app.route("/api/start", methods=["POST"])
def start_game():
    """
    Starts a new Wordle game session.
    - Generates a unique session ID
    - Selects a secret 5-letter word
    - Generates the system prompt instructing the AI Master of the rules and secret word
    - Calls Gemini to generate a customized welcoming greeting
    """
    session_id = str(uuid.uuid4())
    secret_word = get_secret_word()
    
    # Define a clean, powerful f-string system prompt for the AI
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
        f"Keep your responses friendly, encouraging, clear, and concise."
    )
    
    # Initialize message history
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Warm up the AI and get a welcoming greeting for the player
    welcome_prompt = "Hello! I am ready to start playing AI Wordle. Introduce yourself as the Game Master and prompt me for my first guess."
    messages.append({"role": "user", "content": welcome_prompt})
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        ai_greeting = response.choices[0].message.content
        messages.append({"role": "assistant", "content": ai_greeting})
    except Exception as e:
        ai_greeting = f"Welcome to AI Wordle! I'm your AI Game Master. Let's play! Enter your first 5-letter guess."
    
    # Save session state
    active_sessions[session_id] = {
        "secret_word": secret_word,
        "guesses_used": 0,
        "game_over": False,
        "status": "PLAYING",
        "messages": messages,
        "board": []
    }
    
    return jsonify({
        "session_id": session_id,
        "max_guesses": MAX_GUESSES,
        "greeting": ai_greeting,
        "board": []
    })

@app.route("/api/guess", methods=["POST"])
def submit_guess():
    """
    Submits a 5-letter guess and runs one full turn of the agentic loop.
    - Decides whether to invoke tools (validate_word, end_game)
    - Captures "AI thoughts" and "tool executions" for visual logs
    - Returns updated board states, agent logs, and next AI reply
    """
    data = request.json or {}
    session_id = data.get("session_id")
    guess = data.get("guess", "").strip().upper()
    
    if not session_id or session_id not in active_sessions:
        return jsonify({"error": "Invalid or expired game session."}), 404
        
    session = active_sessions[session_id]
    
    if session["game_over"]:
        return jsonify({"error": "The game has already ended."}), 400
        
    if len(guess) != 5:
        return jsonify({"error": "Guess must be exactly 5 letters long."}), 400

    # 1) Increment guesses and append user's guess to messages
    session["guesses_used"] += 1
    session["messages"].append({"role": "user", "content": f"My guess is: {guess}"})
    
    # We will accumulate visual logs/thoughts to display in the UI's AI Brain Console
    logs = []
    logs.append({"type": "thought", "content": f"Analyzing user's guess '{guess}' (Guess {session['guesses_used']}/{MAX_GUESSES})..."})
    
    try:
        # 2) Let Gemini call our tools
        logs.append({"type": "thought", "content": "Invoking Gemini model with available tools list..."})
        response = client.chat.completions.create(
            model=MODEL,
            messages=session["messages"],
            tools=tools
        )
        
        ai_message = response.choices[0].message
        
        # Save whatever the AI decided initially
        session["messages"].append({
            "role": "assistant",
            "content": ai_message.content or "",
            "tool_calls": ai_message.tool_calls
        })
        
        # Check if the AI wants to use tools
        if ai_message.tool_calls:
            logs.append({"type": "thought", "content": f"Gemini decided to take action and call {len(ai_message.tool_calls)} tool(s)."})
            
            for tool_call in ai_message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                logs.append({
                    "type": "tool_call",
                    "content": f"Executing local tool: `{name}` with arguments {json.dumps(args)}"
                })
                
                if name == "validate_word":
                    # Run our validate function!
                    result = validate_word(args["guess"], session["secret_word"])
                    session["messages"].append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": result
                    })
                    
                    logs.append({
                        "type": "tool_response",
                        "content": f"Tool `validate_word` returned: '{result}'"
                    })
                    
                    # Update board state
                    colors = get_feedback_list(args["guess"], session["secret_word"])
                    session["board"].append({
                        "guess": args["guess"],
                        "colors": colors
                    })
                    
                elif name == "end_game":
                    result = end_game(args["reason"], args["answer"])
                    session["messages"].append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": name,
                        "content": result
                    })
                    
                    logs.append({
                        "type": "tool_response",
                        "content": f"Tool `end_game` returned: '{result}'"
                    })
                    
                    session["game_over"] = True
                    session["status"] = args["reason"]
            
            # Enforce safety-net check: if guess was correct but end_game wasn't called,
            # or if guesses are exhausted
            if guess == session["secret_word"]:
                session["game_over"] = True
                session["status"] = "WON"
            elif session["guesses_used"] >= MAX_GUESSES and not session["game_over"]:
                session["game_over"] = True
                session["status"] = "LOST"
                
            # 3) Call Gemini again to format a friendly follow-up response
            logs.append({"type": "thought", "content": "Sending tool outputs back to Gemini to synthesize response..."})
            follow_up = client.chat.completions.create(
                model=MODEL,
                messages=session["messages"]
            )
            reply = follow_up.choices[0].message.content
            session["messages"].append({"role": "assistant", "content": reply})
            logs.append({"type": "text", "content": reply})
            
        else:
            # The AI answered without calling tools (rare, but can happen if input was invalid)
            reply = ai_message.content or "No response from Game Master."
            logs.append({"type": "text", "content": reply})
            
            # Safety checks for out-of-guesses
            if session["guesses_used"] >= MAX_GUESSES:
                session["game_over"] = True
                session["status"] = "LOST"
                
    except Exception as e:
        reply = f"Error communicating with AI: {str(e)}"
        logs.append({"type": "thought", "content": f"Error during agentic execution: {str(e)}"})
        
        # Local fallback if API fails completely so the user can still play
        colors = get_feedback_list(guess, session["secret_word"])
        session["board"].append({
            "guess": guess,
            "colors": colors
        })
        if guess == session["secret_word"]:
            session["game_over"] = True
            session["status"] = "WON"
            reply = "🎉 Correct! You've guessed the word!"
        elif session["guesses_used"] >= MAX_GUESSES:
            session["game_over"] = True
            session["status"] = "LOST"
            reply = f"😔 Game Over! Out of guesses. The word was {session['secret_word']}."
        else:
            reply = f"Here is your feedback: {' '.join(colors).upper()}"
            
    return jsonify({
        "board": session["board"],
        "reply": reply,
        "game_over": session["game_over"],
        "status": session["status"],
        "guesses_used": session["guesses_used"],
        "logs": logs,
        "secret_word": session["secret_word"] if session["game_over"] else None
    })

@app.route("/api/hint", methods=["POST"])
def get_hint():
    """
    Generates a clever, contextual hint without revealing the secret word.
    - Inspects the active session state
    - Instructs Gemini to look at the secret word and previous guesses to construct an encouraging clue
    - Returns the hint as a conversational speech bubble and logs
    """
    data = request.json or {}
    session_id = data.get("session_id")
    
    if not session_id or session_id not in active_sessions:
        return jsonify({"error": "Invalid or expired game session."}), 404
        
    session = active_sessions[session_id]
    
    if session["game_over"]:
        return jsonify({"error": "The game has already ended."}), 400
        
    logs = []
    logs.append({"type": "thought", "content": "Analyzing current progress to generate a helpful hint..."})
    logs.append({"type": "thought", "content": f"Retrieving dictionary entries. Secret word is '{session['secret_word']}'."})
    
    # We construct a short prompt instructing Gemini to write a riddle or clue
    hint_prompt = (
        f"The player is asking for a helper hint. The secret 5-letter word is '{session['secret_word']}'.\n"
        f"Please write a witty, encouragement-focused hint or short riddle about this word. "
        f"WARNING: Do NOT reveal the word directly under any circumstances. "
        f"Keep your response to exactly 1 or 2 friendly sentences."
    )
    
    # Perform a standalone completion query using current session logs + hint instruction
    temp_messages = session["messages"] + [{"role": "user", "content": hint_prompt}]
    
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=temp_messages
        )
        hint_text = response.choices[0].message.content
        logs.append({"type": "thought", "content": "Gemini formulated a cryptic clue successfully."})
        logs.append({"type": "text", "content": hint_text})
        
        # Append the advisor hint to standard messages to keep convo thread complete
        session["messages"].append({"role": "assistant", "content": f"[Advisor Hint Provided] {hint_text}"})
    except Exception as e:
        hint_text = f"I can tell you that the secret word starts with the letter '{session['secret_word'][0].upper()}'!"
        logs.append({"type": "thought", "content": f"Hint API fallback activated: {str(e)}"})
        
    return jsonify({
        "hint": hint_text,
        "logs": logs
    })

# Prevent browsers from caching our styling and script updates during development
@app.after_request
def add_header(response):
    """
    Instructs the user's browser not to cache any responses.
    This guarantees that every single page refresh fetches the absolute latest
    CSS styling and JavaScript logic from our files.
    """
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

if __name__ == "__main__":
    # Standard Flask development port
    app.run(host="127.0.0.1", port=5000, debug=True)
