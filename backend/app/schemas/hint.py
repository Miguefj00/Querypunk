from pydantic import BaseModel


class HintCreate(BaseModel):
    """ Payload to create a hint. """
    order_index: int
    content: str
    unlock_after_attempts: int | None = None


class HintUpdate(BaseModel):
    """ Payload to update a hint. """
    order_index: int | None = None
    content: str | None = None
    unlock_after_attempts: int | None = None


class HintResponse(BaseModel):
    """ Hint data returned by the API. """
    id: int
    order_index: int
    content: str
    unlock_after_attempts: int | None
