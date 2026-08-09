from fastapi import APIRouter, HTTPException

from schemas.request import AskRequest
from schemas.response import AskResponse
from routes.upload import knowledge_service


router = APIRouter(
    prefix="/ask",
    tags=["Knowledge Base"]
)


@router.post("", response_model=AskResponse)
def ask_question(request: AskRequest):

    try:
        result = knowledge_service.ask(request.query)
        return result

    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))