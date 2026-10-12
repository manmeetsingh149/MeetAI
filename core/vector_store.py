import os
import shutil

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "meeting_transcript"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embeddings():
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
    )


def _reset_persist_dir() -> None:
    if os.path.isdir(CHROMA_DIR):
        shutil.rmtree(CHROMA_DIR, ignore_errors=True)


def build_vector_store(transcript: str) -> Chroma:
    print("Building vector store...")
    _reset_persist_dir()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_text(transcript)
    docs = [
        Document(page_content=chunk, metadata={"chunk_index": i})
        for i, chunk in enumerate(chunks)
    ]

    embeddings = get_embeddings()
    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
    )


def build_vector_store_from_texts(
    texts: list[str],
    source_labels: list[str] | None = None,
) -> Chroma:
    """
    Build a vector store from multiple text sources.

    Parameters
    ----------
    texts : list[str]
        List of text strings to index (e.g. transcript + uploaded docs).
    source_labels : list[str] | None
        Optional label for each text (e.g. "transcript", "report.pdf").
        Falls back to "source_0", "source_1", … if not provided.
    """
    print("Building vector store from multiple texts...")
    _reset_persist_dir()

    if source_labels is None:
        source_labels = [f"source_{i}" for i in range(len(texts))]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    all_docs: list[Document] = []
    global_idx = 0
    for text, label in zip(texts, source_labels):
        chunks = splitter.split_text(text)
        for chunk in chunks:
            all_docs.append(
                Document(
                    page_content=chunk,
                    metadata={"chunk_index": global_idx, "source": label},
                )
            )
            global_idx += 1

    embeddings = get_embeddings()
    return Chroma.from_documents(
        documents=all_docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
    )


def load_vector_store() -> Chroma:
    if not os.path.isdir(CHROMA_DIR):
        raise FileNotFoundError(
            f"No saved vector store at '{CHROMA_DIR}'. Run analysis first."
        )
    embeddings = get_embeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def get_retriever(vector_store: Chroma, k: int = 4):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )
