from pydantic import BaseModel


class HintCreate(BaseModel):
    order_index: int
    content: str
    unlock_after_attempts: int | None = None


class HintUpdate(BaseModel):
    order_index: int | None = None
    content: str | None = None
    unlock_after_attempts: int | None = None


class HintResponse(BaseModel):
    id: int
    order_index: int
    content: str
    unlock_after_attempts: int | None
