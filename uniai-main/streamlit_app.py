import os
import re
import streamlit as st
import google.generativeai as genai

# ─────────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="UniAi – Find Your Future University",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────
# Custom CSS – Premium Dark-Blue Theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
}

/* ── Remove Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 0 !important; padding-bottom: 0 !important; }

/* ── Full-page gradient background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #0d1b3e 40%, #091930 100%) !important;
    min-height: 100vh;
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(0,51,102,0.85) 0%, rgba(0,30,80,0.92) 100%),
                url('https://images.unsplash.com/photo-1523050854058-8df90110c9f1?q=80&w=2070&auto=format&fit=crop') center/cover no-repeat;
    padding: 3.5rem 2rem 2.5rem;
    text-align: center;
    border-radius: 0 0 30px 30px;
    margin-bottom: 2rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.5);
}
.hero-banner .logo {
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: 4px;
    color: #ffc107;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-banner h1 {
    font-size: 3rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0 0 0.5rem;
    text-shadow: 0 4px 20px rgba(0,0,0,0.4);
}
.hero-banner p {
    font-size: 1.1rem;
    color: rgba(255,255,255,0.75);
    margin: 0;
}

/* ── Form Card ── */
.form-card {
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 20px;
    padding: 2.5rem 2.5rem 2rem;
    margin: 0 auto 2.5rem;
    max-width: 1100px;
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}
.form-card h3 {
    color: #ffc107;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

/* ── Streamlit widget overrides ── */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stTextInput"] > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}
div[data-testid="stSelectbox"] > div > div:hover,
div[data-testid="stTextInput"] > div > div > input:focus {
    border-color: #ffc107 !important;
    box-shadow: 0 0 0 2px rgba(255,193,7,0.25) !important;
}
label[data-testid="stWidgetLabel"] p,
.stSelectbox label, .stTextInput label {
    color: rgba(255,255,255,0.85) !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
/* Dropdown option text */
div[data-testid="stSelectbox"] span {
    color: #ffffff !important;
}

/* ── Search Button ── */
.stButton > button {
    background: linear-gradient(135deg, #ffc107, #ff9800) !important;
    color: #001f3f !important;
    font-weight: 800 !important;
    font-size: 1rem !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.8rem 2.5rem !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 20px rgba(255,193,7,0.35) !important;
    width: 100% !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(255,193,7,0.5) !important;
}

/* ── Results Section ── */
.results-title {
    text-align: center;
    color: #ffffff;
    font-size: 2rem;
    font-weight: 800;
    margin: 1rem 0 0.5rem;
}
.disclaimer-box {
    background: linear-gradient(135deg, rgba(255,193,7,0.15), rgba(255,152,0,0.1));
    border-left: 4px solid #ffc107;
    border-radius: 10px;
    padding: 1rem 1.5rem;
    color: rgba(255,255,255,0.9);
    font-size: 0.9rem;
    margin: 0 auto 2rem;
    max-width: 900px;
}

/* ── University Card ── */
.uni-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.08), rgba(255,255,255,0.04));
    backdrop-filter: blur(15px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.uni-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: linear-gradient(180deg, #ffc107, #ff9800);
    border-radius: 16px 0 0 16px;
}
.uni-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.3);
    border-color: rgba(255,193,7,0.3);
}
.uni-card h4 {
    color: #ffffff;
    font-size: 1.1rem;
    font-weight: 700;
    margin: 0 0 0.4rem 0.8rem;
}
.uni-card .city-tag {
    color: #ffc107;
    font-size: 0.85rem;
    font-weight: 500;
    margin-left: 0.8rem;
    margin-bottom: 0.8rem;
}
.uni-card .tuition-tag {
    background: rgba(255,193,7,0.15);
    color: #ffc107;
    border-radius: 20px;
    padding: 0.25rem 0.85rem;
    font-size: 0.82rem;
    font-weight: 600;
    display: inline-block;
    margin-left: 0.8rem;
    margin-bottom: 0.8rem;
}
.uni-card .visit-btn {
    display: inline-block;
    background: linear-gradient(135deg, #003366, #005a9e);
    color: #ffffff;
    text-decoration: none;
    padding: 0.45rem 1.1rem;
    border-radius: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-left: 0.8rem;
    transition: all 0.3s;
}
.uni-card .visit-btn:hover {
    background: linear-gradient(135deg, #005a9e, #0077cc);
}
.card-number {
    position: absolute;
    top: 1rem; right: 1.2rem;
    color: rgba(255,255,255,0.15);
    font-size: 2.5rem;
    font-weight: 900;
    line-height: 1;
}

/* ── Spinner overrides ── */
.stSpinner > div { border-top-color: #ffc107 !important; }

/* ── Footer ── */
.footer-bar {
    text-align: center;
    color: rgba(255,255,255,0.35);
    font-size: 0.8rem;
    padding: 2rem 0 1rem;
    letter-spacing: 1px;
}

/* ── Error / Info boxes ── */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: 1px solid rgba(255,193,7,0.3) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Gemini AI Setup
# ─────────────────────────────────────────────
def get_gemini_model():
    """Initialize and return the Gemini model."""
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY", ""))
    if not api_key:
        st.error("⚠️ **GEMINI_API_KEY** not found. Please add it to your Streamlit secrets or environment variables.")
        st.stop()
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.0-flash')

# ─────────────────────────────────────────────
# Prompt & Parser (same logic as original app)
# ─────────────────────────────────────────────
def generate_prompt(student_country, course, degree, target_country, fees):
    """Creates a detailed prompt for the Gemini AI model."""
    return f"""
    You are an expert international university admissions counselor. A student has provided their preferences. Your task is to recommend 10 universities that best match their criteria.

    Student's Criteria:
    - Student's Home Country: {student_country}
    - Desired Course/Field of Study: {course}
    - Desired Degree Level: {degree}
    - Target Country for Study: {target_country}
    - Preferred Annual Tuition Fee Range: {fees}

    Your Instructions:
    1.  Strict Output Format: You MUST respond with ONLY a Python-style list of strings. Do not add any other text, explanation, or introductory sentences. Each string in the list must contain four pieces of information separated by a semicolon ';'.
        - Format for each item: "University Name; City; Estimated Annual Tuition Fees; Website URL"
        - The Website URL must be the official university admissions page if possible, otherwise the homepage. Ensure it starts with https://.
    2.  Find 10 universities in the '{target_country}' that match the criteria.
    3.  Do NOT recommend any universities from the student's home country, '{student_country}'.
    """

def parse_gemini_response(response_text: str):
    """Parses the raw text response from Gemini to extract university data."""
    universities = []
    pattern = r'"([^"]+)"'
    matches = re.findall(pattern, response_text)
    for item in matches:
        parts = [p.strip() for p in item.split(';')]
        if len(parts) == 4:
            universities.append({
                'name':    parts[0],
                'city':    parts[1],
                'tuition': parts[2],
                'website': parts[3],
            })
    return universities

# ─────────────────────────────────────────────
# Hero Banner
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
    <div class="logo">🎓 UniAi</div>
    <h1>Find Your Future University</h1>
    <p>AI-powered university recommendations tailored to your goals and budget</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Input Form
# ─────────────────────────────────────────────
st.markdown('<div class="form-card">', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    course = st.text_input(
        "📚 Course / Field of Study",
        placeholder="e.g., Computer Science, MBA, Medicine...",
        key="course"
    )
    degree = st.selectbox(
        "🎓 Degree Type",
        options=["", "Bachelor's", "Master's", "PhD", "Diploma"],
        key="degree"
    )

with col2:
    target_country = st.selectbox(
        "🌍 Target Country",
        options=[
            "", "United States", "United Kingdom", "Germany", "Canada",
            "Australia", "Switzerland", "France", "South Korea",
            "New Zealand", "Japan", "Netherlands", "Singapore",
            "Sweden", "Denmark", "Norway", "Ireland", "Italy", "Spain"
        ],
        key="target_country"
    )
    student_country = st.selectbox(
        "🏳️ Your Home Country",
        options=[
            "", "India", "China", "Nigeria", "Pakistan", "Brazil",
            "Bangladesh", "Nepal", "Sri Lanka", "United States",
            "United Kingdom", "Germany", "Canada", "Australia",
            "Indonesia", "Mexico", "Iran", "Turkey", "Egypt", "Kenya"
        ],
        key="student_country"
    )

with col3:
    fees = st.selectbox(
        "💰 Annual Tuition Budget",
        options=[
            "", "Any", "Less than $10,000", "$10,000 – $30,000",
            "More than $30,000", "Free or Scholarship-based"
        ],
        key="fees"
    )
    st.markdown("<br>", unsafe_allow_html=True)  # spacer
    search_clicked = st.button("🔍 Find Universities", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)  # close .form-card

# ─────────────────────────────────────────────
# Search Logic
# ─────────────────────────────────────────────
if search_clicked:
    # Validation
    missing = []
    if not course.strip():        missing.append("Course / Field of Study")
    if not degree:                missing.append("Degree Type")
    if not target_country:        missing.append("Target Country")
    if not student_country:       missing.append("Your Home Country")
    if not fees:                  missing.append("Annual Tuition Budget")

    if missing:
        st.warning(f"⚠️ Please fill in: **{', '.join(missing)}**")
    else:
        with st.spinner("🤖 AI is searching for the best universities for you…"):
            try:
                model = get_gemini_model()
                prompt = generate_prompt(student_country, course, degree, target_country, fees)
                response = model.generate_content(prompt)
                universities = parse_gemini_response(response.text)
            except Exception as e:
                st.error(f"❌ An error occurred while contacting Gemini AI: {e}")
                universities = []

        if not universities:
            st.error("😕 No universities found matching your criteria. Please adjust your search and try again.")
        else:
            # Results Header
            st.markdown(f"""
            <div class="results-title">🎓 Recommended Universities in {target_country}</div>
            <div style="text-align:center;color:rgba(255,255,255,0.5);margin-bottom:1.5rem;font-size:0.9rem;">
                Showing {len(universities)} results for <strong style="color:#ffc107">{degree} in {course}</strong>
            </div>
            <div class="disclaimer-box">
                ℹ️ <strong>Disclaimer:</strong> The data provided is AI-generated and for guidance only.
                Please verify all information on the official university websites before making any decisions.
            </div>
            """, unsafe_allow_html=True)

            # University Cards – 2 columns
            left_col, right_col = st.columns(2)
            for i, uni in enumerate(universities):
                name    = uni.get('name', 'N/A')
                city    = uni.get('city', 'N/A')
                tuition = uni.get('tuition', 'Contact University')
                website = uni.get('website', '#')

                card_html = f"""
                <div class="uni-card">
                    <div class="card-number">{i+1:02d}</div>
                    <h4>🏛️ {name}</h4>
                    <div class="city-tag">📍 {city}</div><br>
                    <span class="tuition-tag">💵 {tuition}</span>
                    <br><br>
                    <a href="{website}" target="_blank" rel="noopener noreferrer" class="visit-btn">
                        🔗 Visit Website ↗
                    </a>
                </div>
                """
                if i % 2 == 0:
                    with left_col:
                        st.markdown(card_html, unsafe_allow_html=True)
                else:
                    with right_col:
                        st.markdown(card_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Footer
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer-bar">
    © 2025 UniAi · AI-Powered University Discovery · All rights reserved
</div>
""", unsafe_allow_html=True)
