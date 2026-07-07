"""Tests for the generic SQL transformation runner."""

from pathlib import Path
from unittest.mock import Mock

from alpha60.transformations.result import TransformationStatus
from alpha60.transformations.runner import SqlTransformationRunner


def test_sql_transformation_runner_renders_and_runs_sql(tmp_path: Path) -> None:
    """The runner renders a SQL file and executes it."""
    sql_path = tmp_path / "model.sql"
    sql_path.write_text(
        "CREATE OR REPLACE TABLE `{project_id}.{dataset_id}.table` AS SELECT 1;",
        encoding="utf-8",
    )
    client = Mock()

    runner = SqlTransformationRunner(
        client=client,
        sql_path=sql_path,
        target_table_id="alpha60-data-platform.stg.table",
        template_variables={
            "project_id": "alpha60-data-platform",
            "dataset_id": "stg",
        },
    )

    result = runner.run()

    assert result.status == TransformationStatus.SUCCESS
    assert result.target_table_id == "alpha60-data-platform.stg.table"

    client.query.assert_called_once_with(
        "CREATE OR REPLACE TABLE `alpha60-data-platform.stg.table` AS SELECT 1;"
    )


def test_sql_transformation_runner_returns_failed_result(tmp_path: Path) -> None:
    """Query failures are returned as failed transformation results."""
    sql_path = tmp_path / "model.sql"
    sql_path.write_text("SELECT 1;", encoding="utf-8")

    client = Mock()
    client.query.side_effect = RuntimeError("query failed")

    runner = SqlTransformationRunner(
        client=client,
        sql_path=sql_path,
        target_table_id="alpha60-data-platform.stg.table",
        template_variables={},
    )

    result = runner.run()

    assert result.status == TransformationStatus.FAILED
    assert result.target_table_id == "alpha60-data-platform.stg.table"
    assert result.error_message == "query failed"
