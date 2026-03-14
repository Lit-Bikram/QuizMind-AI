from fastapi import APIRouter, UploadFile, File, HTTPException, Form  # type: ignore
from app.utils.file_utils import save_uploaded_file
from app.services.ingestion.file_parser import parse_uploaded_file
from app.services.rag.rag_pipeline import (
    run_rag_pipeline,
    run_summary_pipeline,
    run_focused_context_pipeline
)
from app.services.mcq.generator import generate_mcqs
from app.schemas.mcq import MCQGenerationResponse

router = APIRouter()


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported right now."
            )

        saved_path = save_uploaded_file(file)
        parsed_result = parse_uploaded_file(saved_path)

        extracted_text = parsed_result["text"]
        num_pages = parsed_result["num_pages"]

        return {
            "message": "File uploaded and parsed successfully",
            "original_filename": file.filename,
            "saved_path": saved_path,
            "num_pages": num_pages,
            "text_length": len(extracted_text),
            "text_preview": extracted_text[:1000]
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document: {str(e)}"
        )


@router.post("/upload-and-query")
async def upload_and_query_document(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported right now."
            )

        saved_path = save_uploaded_file(file)
        parsed_result = parse_uploaded_file(saved_path)

        extracted_text = parsed_result["text"]
        num_pages = parsed_result["num_pages"]

        rag_result = run_rag_pipeline(extracted_text, query=query, k=3)

        return {
            "message": "File uploaded, parsed, and queried successfully",
            "original_filename": file.filename,
            "saved_path": saved_path,
            "num_pages": num_pages,
            "text_length": len(extracted_text),
            "query": query,
            "chunks_created": rag_result["chunks_created"],
            "retrieved_chunks": rag_result["retrieved_chunks"]
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process document and query: {str(e)}"
        )


@router.post("/upload-and-summarize")
async def upload_and_summarize_document(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported right now."
            )

        saved_path = save_uploaded_file(file)
        parsed_result = parse_uploaded_file(saved_path)

        extracted_text = parsed_result["text"]
        num_pages = parsed_result["num_pages"]

        summary_result = run_summary_pipeline(extracted_text)

        return {
            "message": "File uploaded, parsed, and summarized successfully",
            "original_filename": file.filename,
            "saved_path": saved_path,
            "num_pages": num_pages,
            "text_length": len(extracted_text),
            "chunks_created": summary_result["chunks_created"],
            "summary": summary_result["summary"],
            "supporting_chunks": summary_result["retrieved_chunks"]
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to summarize document: {str(e)}"
        )


@router.post("/upload-and-focus")
async def upload_and_focus_document(
    file: UploadFile = File(...),
    query: str = Form(...)
):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported right now."
            )

        saved_path = save_uploaded_file(file)
        parsed_result = parse_uploaded_file(saved_path)

        extracted_text = parsed_result["text"]
        num_pages = parsed_result["num_pages"]

        focus_result = run_focused_context_pipeline(
            text=extracted_text,
            query=query
        )

        return {
            "message": "File uploaded, parsed, and focused successfully",
            "original_filename": file.filename,
            "saved_path": saved_path,
            "num_pages": num_pages,
            "text_length": len(extracted_text),
            "query": query,
            "chunks_created": focus_result["chunks_created"],
            "keyphrases": focus_result["keyphrases"],
            "retrieved_chunks": focus_result["retrieved_chunks"],
            "focused_context": focus_result["focused_context"]
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to build focused context: {str(e)}"
        )


@router.post("/upload-and-generate-mcqs", response_model=MCQGenerationResponse)
async def upload_and_generate_mcqs(
    file: UploadFile = File(...),
    query: str = Form(...),
    num_questions: int = Form(5)
):
    try:
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported right now."
            )

        if num_questions < 1 or num_questions > 10:
            raise HTTPException(
                status_code=400,
                detail="num_questions must be between 1 and 10."
            )

        saved_path = save_uploaded_file(file)
        parsed_result = parse_uploaded_file(saved_path)

        extracted_text = parsed_result["text"]
        num_pages = parsed_result["num_pages"]

        focus_result = run_focused_context_pipeline(
            text=extracted_text,
            query=query
        )

        mcqs = generate_mcqs(
            query=query,
            focused_context=focus_result["focused_context"],
            num_questions=num_questions
        )

        return {
            "message": "File uploaded, parsed, focused, and MCQs generated successfully",
            "original_filename": file.filename,
            "saved_path": saved_path,
            "num_pages": num_pages,
            "text_length": len(extracted_text),
            "query": query,
            "chunks_created": focus_result["chunks_created"],
            "keyphrases": focus_result["keyphrases"],
            "focused_context": focus_result["focused_context"],
            "mcqs": mcqs
        }

    except HTTPException as http_exc:
        raise http_exc

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate MCQs: {str(e)}"
        )
