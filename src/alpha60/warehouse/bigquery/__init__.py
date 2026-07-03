"""BigQuery warehouse integration for ALPHA60.

This package contains BigQuery-specific loading, schema, and client utilities.

The BigQuery integration must remain connector-agnostic. It should operate on
core Record objects rather than source-specific payloads.
"""