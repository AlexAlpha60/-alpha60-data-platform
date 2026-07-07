"""Generic SQL transformation runner."""

from pathlib import Path
from typing import Protocol

from alpha60.transformations.result import TransformationResult, TransformationStatus


class QueryClient(Protocol):
    """Client capable of running SQL queries."""

    def query(self, sql: str) -> list[dict[str, object]]:
        """Run a SQL query and return rows as dictionaries."""


class SqlTransformationRunner:
    """Run a SQL transformation file with template variables."""

    def __init__(
        self,
        client: QueryClient,
        sql_path: Path,
        target_table_id: str,
        template_variables: dict[str, str],
    ) -> None:
        """Create a SQL transformation runner."""
        self._client = client
        self._sql_path = sql_path
        self._target_table_id = target_table_id
        self._template_variables = template_variables

    def run(self) -> TransformationResult:
        """Run the SQL transformation."""
        try:
            self._client.query(self._render_sql())
        except Exception as exc:
            return TransformationResult(
                target_table_id=self._target_table_id,
                status=TransformationStatus.FAILED,
                error_message=str(exc),
            )

        return TransformationResult(
            target_table_id=self._target_table_id,
            status=TransformationStatus.SUCCESS,
        )

    def _render_sql(self) -> str:
        """Render the SQL file with template variables."""
        template = self._sql_path.read_text(encoding="utf-8")
        return template.format(**self._template_variables)
