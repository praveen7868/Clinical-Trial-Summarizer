import streamlit as st
import PyPDF2
from transformers import pipeline

st.set_page_config(page_title="Clinical Trial Summarizer", layout="centered")
st.title("Clinical Trial Report Summarizer")

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

input_method = st.radio("Choose Input Method:", ["Upload PDF", "Paste Trial Text"])
trial_text = ""

if input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload Clinical Trial PDF", type="pdf")
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        trial_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

elif input_method == "Paste Trial Text":
    trial_text = st.text_area("Paste Clinical Trial Report Text Here", height=300)

if st.button("Summarize Report"):
    if not trial_text.strip():
        st.error("Please upload or paste some content.")
    else:
        with st.spinner("Generating summary..."):
            try:
                chunks = [trial_text[i:i+1000] for i in range(0, len(trial_text), 1000)]
                summaries = [summarizer(chunk, max_length=200, min_length=30, do_sample=False)[0]['summary_text'] for chunk in chunks]
                summary = "\n\n".join(summaries)
                st.success("Summary Generated!")
                st.text_area("Trial Summary", summary, height=300)
            except Exception as e:
                st.error(f"Error: {e}")
