import streamlit as st
import json
import os
import time
from streamlit_lottie import st_lottie

# 📄 Page config: clean title and layout
st.set_page_config(
    page_title="Minimal Dictionary",
    page_icon="📘",
    layout="centered"
)
# --- Splash Animation ---
def load_lottiefile(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

if "show_intro" not in st.session_state:
    st.session_state.show_intro = True

if st.session_state.show_intro:
    lottie_intro = load_lottiefile("book.json")
    splash = st.empty()
    with splash.container():
        st.markdown("<h1 style='text-align:center;'>Welcome to DICTIONARY-APP!</h1>", unsafe_allow_html=True)
        st_lottie(lottie_intro, height=300, speed=1.0, loop=False)
        time.sleep(3)
    splash.empty()
    st.session_state.show_intro = False




# 📦 Load dictionary from local file
@st.cache_data
def load_dictionary():
    filepath = "merged.json"
    if not os.path.exists(filepath):
        st.error("❌ merged.json file not found.")
        return {}
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"❌ Error loading dictionary: {e}")
        return {}

dictionary = load_dictionary()

# 🧠 User input
st.title("📘 Dictionary")
word = st.text_input("🔍 Enter a word", "").strip().lower()

# 🔎 Lookup and display meanings
if word:
    entry = dictionary.get(word)

    # Fallback for casing issues
    if not entry:
        entry = dictionary.get(word.capitalize()) or dictionary.get(word.upper())

    if entry:
        if isinstance(entry, str):
            st.markdown(f"<p style='font-size:20px'>• {entry}</p>", unsafe_allow_html=True)
        elif isinstance(entry, dict):
            meanings = entry.get("MEANINGS", [])
            if meanings and isinstance(meanings, list):
                for meaning in meanings:
                    if isinstance(meaning, list) and len(meaning) >= 2:
                        definition = meaning[1]
                        st.markdown(f"<p style='font-size:20px'>• {definition}</p>", unsafe_allow_html=True)
            else:
                definition = entry.get("definition", "")
                if definition:
                    st.markdown(f"<p style='font-size:20px'>• {definition}</p>", unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ Unexpected format for word **{word}**.")
    else:
        st.warning(f"🚫 The word **{word}** was not found in the dictionary.")