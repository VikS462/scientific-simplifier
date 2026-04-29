# scientific-simplifier
# 🧠 Scientific Simplifier: AI-Powered Research Assistant


**Scientific Simplifier** is a web application that takes dense, jargon-heavy research papers and turns them into easy-to-understand summaries. Whether you are a student tackling a new subject or a researcher looking for a quick brief, this tool helps you grasp the "Core Finding" in seconds.

---

## 🚀 Features

* **Multi-Source Input:** Upload PDFs directly, paste raw text, or pull abstracts using a DOI.
* **Intelligent Simplification:** Uses **Google Gemini 2.5 Flash** to rewrite content for different audience levels (5th Grade to Non-expert Adult).
* **Readability Metrics:** Real-time calculation of the **Flesch-Kincaid Grade Level** to show exactly how much the text was simplified.
* **Multilingual Support:** Output summaries in English, Hindi, Punjabi, Spanish, and more.
* **Audio Summaries:** Integrated **Text-to-Speech (gTTS)** to listen to findings on the go.
* **Exportable Reports:** Download the simplified results as a Markdown file for your notes.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit (Python-based Web UI)
* **AI Engine:** Google Gemini 2.5 Flash API
* **PDF Processing:** PyMuPDF (fitz)
* **NLP & Metrics:** Textstat (Readability scoring)
* **Audio:** gTTS (Google Text-to-Speech)

---

