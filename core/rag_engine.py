from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from core.llm import get_llm
from core.vector_store import build_vector_store, build_vector_store_from_texts, load_vector_store, get_retriever

RAG_SYSTEM_PROMPT = """You are an expert assistant. Answer the user's question \
based ONLY on the context provided below (which may come from a meeting transcript, \
an uploaded document, or both).

If the answer is not found in the context, say: \
"I could not find this information in the provided content."

Always be concise and precise. If quoting someone, mention it clearly.

Context:
{context}"""


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def _make_rag_chain(retriever):
    llm = get_llm(temperature=0.3)
    prompt = ChatPromptTemplate.from_messages([
        ("system", RAG_SYSTEM_PROMPT),
        ("human", "{question}"),
    ])
    return (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def build_rag_chain(transcript: str):
    vector_store = build_vector_store(transcript)
    retriever = get_retriever(vector_store, k=4)
    return _make_rag_chain(retriever)


def build_rag_chain_from_docs(texts: list[str], source_labels: list[str] | None = None):
    """
    Build a RAG chain from one or more text sources (documents, transcripts, etc.).

    Parameters
    ----------
    texts : list[str]
        List of plain-text strings to index.
    source_labels : list[str] | None
        Optional human-readable label per text (e.g. "report.pdf").
    """
    vector_store = build_vector_store_from_texts(texts, source_labels)
    retriever = get_retriever(vector_store, k=4)
    return _make_rag_chain(retriever)


def load_rag_chain():
    vector_store = load_vector_store()
    retriever = get_retriever(vector_store, k=4)
    return _make_rag_chain(retriever)


def ask_question(rag_chain, question: str) -> str:
    question = question.strip()
    if not question:
        return "Please enter a question."
    return rag_chain.invoke(question)
