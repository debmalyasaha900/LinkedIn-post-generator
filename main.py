import streamlit as st
import time
from few_shots import FewShotPosts
from db import get_all_influencers
from post_generator import generate_post
import streamlit.components.v1 as components

st.set_page_config(page_title="LinkedIn Post Generator", page_icon="🔗", layout="wide")

# ---------------- RATE LIMITING ----------------
if "last_generated" not in st.session_state:
    st.session_state.last_generated = 0

# ---------------- DARK MODE + CSS ----------------
st.markdown(
    """
    <style>

    .stApp {
        background-color: #0d1117 !important;
        color: #e6edf3 !important;
    }

    .block-container {
        padding-top: 1rem;
    }

    .title {
        font-size: 44px;
        font-weight: 800;
        text-align: center;
        margin-top: 10px;
        color: #58a6ff !important;
    }

    .card {
        background: #161b22;
        padding: 26px;
        border-radius: 14px;
        box-shadow: 0 0 10px rgba(0,0,0,0.4);
        margin-bottom: 22px;
        color: #c9d1d9;
    }

    /* Disable typing in selectbox */
    .stSelectbox input {
        caret-color: transparent !important;
        color: transparent !important;
        text-shadow: 0 0 0 #c9d1d9 !important;
    }

    .stButton>button {
        background-color: #238636 !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 25px !important;
        font-size: 17px !important;
        border: none !important;
    }
    .stButton>button:hover {
        background-color: #2ea043 !important;
    }

    .generated-box {
        background-color: #0d1117;
        border: 1px solid #30363d;
        padding: 22px;
        border-radius: 12px;
        white-space: pre-wrap;
        font-size: 18px;
        color: #e6edf3;
        line-height: 1.6;
    }

    .success-box {
        background-color: #04260f;
        color: #56d364;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #238636;
        font-size: 16px;
    }
    /* Completely disable typing and text cursor */
    .stSelectbox input {
        pointer-events: none !important;   /* Prevent clicking/typing */
        user-select: none !important;
        caret-color: transparent !important;
        color: transparent !important;
        text-shadow: 0 0 0 #c9d1d9 !important;
    }
    
    /* Force cursor to always stay arrow */
    .stSelectbox div, .stSelectbox select, .stSelectbox input {
        cursor: default !important;
    }


    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- TITLE ----------------
st.markdown("<div class='title'>🔗 LinkedIn Post Generator</div>", unsafe_allow_html=True)
st.write("")

fs = FewShotPosts()
influencers = get_all_influencers()
influencer_names = [i["name"] for i in influencers] if influencers else []

# ---------------- INPUT CARD ----------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### ⚙ Select Post Settings")
st.write("Customize how the generator should create your LinkedIn post.")

col1, col2, col3, col4 = st.columns(4)

# ---------------- 1️⃣ Influencer ----------------
with col1:
    selected_influencer = st.selectbox(
        "Influencer",
        influencer_names,
        index=None,
        placeholder="Select Influencer"
    )

# ---------------- 2️⃣ Topic / Tag ----------------
with col2:
    if not selected_influencer:
        selected_tag = st.selectbox(
            "Topic / Tag",
            [],
            index=None,
            disabled=True,
            placeholder="Select influencer first"
        )
    else:
        tag_options = fs.get_tags_for_influencer(selected_influencer)
        selected_tag = st.selectbox(
            "Topic / Tag",
            tag_options,
            index=None,
            placeholder="Select Topic"
        )

# ---------------- 3️⃣ Length ----------------
with col3:
    selected_length = st.selectbox(
        "Length",
        ["Short", "Medium", "Long"],
        index=None,
        disabled=not selected_tag,
        placeholder="Select Length"
    )

# ---------------- 4️⃣ Language ----------------
with col4:
    selected_language = st.selectbox(
        "Language",
        ["English", "Hinglish"],
        index=None,
        disabled=not selected_length,
        placeholder="Select Language"
    )

st.write("")

# ---------------- Generate Button (Disabled Until All Selected) ----------------
generate_clicked = st.button(
    "✨ Generate Post",
    disabled=not (selected_influencer and selected_tag and selected_length and selected_language)
)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- OUTPUT ----------------
if generate_clicked:

    # RATE LIMITER
    now = time.time()
    if now - st.session_state.last_generated < 5:
        wait_time = int(5 - (now - st.session_state.last_generated))
        st.error(f"⏳ Please wait {wait_time} more seconds before generating again.")
        st.stop()

    st.session_state.last_generated = time.time()

    with st.spinner("Generating your LinkedIn post..."):
        post = generate_post(
            influencer=selected_influencer,
            length=selected_length,
            language=selected_language,
            tag=selected_tag
        )

    st.markdown("<div class='success-box'>✔ Post generated successfully!</div>", unsafe_allow_html=True)
    st.write("")
    st.markdown(f"<div class='generated-box'>{post}</div>", unsafe_allow_html=True)

    # --------------- COPY BUTTON (JS) ---------------
    components.html(
        f"""
        <html>
        <head>
            <style>
                .copy-btn {{
                    background-color:#238636;
                    color:white;
                    padding:10px 28px;
                    border:none;
                    border-radius:8px;
                    cursor:pointer;
                    font-size:17px;
                    transition:0.2s;
                }}

                .copy-btn:hover {{
                    background-color:#2ea043;
                }}
            </style>
        </head>

        <body>
            <button class="copy-btn" onclick="copyText()">📋 Copy Post</button>

            <script>
                function copyText() {{
                    navigator.clipboard.writeText(`{post}`);
                }}
            </script>
        </body>
        </html>
        """,
        height=80,
    )

    # --------------- GENERATE AGAIN BUTTON ---------------

# ---------------- FOOTER ----------------
st.markdown(
    """
    <hr><br>
    <div style='text-align:center; color:#8b949e; font-size:15px;'>
        Made with ❤️ by <b>Debmalya Saha</b><br>
        Powered by Llama 4 • Streamlit • MongoDB Atlas • Langgraph
    </div>
    """,
    unsafe_allow_html=True,
)
