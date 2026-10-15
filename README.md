# AI Pythagoras Lab — Adaptive Math Learning

**Course:** Educational Technology & AI  
**Topic:** AI for Differentiated Learning  
**Grade / Math topic:** Grade 8 — Pythagorean Theorem  
**Author:** [Add your name]

## Overview
A Streamlit web app that generates a Pythagorean-theorem task at one of three difficulty levels using Gemini AI. Each task includes a differentiated hint, a verified step-by-step solution, and answer checking.

## Three levels
- **Foundation:** Short direct problem; find the hypotenuse with small integer lengths.
- **Standard:** Find a missing leg; use subtraction of squares.
- **Advanced:** Larger right triangles; missing leg, with more challenging numbers and contextual guidance.

## How to run locally
1. Install Python 3.10+.
2. In the project directory run `pip install -r requirements.txt`.
3. Get a Gemini API key from Google AI Studio.
4. Create `.streamlit/secrets.toml` using `.streamlit/secrets.toml.example` as a template. Insert your own key. **Never publish the key.**
5. Run `streamlit run app.py`.
6. Open the URL shown in the terminal (usually http://localhost:8501).

## Deployment (Streamlit Community Cloud)
1. Create a **public GitHub repository** and push the project files, excluding `.streamlit/secrets.toml`.
2. Visit https://share.streamlit.io/ and choose **Create app**.
3. Select your repository, branch, and `app.py` entry point.
4. In **Advanced settings / Secrets**, set `GEMINI_API_KEY = "YOUR_KEY"`.
5. Deploy and copy the public Streamlit URL into your assignment submission.
6. Include the GitHub repository link and `One_Page_Report.docx`.

## AI prompt design
See `prompts.py` for the exact system and generation prompts, and `PROMPT_LOG.md` for a documented explanation. The API is used on each generation in Gemini mode, not just for a static initial set of tasks.

## Reliability and integrity
- JSON response is schema-checked, including exact `a²+b²=c²` and level-specific rules.
- AI output is retried up to 3 times when invalid or repeated.
- The displayed question and solution are created from verified numbers by deterministic Python functions, reducing hallucination risk.
- The AI-supplied hint is pedagogical guidance and should be reviewed; free-form hint text cannot be completely mathematically verified.
- Offline mode is clearly labelled **practice only**, not AI integration.
- A repeated problem may occur after the finite set is exhausted; the API prompt requests novelty but cannot guarantee indefinite uniqueness.

## Tests
Run `python -m pytest -q` to verify arithmetic and input validation.

## Files
`app.py` — interface and Gemini connection  
`math_engine.py` — verification and calculations  
`prompts.py` — exact AI prompt templates  
`PROMPT_LOG.md` — prompts and design rationale  
`tests/` — automated tests  
`One_Page_Report.docx` — brief assignment report

## Limitations
The site cannot be deployed automatically from a downloaded folder: you must connect your own GitHub account, supply a Gemini key, and publish through Streamlit Cloud. Gemini may incur quota or pricing limits. The advanced level uses more difficult *single-triangle* problems, not multiple-step geometry; this is an intentional, clearly documented design choice.
