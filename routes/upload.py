from fastapi import APIRouter, UploadFile, File, HTTPException

from services.knowledgeService import KnowledgeService


router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Base"]
)

knowledge_service = KnowledgeService()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    file_path = f"temp_{file.filename}"

    try:
        contents = await file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

        result = knowledge_service.ingest(file_path)

        return {
            "message": "Document ingested successfully.",
            **result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )