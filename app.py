import streamlit as st
import boto3
import json

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
            region_name="us-east-1"
        )

        prompt = f"""Human: Summarize the following clinical trial report in 2-3 sentences:\n{input_text}\n\nAssistant:"""

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "prompt": prompt,
            "max_tokens": 300,
            "temperature": 0.7,
            "top_k": 250,
            "top_p": 0.9,
            "stop_sequences": ["\n\nHuman:"]
        }

        response = bedrock.invoke_model(
            modelId="anthropic.claude-v2",
            body=json.dumps(body),
            accept="application/json",
            contentType="application/json"
        )

        result_json = json.loads(response['body'].read())
        summary = result_json.get("completion", "No summary found.")

        st.success("Summary:")
        st.write(summary)
