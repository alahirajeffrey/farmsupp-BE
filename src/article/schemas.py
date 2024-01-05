from datetime import datetime
from pydantic import BaseModel, UUID4
from typing import Optional

class CreateArticleSchema(BaseModel):
    body: str
    title: str

class ArticleReturnSchema(CreateArticleSchema):
    created_at: datetime
    updated_at: datetime
    id: UUID4

class ArticleUpdateSchema(BaseModel):
    title: Optional[str] = None
    body: Optional[str] = None