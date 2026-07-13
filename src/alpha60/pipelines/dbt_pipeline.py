"""dbt warehouse pipeline execution."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
import subprocess


class DbtBuildStatus(StrEnum):
    """Status of a dbt build."""

    SUCCESS = "success"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class DbtBuildResult:
    """Result returned by a dbt build."""

    status: DbtBuildStatus
    return_code: int
    stdout: str
    stderr: str


def run_dbt_build(
    *,
    project_dir: Path,
    select: list[str] | None = None,
) -> DbtBuildResult:
    """Run dbt build for the configured dbt project."""
    command = [
        "dbt",
        "build",
        "--project-dir",
        str(project_dir),
        "--profiles-dir",
        str(project_dir),
    ]

    if select:
        command.extend(["--select", *select])

    completed_process = subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
    )

    status = (
        DbtBuildStatus.SUCCESS
        if completed_process.returncode == 0
        else DbtBuildStatus.FAILED
    )

    return DbtBuildResult(
        status=status,
        return_code=completed_process.returncode,
        stdout=completed_process.stdout,
        stderr=completed_process.stderr,
    )
