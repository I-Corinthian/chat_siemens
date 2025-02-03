import streamlit as st
import siemens_rag as srag

st.title("Chat Siemens")


plc_model = st.selectbox("Model you want to query about", ("S7-1200", "S7-1500"))

user_prompt = st.text_area("ASK YOUR QUESTIONS:", placeholder="E.g., How can I connect an HMI to my PLC?")

if st.button("Ask Siemens"):
    if user_prompt:
        st.subheader("Generated Answer")
        output_placeholder = st.empty()

        full_response = ""
        for chunk in srag.call(input=user_prompt,plc_model=plc_model):
            full_response = chunk
            output_placeholder.write(full_response)

    else:
        st.warning("Please enter a question before submitting.")
