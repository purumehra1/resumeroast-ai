import streamlit as st
import os
import plotly.graph_objects as go
import PyPDF2
import io

st.set_page_config(page_title="ResumeRoast AI", page_icon="🔥", layout="wide")
st.title("🔥 ResumeRoast AI")
st.caption("Upload your resume — get a brutal honest critique, score, and rewrite.")

GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

SAMPLE_RESUME = """John Doe | johndoe@email.com | +91-9876543210 | LinkedIn: linkedin.com/in/johndoe

EDUCATION
B.Tech Computer Science, SRM University, Chennai (2022-2026) | CGPA: 8.2

EXPERIENCE
Software Intern, ABC Tech (Jun-Aug 2025)
- Worked on backend systems
- Did some Python coding
- Helped the team with various tasks

SKILLS
Python, Java, C++, HTML, CSS, JavaScript, Machine Learning, Deep Learning

PROJECTS
1. Todo App - Made a todo app using React
2. Weather App - Gets weather data from API

ACHIEVEMENTS
- Participated in hackathon
- Got certificate in Python course
"""

def get_roast(resume_text, role, gemini_key):
    if gemini_key:
        try:
            import google.generativeai as genai
            genai.configure(api_key=gemini_key)
            model = genai.GenerativeModel('gemini-2.0-flash')
            prompt = f"""You are a brutally honest resume reviewer for {role} roles.

Resume:
{resume_text}

Provide:
1. ROAST: 3-4 sentences of honest, direct criticism (be specific, not mean)
2. SCORES (out of 10 each): Impact, Clarity, Skills Match, Formatting, ATS Optimization, Keywords
3. TOP 5 FIXES: Most impactful changes in order of priority
4. REWRITE: Improve the most important 3 bullet points from their experience

Format your response EXACTLY as:
ROAST: [your roast here]
IMPACT: [score]
CLARITY: [score]  
SKILLS: [score]
FORMATTING: [score]
ATS: [score]
KEYWORDS: [score]
FIX1: [fix]
FIX2: [fix]
FIX3: [fix]
FIX4: [fix]
FIX5: [fix]
REWRITE: [rewritten bullets]"""
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"API Error: {e}"
    else:
        return """ROAST: Your experience bullets read like a job description, not achievements. "Worked on backend systems" tells me nothing — what did you build, improve, or fix? The skills section is a keyword dump that will bore any recruiter. Your projects section needs numbers and impact, not just feature descriptions.
IMPACT: 3
CLARITY: 5
SKILLS: 4
FORMATTING: 6
ATS: 4
KEYWORDS: 5
FIX1: Replace vague verbs (worked, helped, did) with action verbs + metrics: "Reduced API response time by 40% by optimizing database queries"
FIX2: Add GitHub links and live demo URLs to every project
FIX3: Quantify everything: users, lines of code, performance gains, team size
FIX4: Tailor skills section to match job description keywords exactly
FIX5: Add a 2-line professional summary at the top
REWRITE: 
• Engineered RESTful backend services in Python (FastAPI) handling 1,000+ daily requests with 99.9% uptime
• Reduced page load time by 35% by implementing Redis caching and query optimization
• Built and deployed React weather dashboard with OpenWeather API — 50+ GitHub stars"""

def parse_response(text):
    result = {}
    lines = text.split('\n')
    for line in lines:
        for key in ['ROAST','IMPACT','CLARITY','SKILLS','FORMATTING','ATS','KEYWORDS',
                    'FIX1','FIX2','FIX3','FIX4','FIX5','REWRITE']:
            if line.startswith(key+':'):
                result[key] = line[len(key)+1:].strip()
                break
    # Handle multiline REWRITE
    if 'REWRITE' in text:
        result['REWRITE'] = text.split('REWRITE:')[-1].strip()
    return result

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Resume")
    role = st.selectbox("Target Role", ["Software Engineer", "Data Scientist", "ML Engineer",
                                         "Product Manager", "MBA / Business Analyst", "Full Stack Dev"])
    upload = st.file_uploader("Upload PDF", type=['pdf'])
    
    resume_text = ""
    if upload:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(upload.read()))
        resume_text = " ".join([page.extract_text() or "" for page in pdf_reader.pages])
        st.success(f"Extracted {len(resume_text.split())} words from PDF")
    
    use_sample = st.checkbox("Use sample resume (demo)")
    if use_sample:
        resume_text = SAMPLE_RESUME
        st.text_area("Sample Resume", SAMPLE_RESUME, height=200)
    
    if not GEMINI_KEY:
        gemini_input = st.text_input("Gemini API Key (optional — demo mode works without it)", type="password")
        active_key = gemini_input
    else:
        active_key = GEMINI_KEY
    
    roast_btn = st.button("🔥 Roast My Resume", type="primary", disabled=not resume_text)

with col2:
    if roast_btn and resume_text:
        with st.spinner("Analyzing your resume..."):
            raw = get_roast(resume_text, role, active_key)
            parsed = parse_response(raw)
        
        # Roast
        st.subheader("🔥 The Roast")
        st.error(parsed.get('ROAST', 'Could not parse roast.'))
        
        # Score radar
        scores = {
            'Impact':      int(parsed.get('IMPACT', 5)),
            'Clarity':     int(parsed.get('CLARITY', 5)),
            'Skills':      int(parsed.get('SKILLS', 5)),
            'Formatting':  int(parsed.get('FORMATTING', 5)),
            'ATS':         int(parsed.get('ATS', 5)),
            'Keywords':    int(parsed.get('KEYWORDS', 5)),
        }
        total = round(sum(scores.values()) / 6 * 10)
        
        col_s, col_r = st.columns([1,2])
        with col_s:
            st.metric("Overall Score", f"{total}/100",
                      delta="needs work" if total < 60 else "decent" if total < 80 else "strong")
        with col_r:
            fig = go.Figure(go.Scatterpolar(
                r=list(scores.values()), theta=list(scores.keys()),
                fill='toself', fillcolor='rgba(255,80,50,0.2)',
                line=dict(color='#ff5032', width=2)
            ))
            fig.update_layout(polar=dict(radialaxis=dict(range=[0,10])),
                              showlegend=False, height=220,
                              margin=dict(l=30,r=30,t=30,b=30),
                              paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        # Fixes
        st.subheader("💡 Top 5 Fixes")
        for i in range(1, 6):
            fix = parsed.get(f'FIX{i}', '')
            if fix:
                st.write(f"**{i}.** {fix}")
        
        # Rewrite
        st.subheader("✍️ AI Rewrite")
        st.success(parsed.get('REWRITE', 'No rewrite generated.'))
    elif not roast_btn:
        st.info("Upload a resume or check 'Use sample resume' to get started.")

st.divider()
st.caption("Puru Mehra | github.com/purumehra1/resumeroast-ai")
