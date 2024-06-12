from pprint import pprint
import pandas as pd
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import google.generativeai as genai
from chromadb.api.types import Embeddings
import time
from tqdm import tqdm
from google.generativeai import GenerationConfig, GenerativeModel
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
import PyPDF2

async def extract_text(pdf_path):
    try:
        extracted_text = ""
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            num_pages = len(pdf_reader.pages)
            for page_number in range(num_pages):
                page = pdf_reader.pages[page_number]
                extracted_text += page.extract_text()
        print(extracted_text)
        return extracted_text
    except Exception as e:
        print(f"The exception has occured at: {e}")
        return e

def chunking(text):
    text_splitter = RecursiveCharacterTextSplitter (chunk_size = 1000,    #for next time let's try to keep the chunk size little bigger
                                                    chunk_overlap = 100,
                                                    length_function = len,
        add_start_index = True
    )
    texts = text_splitter.create_documents([text])
    docs = []
    for chunk in texts:
        docs.append(chunk.page_content)
    print(docs[:2])
    
gemini_key = os.getenv("GEMINI_KEY")

genai.configure(api_key=gemini_key)
    
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        model = 'models/embedding-001'
        title = 'API'
        return genai.embed_content(
            model=model,
            content=input,
            task_type="retrieval_document",
            title=title)["embedding"]
    

def create_chroma_db(docs,name):
    chroma_client = chromadb.PersistentClient(path="D:/Competitions/KLEOS/backend/backend/parth/apps/data_chat") 
    db = chroma_client.get_or_create_collection(
        name=name, embedding_function=GeminiEmbeddingFunction())
    
    initial_size = db.count()
    for i, d in tqdm(enumerate(docs), total=len(docs), desc="D:/Competitions/KLEOS/backend/backend/parth/apps/data_chat"):
        db.add(
            documents=d,
            ids=str(i + initial_size)
        )
        time.sleep(0.5)
    return db


def get_chroma_db(name):
    chroma_client = chromadb.PersistentClient(path="D:/Competitions/KLEOS/backend/backend/parth/apps/data_chat") # Here as well 
    return chroma_client.get_collection(name=name, function=EmbeddingFunction())

def generating_db(pdf_path):
    text = extract_text(pdf_path)
    docs = chunking(text)
    db = create_chroma_db(docs,'Creating database.')
    

