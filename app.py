import streamlit as st
import subprocess
import sys
import json
import uuid

from pathlib import Path

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parent
RESULTS_DIR = PROJECT_DIR / "output-results"

st.set_page_config(page_title="Reel to Text", page_icon="📚", layout="centered")

# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
<style>
    .stApp {
        background: #101114;
        color: #f5f5f5;
    }

    .block-container {
        max-width: 850px;
        padding-top: 4rem;
        padding-bottom: 4rem;
    }

    .hero {
        text-align: center;
        margin-bottom: 2.5rem;
    }

    .hero-title {
        font-size: 2.8rem;
        font-weight: 750;
        letter-spacing: -1.5px;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }

    .hero-subtitle {
        color: #999da8;
        font-size: 1rem;
    }

    .section-title {
        font-size: 1.3rem;
        font-weight: 650;
        margin-top: 2rem;
        margin-bottom: 1rem;
        color: #ffffff;
    }

    .result-card {
        background: #1b1d23;
        border: 1px solid #30333c;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
        transition: border-color 0.2s ease;
    }

    .result-card:hover {
        border-color: #8b7cff;
    }

    .result-number {
        color: #9c8cff;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .result-title {
        color: #ffffff;
        font-size: 1.15rem;
        font-weight: 650;
        line-height: 1.4;
    }

    .result-creator {
        color: #a4a6b0;
        font-size: 0.9rem;
        margin-top: 8px;
    }

    .empty-state {
        text-align: center;
        padding: 2.5rem 1rem;
        background: #1b1d23;
        border: 1px dashed #393c46;
        border-radius: 14px;
        color: #a4a6b0;
    }

    div.stButton > button {
        background: #7965ed;
        color: white;
        border: none;
        border-radius: 10px;
        min-height: 48px;
        font-weight: 650;
        width: 100%;
    }

    div.stButton > button:hover {
        background: #8b79fa;
        color: white;
        border: none;
    }

    div[data-testid="stTextInput"] input {
        background: #1b1d23;
        color: white;
        border: 1px solid #393c46;
        border-radius: 10px;
        min-height: 48px;
    }

    div[data-testid="stTextInput"] input:focus {
        border-color: #8b7cff;
        box-shadow: 0 0 0 1px #8b7cff;
    }

    hr {
        border-color: #30333c;
    }
</style>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
<div class="hero">
    <div class="hero-title">Reel to Text</div>
    <div class="hero-subtitle">
        Discover books, comics and movies hidden in your Instagram Reels.
    </div>
</div>
""",
    unsafe_allow_html=True,
)

# --------------------------------------------------
# INPUT
# --------------------------------------------------

st.markdown("### Paste an Instagram Reel URL")

url = st.text_input(
    "Instagram URL",
    placeholder="https://www.instagram.com/reel/...",
    label_visibility="collapsed",
)

extract_button = st.button(
    "Extract recommendations", type="primary", use_container_width=True
)

# This placeholder will hold either the spinner or results.
results_area = st.empty()

# --------------------------------------------------
# PIPELINE
# --------------------------------------------------

if extract_button:

    if not url.strip():
        st.warning("Please enter an Instagram URL.")

    elif "instagram.com/" not in url.lower():
        st.warning("Please enter a valid Instagram URL.")

    else:

        target_name = f"reel_{uuid.uuid4().hex[:8]}"

        command = [
            sys.executable,
            "-u",
            str(PROJECT_DIR / "reels_to_text.py"),
            target_name,
            url.strip(),
        ]

        with results_area.container():

            st.markdown(
                '<div class="section-title">Your recommendations</div>',
                unsafe_allow_html=True,
            )

            try:
                with st.spinner(
                    "Processing your Reel. Downloading, transcribing and extracting titles..."
                ):

                    process = subprocess.run(
                        command,
                        cwd=PROJECT_DIR,
                        capture_output=True,
                        text=True,
                        encoding="utf-8",
                        errors="replace",
                    )

                if process.returncode != 0:

                    st.error("The extraction process failed.")

                    with st.expander("View error details"):
                        st.code(process.stdout + "\n" + process.stderr)

                else:

                    result_path = RESULTS_DIR / f"{target_name}.json"

                    if not result_path.exists():

                        st.error(
                            "The pipeline finished, but the result file was not found."
                        )

                    else:

                        with open(result_path, "r", encoding="utf-8") as file:
                            results = json.load(file)

                        items = results.get("items", [])

                        if not items:

                            st.markdown(
                                """
                            <div class="empty-state">
                                <h3>No recommendations found</h3>
                                <p>
                                    We couldn't identify any named books,
                                    comics or movies in this Reel.
                                </p>
                            </div>
                            """,
                                unsafe_allow_html=True,
                            )

                        else:

                            st.success(f"Found {len(items)} recommendations")

                            for index, item in enumerate(items, start=1):

                                title = item.get("title", "Unknown title")
                                creator = item.get("creator")

                                creator_html = ""

                                if creator:
                                    creator_html = (
                                        f'<div class="result-creator">'
                                        f"By {creator}</div>"
                                    )

                                st.markdown(
                                    f"""
                                <div class="result-card">
                                    <div class="result-number">
                                        Recommendation {index:02d}
                                    </div>
                                    <div class="result-title">
                                        {title}
                                    </div>
                                    {creator_html}
                                </div>
                                """,
                                    unsafe_allow_html=True,
                                )

            except Exception as error:
                st.error("An unexpected error occurred.")
                st.exception(error)
