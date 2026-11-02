"""Validate required columns and numeric values."""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def validate_dataframe(df, required_columns, numeric_columns):
    """Check required columns and remove invalid numeric values."""
    validated = df.copy()
    rows_before = len(validated)

    for column in required_columns:
        if column not in validated.columns:
            logger.error("Required column missing: %s", column)
            raise ValueError(f"Required column missing: {column}")

    for column in numeric_columns:
        if column not in validated.columns:
            logger.error("Numeric column missing: %s", column)
            raise ValueError(f"Numeric column missing: {column}")

        invalid_rows = []

        for index, value in validated[column].items():
            if pd.notna(value):
                try:
                    float(value)
                except (ValueError, TypeError):
                    logger.warning(
                        "Invalid numeric value in %s at row %s: %r",
                        column,
                        index,
                        value,
                    )
                    invalid_rows.append(index)

        validated = validated.drop(index=invalid_rows)
        validated[column] = pd.to_numeric(validated[column])

    logger.debug(
        "Validation: %s -> %s rows; removed %s rows",
        rows_before,
        len(validated),
        rows_before - len(validated),
    )

    return validated