from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import *

from sentence_transformers import SentenceTransformer
model_name = "bert-base-chinese"
model = SentenceTransformer(model_name)

class LinFaiss:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="bert-base-chinese")

    def load_data(self):
        loader = WebBaseLoader([
           "https://milvus.io/docs/overview.md",
        ])
        data = loader.load()
        print(data)
        text_splitter = CharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
        docs = text_splitter.split_documents(data)
        print(docs)
        return docs

    def get_embeddings(self, docs):

        vector_store = FAISS.from_documents(
            docs,
            embedding=self.embeddings
        )
        return vector_store

    def documents2dict(self, documents):
        # 将Document对象列表转换为字典
        documents_dict = [
            {'page_content': document.page_content, 'metadata': document.metadata}
            for document in documents
        ]
        return documents_dict

    def save_vec_data(self, index="LinChance_GPT/apps/faiss_index"):
        docs = self.load_data()
        vector_store = self.get_embeddings(docs)
        vector_store.save_local(index)

    def get_similarity_documents(self, q, index="LinChance_GPT/apps/faiss_index", limit=3):
        db = FAISS.load_local(index, self.embeddings)
        docs = db.similarity_search(q, k=limit)
        texts = self.documents2dict(docs)
        return texts


# if __name__ == "__main__":
#     linfaiss = LinFaiss()
#     linfaiss.save_vec_data()
#     query = "How to use Milvus?"
#     similar_doc = linfaiss.get_similarity_documents(query)

