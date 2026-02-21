import streamlit as st
import streamlit.components.v1 as components
st.markdown("""
        <style>
            /* Hide Streamlit deploy button and 3-dot menu */
            .stDeployButton, .stActionButton, [data-testid="stToolbar"] { display: none !important; }
        </style>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;700&display=swap');
        body, .stApp {
            font-family: 'Segoe UI', Arial, sans-serif !important;
            background: linear-gradient(135deg, #f8fafc 0%, #e0e7ef 100%) !important;
            color: #222 !important;
        }
        .stSidebar {
            background: #f1f5f9 !important;
            border-right: 1px solid #cbd5e1 !important;
        }
        .stButton>button {
            background: linear-gradient(90deg, #38bdf8 0%, #a7f3d0 100%) !important;
            color: #222 !important;
            font-weight: 700 !important;
            font-size: 1.1rem !important;
            border-radius: 8px !important;
            border: none !important;
            margin-top: 16px !important;
            cursor: pointer !important;
            transition: background 0.2s !important;
            animation: buttonPulse 2s infinite !important;
        }
        @keyframes buttonPulse {
            0%, 100% { box-shadow: 0 0 0 0 #38bdf8; }
            50% { box-shadow: 0 0 16px 4px #38bdf8; }
        }
            .stTextInput>div>input, .stTextArea>div>textarea, .stPasswordInput>div>input,
            input[type="text"], input[type="password"], textarea {
                background: #fff !important;
                color: #222 !important;
                border-radius: 10px !important;
                border: 3px solid #000 !important;
                outline: 3px solid #23272f !important;
                font-size: 1.1rem !important;
                box-shadow: 0 4px 16px #cbd5e1 !important;
                padding: 12px 16px !important;
                margin-bottom: 8px !important;
                transition: border-color 0.3s, box-shadow 0.3s, background 0.3s, outline-color 0.3s;
            }
            .stTextInput>div>input:focus, .stTextArea>div>textarea:focus, .stPasswordInput>div>input:focus {
                border-color: #38bdf8 !important;
                background: #fff !important;
                box-shadow: 0 6px 24px #38bdf8 !important;
            }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4 {
            color: #222 !important;
            font-weight: 700 !important;
        }
        .stMetric {
            background: #f1f5f9 !important;
            border-radius: 12px !important;
            padding: 12px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 16px rgba(56, 189, 248, 0.08);
            border: 1px solid #cbd5e1 !important;
            animation: fadeIn 1.2s ease;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        .emoji {
            font-size: 1.5rem !important;
            vertical-align: middle !important;
            animation: bounceEmoji 1.2s infinite !important;
        }
        @keyframes bounceEmoji {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px) scale(1.2); }
        }
        .stRadio>div>label, .stSelectbox>div>label {
            color: #38bdf8 !important;
            font-weight: 700 !important;
        }
        .stFileUploader>div>label {
            color: #38bdf8 !important;
            font-weight: 700 !important;
        }
        .stSidebar .sidebar-content {
            animation: fadeIn 1.2s ease;
        }
        .stSidebar .sidebar-content h1, .stSidebar .sidebar-content h2 {
            color: #38bdf8 !important;
        }
    </style>
""", unsafe_allow_html=True)
import requests
import pandas as pd

st.set_page_config(page_title="Twitter Sentiment Analyzer 🐦", layout="wide")

# ---------------------------
# SESSION STATE
# ---------------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "uploaded_df" not in st.session_state:
    st.session_state.uploaded_df = None


# ---------------------------
# LOAD DEFAULT DATASET
# ---------------------------
def load_default_dataset():
    try:
        return pd.read_csv("Covid-19 Twitter Dataset (Apr-Jun 2020).csv")
    except:
        return None


def load_dataset(filename):
    try:
        return pd.read_csv(filename)
    except:
        return None


# ---------------------------
# AUTH PAGE
# ---------------------------
def auth_page():
    st.title("Twitter Sentiment Analysis Platform💬")

    menu = st.radio(" Select Option", ["Login", "Signup"])

    if menu == "Signup":
        st.subheader(" Create New Account")
        new_user = st.text_input("Username ")
        new_pass = st.text_input("Password ", type="password")

        if st.button("Signup"):
            if new_user in st.session_state.users:
                st.error("User already exists!")
            elif new_user.strip() == "" or new_pass.strip() == "":
                st.warning("Fields cannot be empty")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Account created successfully! 🎉")

    if menu == "Login":
        st.subheader("Login to Continue")
        user = st.text_input("Username ")
        password = st.text_input("Password ", type="password")

        if st.button("Login"):
            if user in st.session_state.users and st.session_state.users[user] == password:
                st.session_state.logged_in = True
                st.session_state.username = user
                st.rerun()
            else:
                st.error("Invalid credentials")


# ---------------------------
# SENTIMENT METRIC DISPLAY
# ---------------------------
def show_sentiment_overview(df, title="📊 Sentiment Overview"):

    if "sentiment" not in df.columns:
        st.error("Dataset must contain a 'sentiment' column.")
        st.write("Available columns:", df.columns.tolist())
        return

    pos = df[df["sentiment"].isin(["pos", "positive"])].shape[0]
    neg = df[df["sentiment"].isin(["neg", "negative"])].shape[0]
    neu = df[df["sentiment"].isin(["neu", "neutral"])].shape[0]
    total = len(df)

    st.subheader(title)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📝 Total Tweets", total)
    col2.metric("😊 Positive", pos)
    col3.metric("😡 Negative", neg)
    col4.metric("😐 Neutral", neu)

    chart_data = pd.DataFrame({
        "Sentiment": ["Positive", "Negative", "Neutral"],
        "Count": [pos, neg, neu]
    })

    st.bar_chart(chart_data.set_index("Sentiment"))


# ---------------------------
# MAIN APP
# ---------------------------
def main_app():

    st.sidebar.markdown("""
        <style>
            @keyframes gradientMove {
                0% {background-position: 0% 50%;}
                50% {background-position: 100% 50%;}
                100% {background-position: 0% 50%;}
            }
            .modern-sidebar {
                background: linear-gradient(135deg, #000 0%, #23272f 100%);
                border-radius: 18px;
                padding: 24px 18px 18px 18px;
                margin-bottom: 24px;
                box-shadow: 0 8px 32px rgba(30,161,242,0.18);
                display: flex;
                flex-direction: column;
                align-items: center;
                transition: box-shadow 0.4s;
            }
            .modern-sidebar:hover {
                box-shadow: 0 12px 48px rgba(56,189,248,0.18);
            }
            .modern-logo {
                background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="white"><path d="M23.5 4h4.5l-9.5 11.2 11 12.8h-8.7l-6.8-8.2-7.8 8.2h-4.6l10.2-11.7-10.8-12.3h9l6.2 7.5z"/></svg>') no-repeat center/contain;
                width: 48px;
                height: 48px;
                margin-bottom: 10px;
                transition: transform 0.4s;
            }
            .modern-logo:hover {
                transform: scale(1.15) rotate(10deg);
            }
            .modern-title {
                font-size: 2rem;
                font-weight: 900;
                color: #fff;
                letter-spacing: 1px;
                margin-bottom: 16px;
                text-shadow: 0 2px 8px #23272f;
                transition: color 0.3s;
            }
            .modern-title:hover {
                color: #38bdf8;
            }
            .stRadio > div {
                display: flex;
                flex-direction: column;
                gap: 12px;
            }
            .stRadio > div > label {
                display: flex;
                align-items: center;
                gap: 12px;
                font-size: 1.15rem;
                font-weight: 700;
                color: #0ea5e9;
                background: #fff;
                border-radius: 12px;
                box-shadow: 0 2px 8px #e0e7ef;
                padding: 14px 18px;
                margin-bottom: 0;
                transition: background 0.3s, color 0.3s, box-shadow 0.3s, transform 0.3s;
                cursor: pointer;
            }
            /* Style Streamlit selectbox dropdown */
            .stSelectbox > div {
                background: #f1f5f9 !important;
                border-radius: 12px !important;
                box-shadow: 0 2px 8px #38bdf8 !important;
                padding: 8px 12px !important;
                border: 1px solid #38bdf8 !important;
                animation: fadeIn 1s;
            }
            .stSelectbox label {
                color: #0ea5e9 !important;
                font-weight: 700 !important;
            }
            .stSelectbox select {
                background: #fff !important;
                border-radius: 8px !important;
                border: 1px solid #38bdf8 !important;
                color: #0ea5e9 !important;
                font-weight: 700 !important;
                padding: 6px 10px !important;
                box-shadow: 0 2px 8px #e0e7ef !important;
                transition: box-shadow 0.3s;
            }
            .stSelectbox select:focus {
                box-shadow: 0 4px 16px #38bdf8 !important;
            }
            .stRadio > div > label[data-selected="true"] {
                background: #38bdf8 !important;
                color: #fff !important;
                box-shadow: 0 4px 16px #0ea5e9;
                transform: scale(1.04);
            }
            .stRadio > div > label:hover {
                background: #a7f3d0;
                color: #0ea5e9;
                box-shadow: 0 4px 16px #38bdf8;
                transform: scale(1.03);
            }
            .modern-nav-icon {
                font-size: 1.4rem;
            }
        </style>
        <div class="modern-sidebar">
            <div class="modern-logo"></div>
            <div class="modern-title">Twitter Sentiment Analyzer</div>
        </div>
    """, unsafe_allow_html=True)
    # Use Streamlit's radio for navigation
    menu = st.sidebar.radio(
        "Navigation",
        [
            "🏠 Home",
            "🔍 Search Tweets",
            "⚡ Live Analyzer",
            "🎭 Emotion & Topics",
            "📊 Comparison",
            "📂 Upload Dataset",
            "💬 Chatbot"
        ],
        key="nav_radio"
    )

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # ---------------------------
    # HOME
    # ---------------------------
    if menu == "🏠 Home":
        st.markdown("""
            <h1 style='text-align:center; margin-bottom:24px;'>Dashboard Overview <span class='emoji'>📊</span></h1>
        """, unsafe_allow_html=True)
        df = load_default_dataset()
        if df is None:
            st.error("Default dataset not found.")
        else:
            show_sentiment_overview(df, "Dataset Sentiment Overview")
    elif menu == "💬 Chatbot":
        st.markdown("""
            <h1 style='text-align:center; margin-bottom:24px;'>X Chatbot <span class='emoji'>💬</span></h1>
        """, unsafe_allow_html=True)
        # IMAX screen effect: full width and height
        st.markdown("""
            <style>
                .imax-chatbot iframe {
                    width: 100vw !important;
                    height: 85vh !important;
                    min-height: 600px;
                    border-radius: 18px;
                    box-shadow: 0 8px 32px rgba(56,189,248,0.18);
                    margin: 0 auto;
                    display: block;
                }
            </style>
        """, unsafe_allow_html=True)
        st.markdown('<div class="imax-chatbot">', unsafe_allow_html=True)
        components.iframe("https://tweet-insight.vercel.app/", height=800, width=1920)
        st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------
    # SEARCH TWEETS
    # ---------------------------
    elif menu == "🔍 Search Tweets":
        st.markdown("""
            <h1 style='text-align:center; margin-bottom:24px;'>Search Tweets <span class='emoji'>🔍</span></h1>
        """, unsafe_allow_html=True)
        df = load_default_dataset()
        if df is None:
            st.error("Dataset not found.")
            return
        text_column = next((col for col in df.columns if "text" in col.lower() or "tweet" in col.lower()), None)
        if text_column is None:
            st.error("No tweet text column found.")
            return
        search = st.text_input("🔍 Enter keyword to search")
        if search:
            results = df[df[text_column].str.contains(search, case=False, na=False)]
            st.markdown(f"<div style='margin-bottom:12px;'><span class='emoji'>📌</span> Found {len(results)} results</div>", unsafe_allow_html=True)
            for tweet in results[text_column].head(50):
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown(f"<span class='emoji'>💬</span> {tweet}", unsafe_allow_html=True)

    # ---------------------------
    # LIVE ANALYZER
    # ---------------------------
    elif menu == "⚡ Live Analyzer":
        st.markdown("""
            <h1 style='text-align:center; margin-bottom:24px;'>Live Tweet Analyzer <span class='emoji'>⚡</span></h1>
        """, unsafe_allow_html=True)
        tweet = st.text_area("Enter Tweet")
        if st.button("Analyze"):
            if tweet.strip() == "":
                st.warning("Enter some text")
            else:
                try:
                    response = requests.post(
                        "http://127.0.0.1:5000/predict",
                        json={"text": tweet}
                    )
                    result = response.json()
                    col1, col2, col3 = st.columns(3)
                    col1.metric("<span class='emoji'>😊</span> Sentiment", result.get("sentiment"))
                    col2.metric("<span class='emoji'>😏</span> Sarcasm", result.get("sarcasm"))
                    col3.metric("<span class='emoji'>🎭</span> Emotion", result.get("emotion"))
                except:
                    st.error("Backend not running")

    # ---------------------------
    # EMOTION & TOPICS
    # ---------------------------
    elif menu == "🎭 Emotion & Topics":
        st.markdown("""
            <h1 style='text-align:center; margin-bottom:24px;'>Emotion & Topics Explorer <span class='emoji'>🌈</span></h1>
        """, unsafe_allow_html=True)
        df = load_default_dataset()
        if df is None:
            st.error("Dataset not found.")
            return
        text_column = next((col for col in df.columns if "text" in col.lower() or "tweet" in col.lower()), None)
        if text_column is None:
            st.error("No tweet text column found.")
            return
        if "emotion" not in df.columns:
            df["emotion"] = df[text_column].apply(
                lambda x: "Happy" if "happy" in str(x).lower()
                else "Sad" if "sad" in str(x).lower()
                else "Angry" if "angry" in str(x).lower()
                else "Neutral"
            )
        category = st.selectbox("Select Emotion Category", sorted(df["emotion"].unique()))
        filtered = df[df["emotion"] == category]
        st.markdown(f"<div style='margin-bottom:12px;'><span class='emoji'>📌</span> Found {len(filtered)} tweets</div>", unsafe_allow_html=True)
        for tweet in filtered[text_column].head(50):
            st.markdown("<hr>", unsafe_allow_html=True)
            st.markdown(f"<span class='emoji'>💬</span> {tweet}", unsafe_allow_html=True)

    # ---------------------------
    # COMPARISON (2020 vs 2021)
    # ---------------------------
    elif menu == "📊 Comparison":
        st.markdown("""
            <h1 style='text-align:center; margin-bottom:24px;'>Tweets Comparison 2020 vs 2021 <span class='emoji'>📊</span></h1>
        """, unsafe_allow_html=True)
        df1 = load_dataset("tweets2020.csv")
        df2 = load_dataset("tweets2021.csv")
        if df1 is None or df2 is None:
            st.error("tweets2020.csv or tweets2021.csv not found.")
            return
        col1, col2 = st.columns(2)
        with col1:
            show_sentiment_overview(df1, "Tweets 2020 Overview")
        with col2:
            show_sentiment_overview(df2, "Tweets 2021 Overview")

    # ---------------------------
    # UPLOAD DATASET
    # ---------------------------
    elif menu == "📂 Upload Dataset":
        st.markdown("""
            <h1 style='text-align:center; margin-bottom:24px;'>Upload Your Dataset <span class='emoji'>📂</span></h1>
        """, unsafe_allow_html=True)
        file = st.file_uploader("📤 Upload CSV", type=["csv"])
        if file:
            df = pd.read_csv(file)
            st.session_state.uploaded_df = df
            st.success("Dataset uploaded successfully! 🎉")
            show_sentiment_overview(df, "📊 Uploaded Dataset Overview")
            


# ---------------------------
# APP START
# ---------------------------
if not st.session_state.logged_in:
    auth_page()
else:
    main_app()