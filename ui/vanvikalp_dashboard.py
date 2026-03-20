import streamlit as st
import requests
import json
import os
import chromadb
from pypdf import PdfReader
from chromadb.utils import embedding_functions

# --- Configuration ---
# REPLACE THIS with your actual Cloud Run URL
CLOUD_RUN_URL = "https://vanvikalp-engine-733206344564.us-central1.run.app/generate"
DOCS_DIR = "compliance_docs"

st.set_page_config(page_title="VanVikalp EaaS Engine", page_icon="🍃", layout="wide")

# --- RAG Setup (Local Vector DB) ---
@st.cache_resource
def setup_vector_db():
    """Reads PDFs, chunks them, and stores them in a local ChromaDB."""
    client = chromadb.Client()
    
    # We use a lightweight, free local embedding model
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(name="esg_compliance", embedding_function=sentence_transformer_ef)
    
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        
    doc_id = 0
    # Scan the compliance_docs folder for PDFs
    for filename in os.listdir(DOCS_DIR):
        if filename.endswith(".pdf"):
            reader = PdfReader(os.path.join(DOCS_DIR, filename))
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    # Storing each page as a "chunk" in the database
                    collection.add(
                        documents=[text],
                        metadatas=[{"source": filename, "page": i}],
                        ids=[f"doc_{doc_id}"]
                    )
                    doc_id += 1
    return collection

collection = setup_vector_db()

# --- UI Layout ---
st.title("🍃 VanVikalp AI Engine")
st.markdown("**Environment as a Service (EaaS) Strategy Generator**")

# Sidebar for Authentication (Keeps your token out of the main screen)
with st.sidebar:
    st.header("⚙️ Engine Configuration")
    gcp_token = st.text_input("GCP Identity Token (ya29...)", type="password")
    st.info("Ensure you have placed IGBC/GRIHA PDFs in the `ui/compliance_docs/` folder for the RAG system to read.")

# Main Input Area
user_prompt = st.text_area("Describe the building, campus, or infrastructure challenge:", 
                           placeholder="e.g., We are modernizing the Calcutta University heritage campus. The courtyard floods...")

if st.button("Generate ESG Strategy", type="primary"):
    if not gcp_token:
        st.error("Please enter your GCP Identity Token in the sidebar.")
    elif not user_prompt:
        st.warning("Please enter a scenario prompt.")
    else:
        with st.spinner("Analyzing Compliance Documents & Waking up the Engine..."):
            
            # --- 1. The RAG Retrieval Step ---
            # Search the vector DB for the top 2 most relevant paragraphs based on user input
            results = collection.query(query_texts=[user_prompt], n_results=1)
            retrieved_context = "\n".join(results["documents"][0]) if results["documents"] else "No specific compliance rules found."
            
            # --- 2. The Augmentation Step ---
            # Combine the user's prompt with the official rules
            augmented_prompt = f"""
            User Scenario: {user_prompt}
            
            Strict Compliance Rules to Follow (from RAG Database):
            {retrieved_context}
            
            Provide the ESG strategy based on the scenario, strictly adhering to the compliance rules above.
            """
            
            # --- 3. The Generation Step (API Call) ---
            headers = {
                "Authorization": f"Bearer {gcp_token}",
                "Content-Type": "application/json"
            }
            payload = {"prompt": augmented_prompt}
            
            try:
                response = requests.post(CLOUD_RUN_URL, json=payload, headers=headers, timeout=300)
                
                if response.status_code == 200:
                    strategy_data = response.json()
                    
                    st.success("Strategy Generated Successfully!")
                    st.divider()
                    
                    # --- 4. Render the JSON into beautiful UI Cards ---
                    cols = st.columns(2)
                    for idx, (key, value) in enumerate(strategy_data.items()):
                        with cols[idx % 2]:
                            st.markdown(f"### {key.replace('_', ' ').title()}")
                            st.info(f"**Solution:** {value.get('solution', 'N/A')}")
                            st.success(f"**Impact:** {value.get('estimated_impact', 'N/A')}")
                            
                else:
                    st.error(f"Engine API Error {response.status_code}: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection Failed: {e}")