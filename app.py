import streamlit as st
import io
from gtts import gTTS
from backend.extractor import extract_text_from_pdf, fetch_abstract_from_doi
from backend.scorer import get_readability_score, get_grade_level
from backend.simplifier import simplify_text_with_gemini
from backend.glossary import detect_jargon

# 1. Page Configuration
st.set_page_config(page_title="Scientific Abstract Simplifier", page_icon="🧠", layout="wide")

st.title("🧠 Scientific Abstract Simplifier")
st.markdown("Instantly translate complex research papers into plain English.")

# 2. Sidebar for Advanced Features (Step 4 of Blueprint)
st.sidebar.header("Settings")
level_options = {"10-year-old": "5th grade", "High Schooler": "8th grade", "Non-expert Adult": "12th grade"}
selected_level = st.sidebar.selectbox("Target Reading Level", list(level_options.keys()), index=1)
target_grade_level = level_options[selected_level]
# NEW: Language Selector
language_options = ["English", "Hindi", "Punjabi", "Spanish", "French"]
selected_language = st.sidebar.selectbox("Output Language", language_options, index=0)

# 3. Input Layer (Tabs)
tab_text, tab_pdf, tab_doi = st.tabs(["📝 Paste Text", "📄 Upload PDF", "🔗 Enter DOI"])

raw_text = ""

with tab_text:
    text_input = st.text_area("Paste the abstract here:", height=200)
    if text_input:
        raw_text = text_input

with tab_pdf:
    uploaded_file = st.file_uploader("Upload a Research Paper (PDF)", type="pdf")
    if uploaded_file:
        raw_text = extract_text_from_pdf(uploaded_file.getvalue())
        st.success("PDF loaded successfully!")
        with st.expander("👀 View Extracted Text (Verify the abstract is here)"):
            st.write(raw_text)

with tab_doi:
    doi_input = st.text_input("Enter a DOI (e.g., 10.1038/nature12373)")
    if doi_input:
        with st.spinner("Fetching from database..."):
            raw_text = fetch_abstract_from_doi(doi_input)
            if "Error" not in raw_text and "No abstract" not in raw_text:
                st.success("Abstract fetched successfully!")
            else:
                st.error(raw_text)
                raw_text = ""

# 4. Processing & Output Layer
st.divider()

if raw_text and st.button("Simplify Abstract", type="primary"):
    orig_score = get_readability_score(raw_text)
    orig_grade = get_grade_level(raw_text)

    with st.spinner("Analyzing and simplifying with AI..."):
        hard_words = detect_jargon(raw_text)
        result = simplify_text_with_gemini(raw_text, target_level=target_grade_level, language=selected_language)

        if "error" in result:
            st.error(result["error"])
        else:
            new_score = get_readability_score(result.get("plain_summary", ""))
            new_grade = get_grade_level(result.get("plain_summary", ""))

            st.success(f"**🎯 Core Finding:** {result.get('core_finding', '')}")

            col1, col2 = st.columns(2)
            with col1:
                st.metric(label="Original Readability (Score / Grade)", value=f"{orig_score} / {orig_grade}")
            with col2:
                st.metric(label="New Readability (Score / Grade)", value=f"{new_score} / {new_grade}", delta=f"+{round(new_score - orig_score, 1)} points")

            st.markdown("### 📝 Simple Summary")
            summary_text = result.get("plain_summary", "")
            st.write(summary_text)

            if summary_text:
                with st.spinner("Generating audio..."):
                    try:
                        audio_bytes = io.BytesIO()
                        tts = gTTS(text=summary_text, lang='en')
                        tts.write_to_fp(audio_bytes)
                        st.audio(audio_bytes, format="audio/mp3")
                    except Exception as e:
                        st.warning(f"Could not generate audio: {e}")

            st.markdown("### 📌 Key Takeaways")
            for point in result.get("key_takeaways", []):
                st.markdown(f"- {point}")

            with st.expander("📖 Glossary of Terms"):
                glossary = result.get("glossary", {})
                if glossary:
                    for term, definition in glossary.items():
                        st.markdown(f"**{term.capitalize()}:** {definition}")
                else:
                    st.write("No complex terms detected.")

            st.divider()
            st.markdown("### 💾 Save & Share")

            report_content = f"""# 🧠 Simplified Abstract Report\n\n## 🎯 Core Finding\n{result.get('core_finding', '')}\n\n## 📝 Simple Summary\n{result.get('plain_summary', '')}\n\n## 📌 Key Takeaways\n"""
            
            for point in result.get("key_takeaways", []):
                report_content += f"- {point}\n"

            report_content += "\n## 📖 Glossary of Terms\n"
            
            for term, definition in result.get("glossary", {}).items():
                report_content += f"- **{term.capitalize()}**: {definition}\n"

            st.download_button(
                label="📥 Download Report (.md)",
                data=report_content,
                file_name="simplified_abstract_report.md",
                mime="text/markdown",
                type="primary"
            )