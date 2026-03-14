from app.services.pdf.text_cleaner import clean_pdf_text
from app.services.rag.chunker import chunk_text
from app.services.rag.embedder import embed_texts
from app.services.rag.vector_store import create_faiss_index
from app.services.rag.retriever import retrieve_top_k_chunks
from app.services.rag.summarizer import build_extractive_summary
from app.services.nlp.keyphrase_extractor import extract_keyphrases
from app.services.nlp.context_builder import build_focused_context


def run_rag_pipeline(text: str, query: str, k: int = 3):
    """
    End-to-end temporary RAG pipeline:
    1. Clean text
    2. Chunk text
    3. Embed chunks
    4. Create FAISS index
    5. Retrieve top-k relevant chunks
    """
    cleaned_text = clean_pdf_text(text)
    chunks = chunk_text(cleaned_text)

    if not chunks:
        return {
            "chunks_created": 0,
            "retrieved_chunks": []
        }

    embeddings = embed_texts(chunks)
    index = create_faiss_index(embeddings)
    retrieved = retrieve_top_k_chunks(query, index, chunks, k=k)

    return {
        "chunks_created": len(chunks),
        "chunks": chunks,
        "retrieved_chunks": retrieved
    }


def run_summary_pipeline(text: str):
    """
    Lightweight summarization pipeline:
    - Clean text
    - Chunk document
    - Retrieve summary-relevant chunks
    - Build extractive summary
    """
    cleaned_text = clean_pdf_text(text)
    chunks = chunk_text(cleaned_text)

    if not chunks:
        return {
            "chunks_created": 0,
            "summary": "",
            "retrieved_chunks": []
        }

    embeddings = embed_texts(chunks)
    index = create_faiss_index(embeddings)

    summary_query = "main objective key findings conclusion summary of the document"

    retrieved = retrieve_top_k_chunks(summary_query, index, chunks, k=3)

    summary = build_extractive_summary(
        chunks=chunks,
        retrieved_chunks=retrieved,
        max_summary_chars=1800
    )

    return {
        "chunks_created": len(chunks),
        "summary": summary,
        "retrieved_chunks": retrieved
    }


def run_focused_context_pipeline(text: str, query: str):
    """
    Query-focused content selection pipeline:
    - Clean text
    - Chunk document
    - Extract document keyphrases
    - Retrieve semantically relevant chunks
    - Build focused context for downstream LLM usage
    """
    cleaned_text = clean_pdf_text(text)
    chunks = chunk_text(cleaned_text)

    if not chunks:
        return {
            "chunks_created": 0,
            "keyphrases": [],
            "retrieved_chunks": [],
            "focused_context": ""
        }

    # Use cleaned text for keyphrase extraction
    keyphrase_source = cleaned_text[:5000]
    keyphrases = extract_keyphrases(keyphrase_source, top_n=10)

    embeddings = embed_texts(chunks)
    index = create_faiss_index(embeddings)

    retrieved = retrieve_top_k_chunks(query, index, chunks, k=4)

    focused_context = build_focused_context(
        query=query,
        keyphrases=keyphrases,
        retrieved_chunks=retrieved,
        max_context_chars=2500
    )

    return {
        "chunks_created": len(chunks),
        "keyphrases": keyphrases,
        "retrieved_chunks": retrieved,
        "focused_context": focused_context
    }