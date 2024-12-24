import streamlit as st
from services import initialize_chroma, load_and_split_pdf, store_documents, query_key_values, generate_prediction,stream_response
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import os

st.title("📋 Blood Report Analysis and Vulnerability Prediction 💉🩸 ")


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

uploaded_file = st.file_uploader("📤 Upload Blood Report PDF", type=["pdf"])

if uploaded_file is not None:
    # Save uploaded file
    file_path = f"./{uploaded_file.name}"
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Load and process PDF
    st.write("🔄 Processing PDF...")
    docs = load_and_split_pdf(file_path)

    # Initialize ChromaDB
    chroma_client = initialize_chroma()

    # Store documents
    vector_store = store_documents(chroma_client, docs)
    st.write("Documents stored successfully! ✅ ")

    # Define Groq LLM
    llm = ChatGroq(
        api_key=GROQ_API_KEY,
        model="llama3-8b-8192"
    )

    # Queries for key values
    query = ["VITAMIN B12", "SODIUM", "RBC COUNT", "PLATELET COUNT", "CALCIUM",
             "CHLORIDE", "URIC ACID", "CREATININE", "BLOOD UREA NITROGEN",
             "THYROXINE", "TOTAL CHOLESTEROL", "NEUTROPHILS"]

    st.write("🔄 Extracting blood components values...")
    key_values = query_key_values(vector_store, query, llm)

    # Display key values in table format
    st.write("### **👩🏻‍⚕️ Extracted Key Values**")
    # st.table([(k, v) for k, v in key_values.items()])
    st.table([["<Blood Component>", "<Value>"]] + [(k, v) for k, v in key_values.items()])


    # Generate prediction
    st.write("Generating predictions...")
    prediction = generate_prediction(key_values, llm)
    
    prediction_stream = stream_response(prediction)
    # Display prediction
    st.write("### **👩🏻‍⚕️ Interpretations and Predictions**")
    st.write_stream(prediction_stream)

    # Cleanup
    os.remove(file_path)
