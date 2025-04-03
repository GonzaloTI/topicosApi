from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os
import hashlib

load_dotenv()

class ChromaDBManager:
    def __init__(self):
        self.FILE_PATH = "datos.txt"
        self.PERSIST_DIR = "chroma_db"
        self.EMBEDDINGS = OpenAIEmbeddings()
        self.vectorstore = self._initialize_chroma()

    def _get_file_hash(self, file_path):
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def _initialize_chroma(self):
        current_hash = self._get_file_hash(self.FILE_PATH)
        
        if os.path.exists(self.PERSIST_DIR) and os.path.exists(f"{self.PERSIST_DIR}/hash.txt"):
            with open(f"{self.PERSIST_DIR}/hash.txt", "r") as f:
                saved_hash = f.read()
            
            if saved_hash == current_hash:
                print("✅ Usando embeddings existentes")
                return Chroma(
                    persist_directory=self.PERSIST_DIR,
                    embedding_function=self.EMBEDDINGS
                )
            else:
                return self._reload_documents(current_hash)
        else:
            return self._reload_documents(current_hash)

    def _reload_documents(self, current_hash):
        loader = TextLoader(self.FILE_PATH, encoding="utf-8")
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        texts = text_splitter.split_documents(documents)
        
        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=self.EMBEDDINGS,
            persist_directory=self.PERSIST_DIR
        )
        
        os.makedirs(self.PERSIST_DIR, exist_ok=True)
        with open(f"{self.PERSIST_DIR}/hash.txt", "w") as f:
            f.write(current_hash)
        
        return vectorstore

    def query_documents(self, query, k=2):
        docs = self.vectorstore.similarity_search(query, k=k)
        return [{"content": doc.page_content, "metadata": doc.metadata} for doc in docs]