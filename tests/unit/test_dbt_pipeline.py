"""Tests for dbt warehouse pipeline execution."""

from pathlib import Path
from subprocess import CompletedProcess
from unittest.mock import patch

from alpha60.pipelines.dbt_pipeline import (
    DbtBuildStatus,
    run_dbt_build,
)


def test_run_dbt_build_executes_project() -> None:
    """The dbt pipeline runs dbt build against the configured project."""
    project_dir = Path("/app/dbt/alpha60")

    with patch(
        "alpha60.pipelines.dbt_pipeline.subprocess.run"
    ) as run_command:
        run_command.return_value = CompletedProcess(
            args=[],
            returncode=0,
            stdout="Completed successfully",
            stderr="",
        )

        result = run_dbt_build(project_dir=project_dir)

    assert result.status == DbtBuildStatus.SUCCESS
    assert result.return_code == 0
    assert result.stdout == "Completed successfully"
    assert result.stderr == ""

    run_command.assert_called_once_with(
        [
            "dbt",
            "build",
            "--project-dir",
            str(project_dir),
            "--profiles-dir",
            str(project_dir),
        ],
        check=False,
        capture_output=True,
        text=True,
    )


def test_run_dbt_build_reports_failure() -> None:
    """The dbt pipeline returns a failed result when dbt exits non-zero."""
    project_dir = Path("/app/dbt/alpha60")

    with patch(
        "alpha60.pipelines.dbt_pipeline.subprocess.run"
    ) as run_command:
        run_command.return_value = CompletedProcess(
            args=[],
            returncode=1,
            stdout="",
            stderr="dbt build failed",
        )

        result = run_dbt_build(project_dir=project_dir)

    assert result.status == DbtBuildStatus.FAILED
    assert result.return_code == 1
    assert result.stdout == ""
    assert result.stderr == "dbt build failed"


def test_run_dbt_build_passes_selected_models() -> None:
    """The dbt pipeline can build only selected models."""
    project_dir = Path("/app/dbt/alpha60")

    with patch(
        "alpha60.pipelines.dbt_pipeline.subprocess.run"
    ) as run_command:
        run_command.return_value = CompletedProcess(
            args=[],
            returncode=0,
            stdout="Completed successfully",
            stderr="",
        )

        result = run_dbt_build(
            project_dir=project_dir,
            select=[
                "fact_inventory_snapshot",
                "store_rotation_workbench",
            ],
        )

    assert result.status == DbtBuildStatus.SUCCESS

    run_command.assert_called_once_with(
        [
            "dbt",
            "build",
            "--project-dir",
            str(project_dir),
            "--profiles-dir",
            str(project_dir),
            "--select",
            "fact_inventory_snapshot",
            "store_rotation_workbench",
        ],
        check=False,
        capture_output=True,
        text=True,
    )
