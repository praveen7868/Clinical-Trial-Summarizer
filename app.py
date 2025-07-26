import streamlit as st
import PyPDF2
from transformers import pipeline

st.set_page_config(page_title="Clinical Trial Summarizer", layout="centered")
st.title("Clinical Trial Report Summarizer")

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

input_method = st.radio("Choose Input Method:", ["Upload PDF", "Paste Trial Text"])
trial_text = ""

if input_method == "Upload PDF":
    uploaded_file = st.file_uploader("Upload Clinical Trial PDF", type="pdf")
    if uploaded_file:
        reader = PyPDF2.PdfReader(uploaded_file)
        trial_text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])

elif input_method == "Paste Trial Text":
    trial_text = st.text_area("Paste Clinical Trial Report Text Here", height=300)

trial_text = "\n".join([line for line in trial_text.splitlines() if len(line.strip()) > 30])
trial_text = trial_text[:3000]

summary_length = st.slider("Choose Summary Length (Max Tokens)", 50, 300, 150)

if st.button("Summarize Report"):
    if not trial_text.strip():
        st.error("Please upload or paste some content.")
    else:
        with st.spinner("Generating summary..."):
            try:
                chunks = [trial_text[i:i + 1000] for i in range(0, len(trial_text), 1000)]
                summaries = []
                for i, chunk in enumerate(chunks):
                    st.write(f"Processing chunk {i + 1}/{len(chunks)}...")
                    result = summarizer(chunk, max_length=summary_length, min_length=30, do_sample=False)[0]['summary_text']
                    summaries.append(result)
                summary = "\n\n".join(summaries)
                st.success("Summary Generated!")
                st.text_area("Trial Summary", summary, height=300)
                st.download_button("Download Summary", summary, file_name="summary.txt", mime="text/plain")
            except Exception as e:
                st.error(f"Error: {e}")
