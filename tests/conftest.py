import sqlite3

import duckdb
import pytest

from database_exporter.exporter import DatabaseConnection


@pytest.fixture
def sqlite_connection() -> DatabaseConnection:
    yield sqlite3.connect(":memory:")


@pytest.fixture
def duckdb_connection() -> DatabaseConnection:
    yield duckdb.connect(":memory:")
