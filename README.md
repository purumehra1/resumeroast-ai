# 🔥 ResumeRoast AI

![Python](https://img.shields.io/badge/Python-3.10+-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)

**Brutally honest AI resume reviewer.** Upload your PDF resume and get a score, roast, and improved rewrite — in seconds.

## Features
- 📄 Upload PDF or paste resume text
- 🔥 Brutal honest critique (no sugar-coating)
- 📊 Score out of 100 across 6 dimensions: Impact, Clarity, Skills, Formatting, ATS, Keywords
- ✍️ AI-rewritten improved version
- 💡 Top 5 actionable fixes
- 🎯 Role-specific feedback (SWE, Data, Product, MBA)

## Tech Stack
- **Google Gemini 2.0 Flash** — AI analysis & rewrite
- **PyPDF2** — PDF text extraction
- **Streamlit** — UI
- **Plotly** — score radar chart

## Run
```bash
pip install -r requirements.txt
GEMINI_API_KEY=your_key streamlit run app.py
```

## Author
Puru Mehra — BTech CSE (AIML), SRM Chennai | [github.com/purumehra1](https://github.com/purumehra1)
