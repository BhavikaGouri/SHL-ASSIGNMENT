import json
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
load_dotenv()
with open("data/catalog.json", "r", encoding="utf-8") as f:
    pages = json.load(f)


documents = []
for page in pages:
    documents.append(
        Document(
            page_content=page["content"],
            metadata={
                "title": page["title"],
                "url": page["url"]
            }
        )
    )
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
vector_db = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="data/chroma_db"
)
print(f"Indexed {len(documents)} documents.")