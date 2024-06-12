import PyPDF2
from dotenv import load_dotenv
from pprint import pprint
import pandas as pd
import chromadb
from chromadb import Documents, EmbeddingFunction, Embeddings
import google.generativeai as genai
from IPython.display import Markdown
from chromadb.api.types import Embeddings
import time
from tqdm import tqdm
from google.generativeai import GenerationConfig, GenerativeModel
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from parth.apps.chunking import chunking,create_chroma_db,create_content_embeddings_db,generating_db,get_chroma_db,MyEmbeddingFunction,extract_text

gemini_key = "AIzaSyD5detVlrgZRiQALy7k_L1_QGBHniUIXnc"

genai.configure(api_key=gemini_key)


# async def extract_text(pdf_path):
#     try:
#         extracted_text = ""
#         with open(pdf_path, 'rb') as file:
#             pdf_reader = PyPDF2.PdfReader(file)
#             num_pages = len(pdf_reader.pages)
#             for page_number in range(num_pages):
#                 page = pdf_reader.pages[page_number]
#                 extracted_text += page.extract_text()
#         print(extracted_text)
#         return extracted_text
#     except Exception as e:
#         print(f"The exception has occured at: {e}")
#         return e
    

# class GeminiEmbeddingFunction(EmbeddingFunction):
#     def __call__(self, input: Documents) -> Embeddings:
#         model = 'models/embedding-001'
#         title = 'API'
#         return genai.embed_content(
#             model=model,
#             content=input,
#             task_type="retrieval_document",
#             title=title)["embedding"]
    

# def create_chroma_db(docs,name):
#     chroma_client = chromadb.PersistentClient(path="/Users/mihiresh/Mihiresh/Work/Cheatbot/dsa-java") #Don't forget to change path
#     db = chroma_client.get_or_create_collection(
#         name=name, embedding_function=GeminiEmbeddingFunction())
    
#     initial_size = db.count()
#     for i, d in tqdm(enumerate(docs), total=len(docs), desc="/Users/mihiresh/Mihiresh/Work/Cheatbot/dsa-java"):
#         db.add(
#             documents=d,
#             ids=str(i + initial_size)
#         )
#         time.sleep(0.5)
#     return db


# def get_chroma_db(name):
#     chroma_client = chromadb.PersistentClient(path="/Users/mihiresh/Mihiresh/Work/Cheatbot/dsa-java") # Here as well 
#     return chroma_client.get_collection(name=name, function=EmbeddingFunction())


db = create_chroma_db(docs, "sme_db")
db.count()



def get_relevant_passages(query, db, n_results):
    passages = db.query(query_texts=[query], n_results=n_results)['documents'][0]
    return passages

model = genai.GenerativeModel('gemini-pro')

def extract_text_from_response(response):
    # Initialize an empty string to accumulate text
    extracted_text = ""
    
    # Check if the response has a 'parts' attribute and iterate over it if present
    if hasattr(response, 'parts'):
        for part in response.parts:
            if hasattr(part, 'text'):  # Ensure the part has a 'text' attribute
                extracted_text += part.text + "\n"  # Append the text from each part
    
    # Alternatively, if the structure is deeper (e.g., candidates with content parts):
    elif hasattr(response, 'candidates') and len(response.candidates) > 0:
        for candidate in response.candidates:
            for part in candidate.content.parts:
                if hasattr(part, 'text'):
                    extracted_text += part.text + "\n"
    
    return extracted_text.strip()  # Return the combined text, stripping any trailing newline


def list_to_string(passages):
    content = ""
    for passage in passages:
        content += passage + "\n"
    return content


def make_prompt(ques, knowledge, chats):
    text = knowledge.replace("'","").replace('"','') #even i dont know why i did this

    prompt = f"""question: {ques}.\n
    information base or knowledge base: {text}\n
    Answer the question strictly based from knowledge base by filtering the required information from knowledge base\n
    Generate a sophisticated and neat answer such that it could be written in ex\n
    If the knowledge base does not have data related to the question reply with "Out of Syllabus"
    If the question is asking for a code then also explain the algorithm,\n 
    if the question is asking for career guidance then provide complete career guidance and links for various courses, \n
    if difference is asked differentiate with minimum 7 points in tabular format and one example
    """

    gen_config = GenerationConfig(temperature=0.1)
    answer_text = model.generate_content(prompt,generation_config=gen_config)
    answer = extract_text_from_response(answer_text)
    
    return answer


async def chatbot_response(ques, user_id):
    passages = get_relevant_passages(ques, db, n_results=25) #i have kept the n_results more because i wanted more info to be included in my answwer
    txt = ""
    for passage in passages:
        txt += passage


    cont = list_to_string(passages)
    answer = make_prompt(ques, cont)
    
    return answer

    