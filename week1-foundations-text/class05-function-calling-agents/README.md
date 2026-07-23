# Class 5 — Function Calling & Agentic Loops 🛠️🔁

**Your mission:** use **Google Antigravity** to *vibe code* a small **web app** where an AI
doesn't just chat — it **uses tools** and **works in a loop** to get something done.

So far you've made Gemini **write text** (Class 3) and **make images** (Class 4). Today you
level up: you'll build an app where the AI can **call your Python functions** and keep
**taking actions on its own** until a job is finished. This is the core idea behind every
"AI agent" you hear about.

> **You are the architect, Antigravity is the builder.** You won't type most of the code by
> hand. You'll describe what you want, review Antigravity's plan, run the app, and refine.
> The skill you're practicing is *directing an AI to build software* — that's vibe coding. 🎸

---

## 🚦 Step 1 — Open your workspace

1. **Open the course folder in your IDE** (VS Code, Cursor, or Antigravity):
   **File → Open Folder…** and choose your `vibe-coding-course` folder.
2. **Open a terminal inside your IDE:** the menu **Terminal → New Terminal**
   (or press `` Ctrl + ` ``). It opens already inside the project folder.

---

## ⬇️ Step 2 — Get the new Class 5 files (with Git)

These files were added to the shared course repo, so you need to **pull** them onto your
computer. You may have your own unfinished work from earlier classes — don't worry, these
steps **save your work first** so nothing is lost. 🛟

### The easy way — use your IDE's buttons (recommended if Git is new to you)
1. Open the **Source Control** panel (the branch-looking icon on the left sidebar, or press
   `Ctrl+Shift+G`).
2. If it lists any changed files, type a short message like `my work` in the box and click
   **✔ Commit**. (This saves a snapshot of your work.)
3. **Switch to the `main` branch** if you're on your own branch: click the branch name in the
   **bottom-left corner** of the window and pick **`main`** from the list.
4. Click the **… menu → Pull** (or the **Sync Changes** / circular-arrows button).
5. When it finishes, the `week1-foundations-text/class05-function-calling-agents/` folder will
   appear in your file list. 🎉

### The terminal way — copy/paste these lines
Run them one at a time (they work from anywhere inside the project folder):

```bash
git add -A
git commit -m "Save my work before pulling Class 5"
git checkout main
git pull --no-edit origin main
```

- Lines 1–2 **save your own work** (even half-finished edits) into a snapshot so it's safe.
- Line 3 **switches you to the `main` branch** — in case you were working on your own branch.
- Line 4 **downloads the new class files** and blends them in.

> 💬 **What if a line says "nothing to commit"?** Great — that just means you had no unsaved
> changes. Skip ahead to the `git checkout main` line.
>
> 💬 **What if it mentions a "merge conflict"?** That's rare here because Class 5 is a brand-new
> folder. If it happens, don't panic — ask your instructor for a hand.

---

## 🐍 Step 3 — Turn on the environment, then go to the Class 5 folder

1. **Turn on the course environment** (Python 3.10 with all our AI libraries). Type this and
   press Enter:

```bash
conda activate gset-vibes
```

   ✅ You'll know it worked when you see **`(gset-vibes)`** at the start of your terminal line.
   If you get "conda: command not found" or the environment doesn't exist, redo Step 3 of the
   main [README](../../README.md).

   > 🪟 **Windows:** if `conda activate` doesn't work in a normal terminal, open the app called
   > **Anaconda Prompt** and run the command there.

2. **Install the libraries** (this makes sure you have everything today's code needs):

```bash
pip install -r requirements.txt
```

   > You only need to run this once (or again later if a new library is ever added). If it
   > prints a lot of "already satisfied" lines, that's fine — it just means you're up to date.

3. **Go into the Class 5 folder** so the commands below are nice and short:

```bash
cd week1-foundations-text/class05-function-calling-agents
```

   > From now on, run every command in this README **from inside this folder**. To get back
   > to the project's main folder later, type `cd ../..`.

---

## 🧠 The big ideas you're showing off

### 1. Function calling ("tools")
Normally the AI can only *talk*. **Function calling** lets you hand the AI a menu of Python
functions ("tools") it's allowed to run — like `validate_word(guess)` or
`get_weather(city)`. The AI reads the situation, **decides which tool to call and with what
inputs**, your code runs the real function, and the result gets handed back to the AI.

> Think of it like giving the AI hands. Chatting = talking. Tools = *doing*.

### 2. Agentic loop
A single tool call is nice, but real agents **keep going**. An **agentic loop** is just a
`while` loop that repeats:

```
while not done:
    1. Ask the AI what to do next
    2. If it wants to use a tool → run that tool, give it the result
    3. Repeat until the goal is reached (then stop the loop)
```

That loop is what lets an AI play a whole game of Wordle, or look up a city *and then* fetch
its weather *and then* answer you — several steps, no human nudging each one.

### 3. RAG: fewer made-up answers (a.k.a. fixing "hallucinations")
Ask an AI a hard fact and it will sometimes **hallucinate** — confidently make something up.
That's because a plain language model is answering from fuzzy memory of its training data,
which can be outdated or just wrong.

**RAG** (*Retrieval-Augmented Generation*) fixes this by combining the two ideas above:

1. **Retrieve** — the agent uses a *tool* to go get **real, current facts** (search
   Wikipedia, call a weather API, read a file).
2. **Augment** — those facts are added into the conversation the AI can see.
3. **Generate** — the AI writes its answer **using those facts**, and can **cite the source**.

> 🧠 In short: tools + a loop let the AI *look things up instead of guessing*. Grounding the
> answer in retrieved facts is the single most effective way to reduce hallucinations. Even
> the Wordle and weather apps use this idea — the AI never *guesses* the feedback or the
> forecast, it gets the truth from your `validate_word` / `get_forecast` tool.

**How you make it happen is mostly in the prompt.** You explicitly *instruct* the AI to stay
grounded. Good rules to put in your system prompt:
- "Do **not** rely on your own knowledge — it may be outdated. **Use the tools** to find facts."
- "Answer **only** using what the tools returned. If the facts aren't there, **search again**
  or say you don't know — **never make it up**."
- "**Cite the source** (include the link/data you used)."

> You saw all three ideas live in class yesterday.

---

## 🔑 Step 4 — Add your Gemini API key

Make a copy of the key template (you're inside the Class 5 folder now):

```bash
cp .env.example .env
```

Then open the new `.env` file and paste your key after `GEMINI_API_KEY=`. Never paste your key
into the code itself — the program reads it from `.env` automatically. 🎉

> You'll also need **Google Antigravity** installed and signed in for Phase 2. If you haven't
> yet, follow [docs/antigravity-tips.md](../../docs/antigravity-tips.md).

---

## 🎯 The assignment — two phases

You'll do this in **two phases**, and we give you **starter code** to make Phase 1 easy:

- **Phase 1 — Make the "brain" work in the terminal.** Open the starter `.py` file for your
  project and complete the 5 small `TODO` steps. Most of the code is already written for you
  ("BUILDING BLOCK"s) — you just wire up the tool and the loop. Run it in the terminal until
  it works.
- **Phase 2 — Give it a face with Antigravity.** Once the brain works, use Antigravity to
  wrap it in a **web app** you can use in the browser. (See the workflow below.)

Pick ONE project:

### Option A — AI Wordle Game Master 🟩 (recommended starter)
An AI runs a game of Wordle. You type 5-letter guesses; the AI uses a `validate_word` tool to
check each guess and show color feedback (🟩🟨⬜), looping until you win or run out of guesses,
then calls an `end_game` tool.
- **Starter file:** [`wordle_agent_starter.py`](wordle_agent_starter.py) — do the 5 TODOs.
- **Already done for you:** the game logic (`validate_word`, `end_game`) and a word list
  (`wordle.txt`, 2,314 words).
- **You wire up:** the AI's instructions, one tool, and the guessing loop.

### Option B — Weather Assistant ⛅ (real external API, no key needed!)
Ask a question in plain English ("Do I need an umbrella in Paris tomorrow?") and the AI
answers by calling tools that hit the **free, no-signup** [Open-Meteo](https://open-meteo.com)
API.
- **Starter file:** [`weather_agent_starter.py`](weather_agent_starter.py) — do the 5 TODOs.
- **Already done for you:** the two API tools (`find_city`, `get_forecast`) — no key needed.
- **You wire up:** the AI's instructions, one tool, and a multi-step loop (find city → get
  forecast → answer). This is a great example of the AI taking **several steps on its own**.

### Option C — Wikipedia Research Agent 📚 (the RAG one!)
Ask a factual question ("How tall is Mount Everest?") and the AI **looks it up on Wikipedia**
instead of guessing — then answers **with a source link**. This is RAG in action, and the
clearest way to *see* an agent avoid hallucinating.
- **Starter file:** [`research_agent_starter.py`](research_agent_starter.py) — do the 5 TODOs.
- **Already done for you:** the `search_wikipedia` tool (returns a summary + source URL).
- **You wire up:** the AI's instructions, one tool, and a loop that keeps searching until it
  can answer. **TODO 1 is the star here** — it's where you write the anti-hallucination rules.

### Option D — Your own agent 💡
Anything you like that hits the checklist below. Start by copying one of the starter files and
swapping in your own tools. Ideas: a trivia host that checks answers, a "20 Questions" bot, a
tip/bill-splitting agent, a unit-converter agent, a to-do assistant.

### ✔️ Definition of done (your app must have ALL of these)
- [ ] It **runs in a web browser** (a simple page you can click/type into).
- [ ] The AI uses **at least one tool** (function calling) that runs *your* Python code.
- [ ] There's an **agentic loop** — the AI can take **more than one step** without you
      editing code between steps.
- [ ] The Gemini key is loaded from **`.env`** (never hard-coded).
- [ ] You can **explain, in your own words**, where the tool call and the loop happen. 🗣️

---

## 🧪 Phase 1 — Get the brain working in the terminal

1. Open your starter file (`wordle_agent_starter.py`, `weather_agent_starter.py`, or
   `research_agent_starter.py`).
2. Read the comments from top to bottom — the "BUILDING BLOCK" parts are already done.
3. Complete the **5 TODOs** (search the file for `TODO`). They're small and in order.
4. Run it (from inside the Class 5 folder) and test it:

```bash
python wordle_agent_starter.py
```

> Stuck on a TODO? Read the hint right next to it, and look at the **worked example** — each
> starter fills in one tool completely so you can copy the pattern for yours. You can also ask
> Antigravity: *"Explain what TODO 3 is asking me to do in simple terms."*

---

## ✅ Test your work (test cases)

### Step 1 — Run the automatic self-check
Each project comes with a little test script that checks the "building block" functions for
you (no AI needed). Run the one for your project:

```bash
# Wordle:
python test_wordle.py

# Weather (needs internet):
python test_weather.py

# Research / RAG (needs internet):
python test_research.py
```

You should see a list of **✅ PASS** lines. A **❌ FAIL** line tells you exactly what was
expected, so you know what to fix.

### Step 2 — Try these by hand (after you finish the TODOs)
Run your program and try each row. This is how you check the AI is really using the tool and
the loop:

**Wordle** — `python wordle_agent_starter.py`

| Type this guess | What should happen |
| --------------- | ------------------ |
| `CAT` (not 5 letters) | The AI asks you to try again; it shouldn't count as a real guess |
| `CRANE` (a normal guess) | The AI shows 🟩 / 🟨 / ⬜ feedback for each letter |
| the **correct** word | The AI congratulates you and the game **ends** (🎉) |
| six wrong guesses | The AI ends the game and reveals the word |

**Weather** — `python weather_agent_starter.py`

| Ask this | What should happen |
| -------- | ------------------ |
| `What's the weather in Tokyo?` | You see it use `find_city` **then** `get_forecast`, then it answers |
| `Do I need an umbrella in London tomorrow?` | It checks the rain chance and answers yes/no |
| `Is it hotter in Cairo or Oslo right now?` | It looks up **both** cities and compares |
| `What's the weather in Zzzxqq?` | It says it can't find that city (no crash) |

**Research (RAG)** — `python research_agent_starter.py`

| Ask this | What should happen |
| -------- | ------------------ |
| `How tall is Mount Everest?` | It searches Wikipedia, then answers **with a source link** |
| `Who wrote Romeo and Juliet?` | It answers from the article, not from memory |
| `What is the capital of Australia?` | It answers **Canberra** (not the common wrong guess) and cites it |
| `What is a florbnax?` (made-up) | It searches, finds nothing, and says it can't find it — it does **not** invent an answer |

> 👀 Watch the terminal! When it prints lines like `🔧 AI is using tool: find_city(...)` or
> `🔎 Searching Wikipedia for: ...`, that's your **agentic loop** working — the AI choosing
> tools and taking steps on its own. And for the research agent, the *source link* in the
> answer is your proof that RAG kept it honest. ✅

---

## 🚀 Phase 2 — Give it a face with Antigravity (the vibe-coding workflow)

1. **Open this course folder in Antigravity** and make sure your `.env` (with your key) is in
   this Class 5 folder.

2. **Use Planning mode.** Let the agent write a **plan first** so you can read and approve it
   *before* it changes code. (See the Antigravity tips doc.)

3. **Point it at your working starter and ask for a web app.** Copy one of these into the
   agent and edit to taste:

   > **Wordle prompt:** "I have a working terminal program in
   > `wordle_agent_starter.py` that uses Gemini function calling to run a game of Wordle. Turn
   > it into a small Flask web app I can play in the browser. Keep the same tools
   > (`validate_word`, `end_game`) and the agentic loop. Read `GEMINI_API_KEY` from `.env` with
   > python-dotenv — never hard-code the key. Make a clean, colorful Wordle-style page and
   > explain the code to me like I'm new to programming."

   > **Weather prompt:** "I have a working terminal program in
   > `weather_agent_starter.py` that uses Gemini function calling with the free Open-Meteo API.
   > Turn it into a small Flask web app where I type a weather question and see the answer.
   > Keep the same tools (`find_city`, `get_forecast`) and the agentic loop, and keep reading
   > `GEMINI_API_KEY` from `.env`. Make a clean page and explain the code simply."

   > **Research prompt:** "I have a working terminal program in
   > `research_agent_starter.py` that uses Gemini function calling to answer questions from
   > Wikipedia (RAG). Turn it into a small Flask web app where I type a question and see the
   > answer **with its source link shown**. Keep the same `search_wikipedia` tool, the agentic
   > loop, and the anti-hallucination system prompt, and keep reading `GEMINI_API_KEY` from
   > `.env`. Make a clean page and explain the code simply."

4. **Read the Artifacts, then run it.** When Antigravity finishes, skim its plan/task list,
   then actually run the app and try it yourself. **Running your code is how you catch
   mistakes** — don't just trust it. (If a model name errors, swap in a current one from the
   [Gemini models list](https://ai.google.dev/gemini-api/docs/models).)

5. **Iterate in small, specific asks.** "Add a guess counter." "Make wrong guesses shake."
   "Show the AI's reasoning in a side panel." Small prompts beat "make it better."

6. **(Pro tip) Add a rule so Antigravity stays on-brand.** Create `.agent/rules/course.md`
   with standing instructions like: *"Always read the Gemini key from `.env` with
   python-dotenv; never hard-code keys. Explain new code in simple terms for a beginner."*

---

## 🧩 Stretch goals (if you finish early)
- **Flip Wordle:** make the AI **play** Wordle by itself — it guesses, reads the 🟩🟨⬜ hints,
  and keeps refining in the loop until it wins. (A pure agentic loop!)
- **Add a second tool.** e.g. a `get_hint()` tool in Wordle, or a `suggest_outfit()` tool in
  the weather app.
- **Show the AI's thinking.** Print each tool the AI decides to call so you can *watch the
  loop* happen on screen.
- **Make it multimodal.** Use what you learned in Class 4 to generate an image (a Wordle
  victory poster, or weather art for the city).

---

## 🆘 Common problems
- **"GEMINI_API_KEY not found" / auth error** — Your `.env` is missing or the key is wrong.
  Make sure `.env` is in this folder and the key has no quotes around it.
- **A model name error** — Model names change. Update the model to a current one from the
  [Gemini models list](https://ai.google.dev/gemini-api/docs/models).
- **"Port already in use"** — Another app is on that port. Ask Antigravity to run on a
  different port (e.g. 5002), or close the other app.
- **The AI never calls the tool** — Your tool's `description` probably isn't clear. Make the
  description say exactly *when* to use it, and tell the AI in the system prompt that it must
  use tools instead of guessing.
- **The loop never stops (or stops too early)** — Make sure there's a clear "we're done"
  signal (like an `end_game` tool or an all-green result) and a max number of turns as a
  safety net.

---

## 📥 What to turn in
- Your working web app (the files Antigravity created in this folder).
- A **2–3 sentence note** answering: *Where does the AI call a tool? Where is the agentic
  loop? What's one thing you changed after your first run?*

---

## 📤 Save and share your finished work with Git

When your app works, put it on **your own branch**. A branch is a separate copy of the
project where you can safely save and share your changes without changing the shared `main`
branch.

> ⚠️ Never commit your `.env` file — it contains your private Gemini API key. The course
> `.gitignore` should protect it, but always check the file list before committing.

From the project’s main folder, run these commands one at a time:

```bash
git checkout -b class5-your-name
git status
git add week1-foundations-text/class05-function-calling-agents
git commit -m "Build Class 5 AI agent app"
git push -u origin class5-your-name
```

Replace `your-name` with your own name, using lowercase letters and hyphens — for example,
`class5-maya-chen`.

- `git checkout -b ...` creates your new branch and moves you onto it.
- `git status` shows what will be saved. **Check that `.env` is not listed.**
- `git add ...` selects only your Class 5 work, not unfinished work from other classes.
- `git commit ...` saves a snapshot of that work.
- `git push ...` uploads your branch to GitHub.

After the push, GitHub may show a link to make a **Pull Request**. Only create one if your
instructor asks for it; otherwise, your branch is your submitted backup.

---

## 🔗 Handy links
- [Google Antigravity tips (our cheat sheet)](../../docs/antigravity-tips.md)
- [Class 3 code — Wordle & researcher examples](../class03-text-generation/intro_to_gemini.py)
- [Gemini function calling docs](https://ai.google.dev/gemini-api/docs/function-calling)
- [Gemini models list](https://ai.google.dev/gemini-api/docs/models)
- [Open-Meteo weather API (free, no key)](https://open-meteo.com/en/docs)

**Now go direct your AI teammate — and build something that *does* things. 🚀**