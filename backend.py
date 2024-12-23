import os
import chromadb
from chromadb.config import Settings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
import re
import uuid

from dotenv import load_dotenv
import os

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Step 1: Load PDF and extract text
def load_and_split_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = text_splitter.split_documents(documents)
    return docs

# Step 2: Initialize ChromaDB
def initialize_chroma():
    client = chromadb.PersistentClient(path="./blood_db")
    return client

# Step 3: Embed and store the documents
def store_documents(client, docs):
    embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    vector_store = Chroma(client=client, collection_name="blood_reports", embedding_function=embedding)
    ids = [str(uuid.uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(documents=docs, ids=ids)
    return vector_store

# Step 4: Query Groq model to extract key values
def query_key_values(vector_store, query):
    llm = ChatGroq(
        api_key= GROQ_API_KEY,
        model="llama3-8b-8192"
    )
    key_values = {}

    for que in query:
        prompt_template = PromptTemplate(
            input_variables=["content", "query"],
            template="""Extract the following key component: {query} from the given content.
            {content}
            Provide clear output(single value in number) in key-value format."""
        )
        chain = LLMChain(llm=llm, prompt=prompt_template)
        results = vector_store.similarity_search(que)
        contents = "\n".join([result.page_content for result in results])
        response = chain.run(content=contents, query=que)
        match = re.search(r'(?<=[:\s])(\d+\.\d+|\d+)(?=\s|\b)', response)
        if match:
            key_values[que] = match.group()
    return key_values

# Predict vulnerabilities based on extracted values
def predict_vulnerability(values):
    vulnerabilities = {}
    vitamin_b12 = float(values.get("vitamin b12", 0))
    rbc_count = float(values.get("RBC COUNT", 0))
    platelet_count = float(values.get("PLATELET COUNT", 0))
    thyroxine = float(values.get("THYROXINE", 0))
    creatinine = float(values.get("CREATININE", 0))
    bun = float(values.get("BLOOD UREA NITROGEN", 0))
    uric_acid = float(values.get("URIC ACID", 0))
    neutrophils = float(values.get("NEUTROPHILS", 0))
    total_cholesterol = float(values.get("TOTAL CHOLESTEROL", 0))

    if vitamin_b12 < 200 and rbc_count < 4.2:
        vulnerabilities["Vitamin B12 Deficiency and Anemia"] = "High"
    elif vitamin_b12 >= 200 and rbc_count >= 4.2 and platelet_count >= 150000:
        vulnerabilities["Vitamin B12 Deficiency and Anemia"] = "Low"
    else:
        vulnerabilities["Vitamin B12 Deficiency and Anemia"] = "Moderate"

    if thyroxine < 4.5:
        vulnerabilities["Hypothyroidism"] = "High"
    elif thyroxine > 11.2:
        vulnerabilities["Hyperthyroidism"] = "High"
    else:
        vulnerabilities["Thyroid Dysfunction"] = "Low"

    if creatinine > 1.2 or bun > 20:
        vulnerabilities["Chronic Kidney Disease (CKD)"] = "High"
    else:
        vulnerabilities["Chronic Kidney Disease (CKD)"] = "Low"

    if uric_acid > 6.8:
        vulnerabilities["Gout"] = "High"
    else:
        vulnerabilities["Gout"] = "Low"

    if neutrophils > 8000:
        vulnerabilities["Infection"] = "High"
    elif neutrophils < 1500:
        vulnerabilities["Immune Deficiency"] = "High"
    else:
        vulnerabilities["Infection/Immune Status"] = "Normal"

    if total_cholesterol > 240:
        vulnerabilities["Cardiovascular Disease"] = "High"
    elif total_cholesterol <= 200:
        vulnerabilities["Cardiovascular Disease"] = "Low"
    else:
        vulnerabilities["Cardiovascular Disease"] = "Moderate"

    return vulnerabilities

# Generate vulnerability descriptions using Groq
def generate_description(vulnerabilities):
    llm = ChatGroq(
        api_key= GROQ_API_KEY,
        model="llama3-8b-8192"
    )
    prompt_template = PromptTemplate(
    input_variables=["content"],
    template="""List each health vulnerability below in structured bulleted points. Include:  

        • Description of the condition  
        • Vulnerability level  
        • Suggested changes to reduce vulnerability  

    Strictly present only the structured points without any introductory text.
    {content}
    """
    )

    content = "\n".join([f"{disease}: {vulnerability}" for disease, vulnerability in vulnerabilities.items()])
    chain = LLMChain(llm=llm, prompt=prompt_template)
    return chain.run(content=content)
