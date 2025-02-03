from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS


class Vectordbquery():
    def __init__(self):
        self.embedding = OllamaEmbeddings(model='nomic-embed-text:latest')
        self.current_path = ""

    def set_loader(self, path):
        self.current_path = path
        self.db = FAISS.load_local(folder_path=self.current_path, embeddings=self.embedding, allow_dangerous_deserialization=True)

    def query(self, text, path, top_k=5):
        if self.current_path != path:
            self.set_loader(path=path)
        
        results = self.db.similarity_search_with_score(text, k=top_k)
        return [(res[0].page_content, res[1]) for res in results]

