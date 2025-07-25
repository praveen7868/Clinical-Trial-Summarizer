import streamlit as st
import openai
import PyPDF2

st.set_page_config(page_title="Clinical Trial Summarizer", layout="centered")
st.title("Clinical Trial Report Summarizer")

openai_api_key = st.secrets["openai"]["api_key"]
openai.api_key = openai_api_key

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
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a clinical research expert. Summarize the clinical trial report into Objective, Methods, Results, and Conclusion."},
                        {"role": "user", "content": trial_text}
                    ],
                    temperature=0.3,
                    max_tokens=1000
                )
                summary = response.choices[0].message.content
                st.success("Summary Generated!")
                st.text_area("Trial Summary", summary, height=300)
            except Exception as e:
                st.error(f"Error: {e}")
                
