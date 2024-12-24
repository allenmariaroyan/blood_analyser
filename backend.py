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
import time


# Initialize ChromaDB
def initialize_chroma():
    client = chromadb.PersistentClient(path="./blood_db")
    return client

# Function to load and split PDF
def load_and_split_pdf(file_path):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    docs = text_splitter.split_documents(documents)
    return docs

# Function to store documents in ChromaDB
def store_documents(client, docs):
    embedding = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')
    vector_store = Chroma(client=client, collection_name="blood_reports", embedding_function=embedding)
    ids = [str(uuid.uuid4()) for _ in range(len(docs))]
    vector_store.add_documents(documents=docs, ids=ids)
    return vector_store

# Function to query Groq model
def query_key_values(vector_store, query, llm):
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

# Function to generate prediction
def generate_prediction(vulnerabilities, llm):
    prompt_template = PromptTemplate(
        input_variables=["content"],
        template="""Given the following blood component's values, provide a description for each blood component first.
        Then, as a separate part, predict whether the particular person's vulnerabilities to diseases which are related and dependent on one or more blood components listed in the content.
        Provide the level of vulnerability as a separate part in a bullet point format.
        Finally, give two to three line suggestions to reduce vulnerability in another bullet points format.
        Return all results in structured format.

        {content}
        """
    )
    content = "\n".join([f"{key}: {value}" for key, value in vulnerabilities.items()])
    formatted_prompt = prompt_template.format(content=content)

    chain = LLMChain(llm=llm, prompt=prompt_template)
    description = chain.run(content=formatted_prompt)
    stream_response(description)
    return description


def stream_response(response_text, chunk_size=15, delay=0.1):
    start = 0
    while start < len(response_text):
        # Get the next chunk of text
        chunk = response_text[start:start + chunk_size]
        yield chunk
        start += chunk_size
        time.sleep(delay)
