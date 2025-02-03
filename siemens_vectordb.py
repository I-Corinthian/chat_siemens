from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS

loader = PyPDFDirectoryLoader(path='plc_data\s71500',glob='*.pdf')
doc = loader.load()


text_spliter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
text = text_spliter.split_documents(documents=doc)

embedding = OllamaEmbeddings(model='nomic-embed-text:latest')

db = FAISS.from_documents(documents=text,embedding=embedding)

db.save_local(folder_path='vector_db')