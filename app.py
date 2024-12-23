import streamlit as st
from backend import load_and_split_pdf, initialize_chroma, store_documents, query_key_values, predict_vulnerability, generate_description
import uuid
import os

st.title("📋 Blood Report Analysis and Vulnerability Prediction 💉🩸 ")

uploaded_file = st.file_uploader("📤 Upload Blood Report", type=["pdf"])

if uploaded_file is not None:
    with open(f"temp_{uuid.uuid4().hex}.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())
    file_path = f.name
    
    st.subheader("🔄 Analysing Blood Report ...")
    docs = load_and_split_pdf(file_path)
    st.write("Report loaded and processed ✅ ")
    
    chroma_client = initialize_chroma()
    vector_store = store_documents(chroma_client, docs)
    
    # Query Key Values
    st.subheader("🧬 Extracting Blood Component Values...")
    query = [
        "vitamin b12", "SODIUM", "RBC COUNT", "PLATELET COUNT", "CALCIUM",
        "CHLORIDE", "URIC ACID", "CREATININE", "BLOOD UREA NITROGEN", 
        "THYROXINE", "TOTAL CHOLESTEROL", "NEUTROPHILS"
    ]
    key_values = query_key_values(vector_store, query)
    indexed_key_values = {str(i+1): {"Parameter": k, "Value": v} for i, (k, v) in enumerate(key_values.items())}

    # Display Key Values in Table
    st.subheader("Key Values")
    key_values_table = {"Parameter": list(key_values.keys()), "Value": list(key_values.values())}
    st.table(key_values_table)

    # Predict Vulnerabilities
    st.subheader("👩🏻‍⚕️ Predicting Vulnerabilities...")
    vulnerabilities = predict_vulnerability(key_values)

    # Display Vulnerabilities in Table
    vulnerabilities_table = {"Condition": list(vulnerabilities.keys()), "Risk Level": list(vulnerabilities.values())}
    st.table(vulnerabilities_table)
    
    st.subheader("👨🏻‍⚕️ Vulnerability Descriptions")
    description = generate_description(vulnerabilities)
    st.write(description)
    
    os.remove(file_path)
else:
    st.write("Please upload a Report file to begin.")
