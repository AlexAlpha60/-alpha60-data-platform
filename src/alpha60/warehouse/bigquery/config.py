"""Configuration for the BigQuery warehouse."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BigQueryConfig:
    """Configuration required to load data into BigQuery."""

    project_id: str
    dataset_id: str
    location: str = "australia-southeast1"