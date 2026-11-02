import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    cleaned = df.drop_duplicates()

    logger.debug(
        "remove_duplicates: removed %s rows",
        len(df) - len(cleaned)
    )
    return cleaned


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        cleaned = df.dropna(axis=0)
        removed = len(df) - len(cleaned)

    elif axis == "columns":
        cleaned = df.dropna(axis=1)
        removed = len(df.columns) - len(cleaned.columns)

    else:
        logger.error("Unsupported missing-value axis: %s", axis)
        raise ValueError(f"Unsupported missing-value axis: {axis}")

    logger.debug("handle_missing: removed %s %s", removed, axis)
    return cleaned


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ("iqr", "zscore"):
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError(f"Unsupported outlier method: {method}")

    cleaned = df.copy()

    for column in columns:
        if column not in cleaned.columns:
            logger.warning("Column not found: %s", column)
            continue

        if not pd.api.types.is_numeric_dtype(cleaned[column]):
            logger.warning("Column is not numeric: %s", column)
            continue

        values = cleaned[column]
        rows_before = len(cleaned)

        if method == "iqr":
            q1 = values.quantile(0.25)
            q3 = values.quantile(0.75)
            iqr = q3 - q1

            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr

            outliers = (values < lower) | (values > upper)

        else:
            mean = values.mean()
            std = values.std(ddof=0)

            if pd.isna(std) or std == 0:
                logger.debug(
                    "%s: method=%s threshold=%s removed=0 "
                    "(no variation or no numeric values)",
                    column, method, threshold
                )
                continue

            z_scores = (values - mean) / std
            outliers = z_scores.abs() > threshold

        cleaned = cleaned.loc[~outliers]

        logger.debug(
            "%s: method=%s threshold=%s removed=%s",
            column, method, threshold,
            rows_before - len(cleaned)
        )

    return cleaned


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    settings = config["processing"]
    cleaned = df.copy()

    if settings["remove_duplicates"]:
        cleaned = remove_duplicates(cleaned)

    missing = settings["missing"]
    if missing["enabled"]:
        cleaned = handle_missing(cleaned, axis=missing["axis"])

    outliers = settings["outliers"]
    if outliers["enabled"]:
        cleaned = remove_outliers(
            cleaned,
            columns=outliers["columns"],
            method=outliers["method"],
            threshold=outliers["threshold"]
        )

    return cleaned


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": (
            len(df_before.columns) - len(df_after.columns)
        )
    }