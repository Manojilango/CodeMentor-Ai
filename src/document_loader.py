import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def load_python_files(folder_path: str) -> list[Document]:
    """Load all .py files from a folder as documents"""
    documents = []
    for root, dirs, files in os.walk(folder_path):
        # skip hidden/venv/git folders
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'venv']
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    if content.strip():
                        documents.append(
                            Document(
                                page_content=content,
                                metadata={"source": file, "path": filepath}
                            )
                        )
                except Exception as e:
                    print(f"Skipped {filepath}: {e}")
    return documents

def chunk_documents(documents: list[Document]) -> list[Document]:
    """Split documents into smaller chunks for embedding"""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
        separators=["\n\nclass ", "\n\ndef ", "\n\n", "\n", " "]
    )
    return splitter.split_documents(documents)

if __name__ == "__main__":
    folder = os.path.expanduser("~/CodeMentor-AI/data/Coding-solving-")
    docs = load_python_files(folder)
    print(f"Loaded {len(docs)} files")
    
    chunks = chunk_documents(docs)
    print(f"Created {len(chunks)} chunks")
    
    if chunks:
        print("\nSample chunk:")
        print(chunks[0].page_content[:200])
        print(f"Source: {chunks[0].metadata}")
