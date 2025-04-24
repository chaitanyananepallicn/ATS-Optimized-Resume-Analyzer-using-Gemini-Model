import streamlit as st
from streamlit_extras import add_vertical_space as avs
from dotenv import load_dotenv
import google.generativeai as genai
import os
import PyPDF2
from PIL import Image

# Load environment variables and configure Gemini AI
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Function to get Gemini response
def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

# Input prompt template
input_prompt = """
As an experienced ATS (Applicant Tracking System)...
resume: {text}
description: {jd}

I want the response in the following structure:
The first line indicates the percentage match with the job description (JD).
The second line presents a list of missing keywords.
The third section provides a profile summary.

Mention the title for all the three sections.
While generating the response put some space to separate all the three sections.
"""

# Streamlit UI Configuration
st.set_page_config(page_title="ResumeIQ", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS with adjusted spacing
st.markdown("""
<style>
    /* Main container */
    .main {
        background-color: #121212;
        color: #e0e0e0;
        font-family: 'Poppins', sans-serif;
        margin-top: 0 !important;
        padding-top: 10px !important;
    }

    /* Header section with background image */
    .header-section {
        background: url('images/icon1.png') no-repeat center center;
        background-size: cover;
        padding: 20px;
        border-radius: 15px;
        position: relative;
        margin-top: 0 !important;
    }
    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(18, 18, 18, 0.7);
        border-radius: 15px;
        z-index: 0;
    }
    .header-content {
        position: relative;
        z-index: 1;
        text-align: center;
    }

    /* Header styles */
    .header-title {
        color: #00ddeb !important;
        font-weight: 700;
        font-size: 3.5rem;
        letter-spacing: 1px;
        text-shadow: 2px 2px 8px rgba(0, 221, 235, 0.3);
        margin: 0;
    }
    .header-subtitle {
        color: #b0bec5 !important;
        font-weight: 300;
        font-size: 1.5rem;
        margin-top: -5px;
    }
    .header-desc {
        color: #90a4ae !important;
        font-size: 1rem;
        margin-top: 5px;
    }

    /* Section dividers */
    .divider {
        border-top: 1px solid #37474f;
        margin: 20px 0; /* Consistent spacing between sections */
    }

    /* Section container for consistent spacing */
    .section-container {
        margin: 20px 0; /* Reduced and consistent spacing between sections */
    }

    /* Subheader styles */
    h2 {
        color: #00ddeb !important;
        font-weight: 600;
        font-size: 2rem;
        margin-bottom: 15px;
    }

    /* Input fields */
    .stTextArea > div > textarea,
    .stTextInput > div > input {
        background-color: #1e2a38 !important;
        color: #e0e0e0 !important;
        border: 1px solid #37474f !important;
        border-radius: 8px;
        padding: 10px;
    }

    /* Button styles */
    .stButton > button {
        background: linear-gradient(90deg, #00ddeb 0%, #00b0ff 100%);
        color: #121212;
        font-weight: 600;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #00b0ff 0%, #00ddeb 100%);
        box-shadow: 0 4px 15px rgba(0, 221, 235, 0.4);
    }

    /* Result box */
    .result-box {
        background-color: #1e2a38;
        padding: 20px;
        border-radius: 12px;
        color: #e0e0e0;
        border: 1px solid #37474f;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    }

    /* Feature list */
    .feature-item {
        color: #b0bec5 !important;
        font-size: 1.1rem;
        margin-bottom: 8px;
    }

    /* Image and text layout for Features section */
    .feature-container {
        display: flex;
        align-items: center;
        gap: 20px;
        margin: 20px 0;
    }
    .feature-image {
        flex: 0 0 auto;
        width: 250px;
    }
    .feature-text {
        flex: 1;
        color: #b0bec5;
        font-size: 1.1rem;
        line-height: 1.6;
    }

    /* FAQ styles */
    .stExpander {
        background-color: #1e2a38 !important;
        border-radius: 8px;
        border: 1px solid #37474f;
        margin-bottom: 10px;
    }
    .stExpander > div > div {
        color: #00ddeb !important;
        font-weight: 500;
    }
    .stExpander > div > div > div {
        color: #b0bec5 !important;
    }

    /* Footer */
    .footer {
        color: #607d8b !important;
        font-size: 0.9rem;
        text-align: center;
        margin-top: 20px; /* Reduced spacing */
    }

    /* Images */
    .stImage > img {
        border-radius: 10px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }
    .stImage > img:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Header Section with Background
avs.add_vertical_space(1)  # Keep minimal top spacing
st.markdown("""
<div class='header-section'>
    <div class='header-content'>
        <h1 class='header-title'>ResumeIQ</h1>
        <h3 class='header-subtitle'>Navigate the Job Market with Confidence!</h3>
        <p class='header-desc'>ATS-Optimized Resume Analyzer powered by Google Gemini AI</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Features Section with Image and Text
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-container'>", unsafe_allow_html=True)
st.subheader("Wide Range of Offerings")
col1, col2 = st.columns([1, 2])
with col1:
    img_features = Image.open("images/icon2.png")
    st.image(img_features, caption="Our Features", width=250, use_column_width=True)
with col2:
    st.markdown("""
    <div class='feature-text'>
        Discover the power of ResumeIQ with our comprehensive suite of tools designed to elevate your career:
        <ul>
            <li>ATS-Optimized Resume Analysis</li>
            <li>Resume Optimization</li>
            <li>Skill Enhancement</li>
            <li>Career Progression Guidance</li>
            <li>Tailored Profile Summaries</li>
            <li>Streamlined Application Process</li>
            <li>Personalized Recommendations</li>
            <li>Efficient Career Navigation</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Resume Analysis Section
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-container'>", unsafe_allow_html=True)
st.subheader("Resume Analysis")
jd = st.text_area("📄 Paste the Job Description", height=150, placeholder="Enter the job description here...")
uploaded_file = st.file_uploader("📎 Upload Your Resume (PDF only)", type="pdf")

if st.button("Analyze Resume"):
    if uploaded_file and jd:
        with st.spinner("Analyzing your resume..."):
            text = input_pdf_text(uploaded_file)
            final_prompt = input_prompt.format(text=text, jd=jd)
            response = get_gemini_response(final_prompt)
            st.success("✅ Analysis Complete!")
            st.markdown("### 📊 ATS Match Result")
            st.markdown(f"""
            <div class='result-box'>
                <pre>{response}</pre>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Please upload a resume and provide a job description.")

img_analysis = Image.open("images/icon3.png")
st.image(img_analysis, width=250)
st.markdown("</div>", unsafe_allow_html=True)

# FAQ Section
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<div class='section-container'>", unsafe_allow_html=True)
st.subheader("Frequently Asked Questions")
faq = {
    "How does ResumeIQ analyze resumes and job descriptions?": "It leverages Google's Gemini AI to identify keyword matches and calculate resume-to-job-description compatibility with high accuracy.",
    "Can ResumeIQ suggest improvements for my resume?": "Yes! It provides a list of missing keywords and a custom profile summary to enhance your resume's ATS compatibility.",
    "Is this suitable for entry-level or experienced professionals?": "Absolutely! ResumeIQ tailors feedback to your experience level and career goals, whether you're just starting out or advancing in your career."
}
for question, answer in faq.items():
    with st.expander(f"**Q: {question}**"):
        st.write(answer)
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<hr class='divider'>", unsafe_allow_html=True)
st.markdown("<p class='footer'>Made with  using Streamlit & Gemini AI</p>", unsafe_allow_html=True)