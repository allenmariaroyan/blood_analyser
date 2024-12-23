# Blood Report Analysis and Vulnerability Prediction

This project provides a comprehensive solution for processing and analyzing blood report PDFs. It extracts key health parameters, predicts potential health vulnerabilities, and generates detailed descriptions of associated health risks. The system leverages Groq AI for query-based data extraction and vulnerability prediction, with ChromaDB for document storage and efficient retrieval.

---

## Features

- **PDF Upload and Processing:** Enables users to upload blood report PDFs and processes them to extract critical medical parameters.  
- **Text Extraction:** Extracts essential values from the PDF report (e.g., vitamin levels, cholesterol, blood markers).  
- **Vulnerability Prediction:** Analyzes extracted values to predict health vulnerabilities such as anemia, thyroid dysfunction, or kidney disease.  
- **Vulnerability Descriptions:** Generates detailed, structured health vulnerability descriptions, including severity and recommended lifestyle changes.  
- **ChromaDB Integration:** Utilizes ChromaDB for storing and retrieving processed document data efficiently.

---

## Technologies Used

- **Streamlit:** Interactive web interface for user interaction.  
- **Groq AI:** For querying extracted values and generating predictions and descriptions.  
- **ChromaDB:** For managing and retrieving document embeddings.  
- **HuggingFace Embeddings:** For transforming text into vector embeddings for similarity search.  
- **LangChain:** Facilitates text splitting, document loading, and chaining LLM queries.

---

## Setup Instructions

### Prerequisites

1. **Python 3.8+**: Ensure Python is installed on your system.  
2. **Install dependencies** using the following command:  
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Create a `.env` file in the root directory.
   - Add your Groq AI API key to the `.env` file:
     ```
     GROQ_API_KEY=your_groq_api_key_here
     ```

### Running the Application

To start the application, run the following command in your terminal:
```bash
streamlit run app.py
```
This will launch the Streamlit application in your default web browser.

---

## File Structure

```
.
├── app.py                # Streamlit app for UI and results display
├── backend.py            # Core logic for document processing, querying, and prediction
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables, including GROQ_API_KEY
├── data/                 # Folder for processed data storage (if applicable)
└── README.md             # Project documentation
```

---

## How It Works

1. **Uploading the Report:**
   - Users upload a PDF of a blood report through the Streamlit interface.

2. **Document Loading and Text Extraction:**
   - The `load_and_split_pdf` function extracts and splits the document into manageable chunks for processing.

3. **Storing Documents in ChromaDB:**
   - Document text is embedded using HuggingFace embeddings and stored in a ChromaDB instance for efficient similarity search.

4. **Extracting Key Health Parameters:**
   - Groq AI extracts specific blood components (e.g., Vitamin B12, RBC count) from the document.

5. **Vulnerability Prediction:**
   - Extracted values are compared against pre-defined thresholds to predict vulnerabilities like anemia or thyroid dysfunction.

6. **Vulnerability Description Generation:**
   - Groq AI generates detailed descriptions of each predicted vulnerability, including severity levels and suggested lifestyle changes.

---

## Example Output

### Key Blood Component Values
| Parameter           | Value      |
|---------------------|------------|
| Vitamin B12         | 150        |
| RBC Count           | 4.1        |
| Platelet Count      | 180,000    |
| Thyroxine           | 7.5        |
| Creatinine          | 1.1        |

### Predicted Vulnerabilities
| Condition                  | Risk Level |
|----------------------------|------------|
| Vitamin B12 Deficiency and Anemia | High       |
| Thyroid Dysfunction         | Low        |
| Chronic Kidney Disease (CKD) | Low        |

### Vulnerability Descriptions
- **Vitamin B12 Deficiency and Anemia:**
  - **Description:** A condition where the body lacks sufficient Vitamin B12, potentially leading to anemia.
  - **Risk Level:** High
  - **Suggested Changes:** Increase Vitamin B12 intake through diet or supplements.

---

### Streamlit Demo

<img width="1440" alt="Screenshot 2024-12-23 at 3 57 42 PM" src="https://github.com/user-attachments/assets/47faac96-dd4a-4c8a-975d-ee1a3a57433d" />

<img width="1440" alt="Screenshot 2024-12-23 at 3 57 59 PM" src="https://github.com/user-attachments/assets/df859cd9-706e-4fa6-bc3a-dd141f487300" />

<img width="1440" alt="Screenshot 2024-12-23 at 3 58 14 PM" src="https://github.com/user-attachments/assets/35423c85-27ec-4a71-8694-d691b80965da" />

<img width="1440" alt="Screenshot 2024-12-23 at 3 58 14 PM" src="https://github.com/user-attachments/assets/ba9a43b4-ca46-49d9-9ac4-35f8b2311762" />

<img width="1440" alt="Screenshot 2024-12-23 at 3 58 16 PM" src="https://github.com/user-attachments/assets/f29c6c06-5269-46cd-bf3b-cc9859221f0a" />

<img width="1440" alt="Screenshot 2024-12-23 at 3 58 19 PM" src="https://github.com/user-attachments/assets/5d11bf7b-1bb4-42dd-9d59-1e56ed49600b" />









 
