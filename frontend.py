# Setup libraries
import os
import streamlit as st 
from backend import get_chain, analyse


# Context
st.title("Auto Accessibility Checker")
st.write("Uses AI models to check obvious errors in the W3C-WAI accessibility standards.")

# Search inputs
with st.sidebar:
    with st.form(key='user_input'):
        key = st.text_input("OpenAI API Key", max_chars=60, placeholder="Enter an OpenAI API Key")
        model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4-turbo"], index=0)
        code = st.text_area("Code", placeholder="Paste your HTML code here")
        submit = st.form_submit_button("Analyse")

if submit and code:
    st.write("Analysing:")
    st.write(f"```html\n{code}\n```")

    # Get output
    chain = get_chain(key, model)
    results = analyse(chain, code)

    # Show summary results
    st.write(f"\n**Here are the results**:\n{results.content}")

# Error message
elif submit and not code:
    st.write("No code snippet to analyse.")