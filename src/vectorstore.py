import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from .document_loader import load_python_files, chunk_documents

VECTORSTORE_PATH = os.path.expanduser("~/CodeMentor-AI/data/faiss_index")

def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"}
    )

def build_vectorstore(folder_path: str):
    print("Loading documents...")
    docs = load_python_files(folder_path)
    print(f"Loaded {len(docs)} files")

    print("Chunking documents...")
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")

    print("Building embeddings (this may take a minute)...")
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    print(f"Saving vectorstore to {VECTORSTORE_PATH}...")
    vectorstore.save_local(VECTORSTORE_PATH)
    print("Done! Vectorstore built and saved.")
    return vectorstore

def load_vectorstore():
    embeddings = get_embeddings()
    return FAISS.load_local(
        VECTORSTORE_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

if __name__ == "__main__":
    folder = os.path.expanduser("~/CodeMentor-AI/data/Coding-solving-")
    vectorstore = build_vectorstore(folder)

    # Quick test
    print("\n--- Testing retrieval ---")
    query = "what is sliding window"
    results = vectorstore.similarity_search(query, k=2)
    for i, doc in enumerate(results):
        print(f"\nResult {i+1} (source: {doc.metadata.get('source')}):")
        print(doc.page_content[:200])
