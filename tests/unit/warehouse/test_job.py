"""Tests for warehouse load jobs."""

from alpha60.warehouse.job import WarehouseJobStatus, WarehouseLoadJob


def test_warehouse_load_job_defaults() -> None:
    """A warehouse load job has sensible defaults."""
    job = WarehouseLoadJob(
        job_id="job-123",
        table_id="products",
        status=WarehouseJobStatus.PENDING,
    )

    assert job.job_id == "job-123"
    assert job.table_id == "products"
    assert job.status == WarehouseJobStatus.PENDING
    assert job.rows_loaded == 0
    assert job.error_message is None