from pydantic import BaseModel


class ResetRunRequest(BaseModel):
    """ Challenge request to restart its active run. """
    challenge_id: int
