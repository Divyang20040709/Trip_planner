import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import IntegrityError

st.set_page_config(
    page_title="Trip Planner AI — Your Personal Travel Assistant",
    page_icon="✈️",
    layout="centered",
)

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
DB_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:@localhost/trip_planner")

Base = declarative_base()

class TripPlan(Base):
    __tablename__ = "trip_plan"
    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_name   = Column(String(100), nullable=False)
    user_email  = Column(String(100), nullable=False)
    user_mobile = Column(String(20),  nullable=False)

engine  = create_engine(DB_URL, pool_pre_ping=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def insert_user_details(user_name: str, user_email: str, user_mobile: str) -> bool:
    session = Session()
    try:
        session.add(TripPlan(user_name=user_name, user_email=user_email, user_mobile=user_mobile))
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        st.error("A database integrity error occurred. Please try again.")
        return False
    except Exception as e:
        session.rollback()
        st.error(f"Database error: {e}")
        return False
    finally:
        session.close()

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are an intelligent trip planner chatbot.
Your role is to help users create a personalized trip plan based on their preferences.
Generate a detailed trip plan that includes:
- Suggested activities and attractions at the destination
- Recommended accommodations within the specified budget
- Estimated costs for activities, accommodations, and meals
- A day-by-day itinerary that optimizes the user's time and budget
- Local food recommendations
- Travel tips and must-knows for the destination

Always present information in a clear, structured format with emojis for readability.
End every response with: "⚠️ Disclaimer: This trip plan is for informational purposes only. Please verify details before making travel arrangements."
"""

def generate_response(destination: str, duration: str, budget: str) -> str:
    prompt = (
        f"{SYSTEM_PROMPT}\n\n"
        f"Create a complete trip plan for:\n"
        f"📍 Destination: {destination}\n"
        f"📅 Duration: {duration}\n"
        f"💰 Budget: {budget}\n\n"
        f"Make it detailed, practical, and exciting!"
    )
    response = client.models.generate_content(model="gemini-3-flash-preview", contents=prompt)
    return response.text


st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
}
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: linear-gradient(160deg, #dbeafe 0%, #ede9fe 40%, #fce7f3 100%);
    min-height: 100vh;
}

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 780px !important;
}

.hero-wrap {
    background: white;
    border-radius: 24px;
    padding: 2.4rem 2rem 1.8rem;
    text-align: center;
    box-shadow: 0 4px 32px rgba(99,102,241,0.10);
    margin-bottom: 1.5rem;
    border: 1px solid rgba(99,102,241,0.08);
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #6366f1, #8b5cf6, #f97316);
    border-radius: 24px 24px 0 0;
}
.hero-icon {
    font-size: 3rem;
    line-height: 1;
    margin-bottom: 0.5rem;
    display: block;
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 50%, #f97316 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem;
    line-height: 1.2;
}
.hero-sub {
    color: #64748b;
    font-size: 1rem;
    font-weight: 400;
    margin: 0;
}

.step-card {
    background: white;
    border-radius: 20px;
    padding: 1.6rem 1.8rem 1.2rem;
    box-shadow: 0 2px 20px rgba(0,0,0,0.06);
    margin-bottom: 1.2rem;
    border: 1px solid rgba(0,0,0,0.05);
}
.step-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 1.2rem;
}
.step-number {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    color: white;
    font-size: 0.85rem;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}
.step-title {
    font-size: 1rem;
    font-weight: 700;
    color: #1e293b;
    margin: 0;
}
.step-subtitle {
    font-size: 0.8rem;
    color: #94a3b8;
    margin: 0;
    font-weight: 400;
}

label, .stTextInput label, [data-testid="stTextInput"] label {
    color: #374151 !important;
    font-size: 0.87rem !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
}

input, textarea,
.stTextInput input,
[data-testid="stTextInput"] input {
    background: #f8fafc !important;
    border: 1.5px solid #e2e8f0 !important;
    border-radius: 10px !important;
    color: #1e293b !important;
    -webkit-text-fill-color: #1e293b !important;
    caret-color: #6366f1 !important;
    font-size: 0.93rem !important;
    font-weight: 500 !important;
    padding: 0.6rem 0.9rem !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease, background 0.2s ease !important;
}
.stTextInput input:focus,
[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    background: #ffffff !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
    outline: none !important;
}
.stTextInput input::placeholder,
[data-testid="stTextInput"] input::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
    font-weight: 400 !important;
}

.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: white !important;
    -webkit-text-fill-color: white !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 0.8rem 2rem !important;
    font-size: 1.02rem !important;
    font-weight: 700 !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
    transition: transform 0.15s ease, box-shadow 0.15s ease !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(99,102,241,0.5) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

.stAlert {
    border-radius: 12px !important;
    font-size: 0.9rem !important;
}

.stSpinner > div { border-top-color: #6366f1 !important; }

.output-wrap {
    background: white;
    border-radius: 20px;
    padding: 1.8rem;
    box-shadow: 0 4px 28px rgba(99,102,241,0.10);
    border: 1px solid rgba(99,102,241,0.12);
    margin-top: 1.5rem;
    position: relative;
    overflow: hidden;
}
.output-wrap::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, #f97316, #8b5cf6, #6366f1);
    border-radius: 20px 20px 0 0;
}
.output-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 8px;
}

.tip-box {
    background: linear-gradient(135deg, #eff6ff, #f5f3ff);
    border: 1px solid #c7d2fe;
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 1.2rem;
}
.tip-icon { font-size: 1.1rem; flex-shrink: 0; margin-top: 1px; }
.tip-text { color: #4338ca; font-size: 0.85rem; font-weight: 500; line-height: 1.5; }

.stMarkdown p, .stMarkdown li {
    color: #334155 !important;
    font-size: 0.95rem !important;
    line-height: 1.75 !important;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #1e293b !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="hero-wrap">
    <span class="hero-icon">✈️</span>
    <h1 class="hero-title">Trip Planner AI</h1>
    <p class="hero-sub">Your personal travel assistant powered by Gemini AI — <br>
    fill in the details below and get a full itinerary in seconds.</p>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div class="step-card">
    <div class="step-header">
        <div class="step-number">1</div>
        <div>
            <p class="step-title">👤 Your Details</p>
            <p class="step-subtitle">We save your info to personalise future plans</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    user_name = st.text_input("Full Name", placeholder="e.g. Aryan Sharma", key="name")
with col2:
    user_email = st.text_input("Email Address", placeholder="e.g. aryan@gmail.com", key="email")
with col3:
    user_mobile = st.text_input("Mobile Number", placeholder="e.g. +91 98765 43210", key="mobile")


st.markdown("""
<div class="step-card" style="margin-top:1.2rem">
    <div class="step-header">
        <div class="step-number">2</div>
        <div>
            <p class="step-title">🗺️ Trip Preferences</p>
            <p class="step-subtitle">Tell us where you want to go and how much you want to spend</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

col_dest, col_dur = st.columns([2, 1])
with col_dest:
    destination = st.text_input("Destination", placeholder="e.g. Goa, Paris, Bali, New York", key="dest")
with col_dur:
    duration = st.text_input("Duration", placeholder="e.g. 5 Days 4 Nights", key="dur")

budget = st.text_input("Total Budget", placeholder="e.g. ₹30,000 or $500 — include currency!", key="budget")

st.markdown("""
<div class="tip-box" style="margin-top:0.6rem">
    <span class="tip-icon">💡</span>
    <span class="tip-text">
        <strong>Pro tip:</strong> The more specific your budget and destination, the better your plan!
        Try "Manali for 4 days 3 nights under ₹15,000 including transport".
    </span>
</div>
""", unsafe_allow_html=True)


generate = st.button("🌍  Generate My Trip Plan  →")

if generate:
    missing = []
    if not user_name:   missing.append("Full Name")
    if not user_email:  missing.append("Email Address")
    if not user_mobile: missing.append("Mobile Number")
    if not destination: missing.append("Destination")
    if not duration:    missing.append("Duration")
    if not budget:      missing.append("Budget")

    if missing:
        st.error(f"⚠️  Please fill in: **{', '.join(missing)}**")
    else:
        with st.spinner("✈️  Building your personalised trip plan…"):
            saved = insert_user_details(user_name, user_email, user_mobile)
            if not saved:
                st.stop()
            plan = generate_response(destination, duration, budget)

        st.markdown(f"""
        <div class="output-wrap">
            <div class="output-title">
                🗓️ Your Personalised Trip Plan for <span style="color:#6366f1">{destination}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"✅ Plan generated for **{user_name}** · {duration} · {budget}")
        st.markdown("---")
        st.markdown(plan)