"""Define API response models."""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Describe the application status."""

    status: str
    version: str


class DatasetInfo(BaseModel):
    """Describe a stored dataset."""

    id: int
    filename: str
    rows: int
    columns: int
    column_names: list[str]