"""Define API request and response models."""

from pydantic import BaseModel, Field


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


class ValidationSettings(BaseModel):
    """Configure column validation."""

    required_columns: list[str] = Field(default_factory=list)
    numeric_columns: list[str] = Field(default_factory=list)


class MissingSettings(BaseModel):
    """Configure missing-value handling."""

    enabled: bool = True
    axis: str = "rows"


class OutlierSettings(BaseModel):
    """Configure outlier removal."""

    enabled: bool = False
    columns: list[str] = Field(default_factory=list)
    method: str = "iqr"
    threshold: float = 1.5


class ProcessingSettings(BaseModel):
    """Configure data cleaning."""

    remove_duplicates: bool = True
    missing: MissingSettings = Field(default_factory=MissingSettings)
    outliers: OutlierSettings = Field(default_factory=OutlierSettings)


class ProcessConfig(BaseModel):
    """Combine validation and processing settings."""

    validation: ValidationSettings = Field(
        default_factory=ValidationSettings
    )
    processing: ProcessingSettings = Field(
        default_factory=ProcessingSettings
    )


class ProcessingReport(BaseModel):
    """Describe validation and cleaning results."""

    id: int
    validation_rows_removed: int
    cleaning_report: dict[str, int]