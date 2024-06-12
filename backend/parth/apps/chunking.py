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
import asyncio
from chromadb.utils import embedding_functions

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

async def chunking(text):
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
    return docs
    
gemini_key = os.getenv("GEMINI_KEY")

genai.configure(api_key=gemini_key)
    
class GeminiEmbeddingFunction(EmbeddingFunction):
    def __call__(self, input: Documents) -> Embeddings:
        model = "models/text-embedding-004"
        title = 'API'
        return genai.embed_content(
            model=model,
            content=input,
            title=title)["embedding"]
    

async def create_chroma_db(docs,name):
    try:
        chroma_client = chromadb.PersistentClient(path="D:/Competitions/KLEOS/backend/backend/parth/apps/database") 
        print(f"\n\nChroma Client:\n{chroma_client}\n\n")
        db = chroma_client.get_or_create_collection(
            name=name, embedding_function=GeminiEmbeddingFunction())
        print(f"\n\nDB:\n{db}\n\n")
        initial_size = db.count()
        for i, d in tqdm(enumerate(docs), total=len(docs), desc="D:/Competitions/KLEOS/backend/backend/parth/apps/database"):
            db.add(
                documents=d,
                ids=str(i + initial_size)
            )
            print(f"\n\nD in Docs is:\n{d}\n\n")
            time.sleep(0.5)
        return db
    except Exception as e:
        print(f"\n\nError in create chroma db:\n{e}")
        return e
    


async def get_chroma_db(name):
    chroma_client = chromadb.PersistentClient(path="D:/Competitions/KLEOS/backend/backend/parth/apps/database") # Here as well 
    return chroma_client.get_collection(name=name, function=EmbeddingFunction())

async def generating_db(pdf_path):
    text = await extract_text(pdf_path)
    docs = await chunking(text)
    print(f"\n\nDocs:\n{docs}\n\n")
    db = await create_chroma_db(docs,'valid_data')
    return db

async def main():
    pdf_path = './cyber_learn.pdf'
    op = await generating_db(pdf_path)
    print(op)

asyncio.run(main())
# text = extract_text(pdf_path)
# print(text)

