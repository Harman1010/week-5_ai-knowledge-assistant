from pydantic import BaseModel,Field

class AskRequest(BaseModel):

    query : str = Field(...,min_length=1)