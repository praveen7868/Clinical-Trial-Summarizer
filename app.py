import streamlit as st
import boto3

st.set_page_config(page_title="AI Clinical Trial Report Summarizer", layout="centered")

st.title("🧠 AI Clinical Trial Report Summarizer")
st.markdown("Summarize structured clinical trial reports using Generative AI via AWS Bedrock.")

input_text = st.text_area("Paste your clinical trial report (structured format):", height=200)

if st.button("Summarize"):
    if not input_text.strip():
        st.warning("Please enter some text to summarize.")
    else:
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name="us-east-1"  # or your chosen region
        )

        body = {
            "prompt": f"Summarize this clinical trial report in 2-3 sentences:\n{input_text}",
            "max_tokens": 300,
            "temperature": 0.7,
            "top_k": 250,
            "top_p": 0.9,
            "stop_sequences": []
        }

        response = bedrock.invoke_model(
            modelId="amazon.titan-text-express-v1",
            body=str(body).encode("utf-8"),
            accept="application/json",
            contentType="application/json"
        )

        result = response['body'].read().decode('utf-8')
        st.success("Summary:")
        st.write(result)
