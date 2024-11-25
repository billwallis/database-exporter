"""
End-to-end tests for the package.
"""

import pathlib
import re
from typing import Callable

import pytest

import database_exporter
from database_exporter.exporter import DatabaseConnection

FIXTURES = pathlib.Path(__file__).parent / "fixtures"


@pytest.fixture
def simple_query__sql() -> str:
    return (FIXTURES / "simple_query.sql").read_text().strip()


@pytest.fixture
def simple_query__csv() -> str:
    return (FIXTURES / "simple_query.csv").read_text().strip()


@pytest.fixture
def complex_query__sql() -> str:
    return (FIXTURES / "complex_query.sql").read_text().strip()


@pytest.fixture
def complex_query__csv() -> str:
    return (FIXTURES / "complex_query.csv").read_text().strip()

@pytest.mark.parametrize(
    "query, result, exporter",
    [
        ("simple_query__sql", "simple_query__csv", database_exporter.query_to_csv),
    ],
)
def test__sqlite_result_sets_can_be_exported_to_a_file(
    sqlite_connection: DatabaseConnection,
    tmp_path: pathlib.Path,
    request: pytest.FixtureRequest,
    query: str,
    result: str,
    exporter: Callable,
) -> None:
    """
    The result set from a SQLite query can be exported to a file.
    """
    actual_path = tmp_path / "actual.csv"
    exporter(
        conn=sqlite_connection,
        query=request.getfixturevalue(query),
        filepath=actual_path,
    )

    assert actual_path.exists()
    actual = actual_path.read_text().strip()

    # The sqlite3 driver returns ints instead of bools
    # fmt: off
    result = (
        request.getfixturevalue(result)
            .replace("true", "1")
            .replace("false", "0")
    )
    # fmt: on

    # In CI, the drivers print extra line breaks to the CSV for some reason :shrug:
    actual = re.sub(r"\n+", "\n", actual)

    assert actual == result


@pytest.mark.parametrize(
    "query, result, exporter",
    [
        ("simple_query__sql", "simple_query__csv", database_exporter.query_to_csv),
        ("complex_query__sql", "complex_query__csv", database_exporter.query_to_csv),
    ],
)
def test__duckdb_result_sets_can_be_exported_to_a_file(
    duckdb_connection: DatabaseConnection,
    tmp_path: pathlib.Path,
    request: pytest.FixtureRequest,
    query: str,
    result: str,
    exporter: Callable,
) -> None:
    """
    The result set from a DuckDB query can be exported to a file.
    """
    actual_path = tmp_path / "actual.csv"
    exporter(
        conn=duckdb_connection,
        query=request.getfixturevalue(query),
        filepath=actual_path,
    )

    assert actual_path.exists()
    actual = actual_path.read_text().strip()

    # In CI, the drivers print extra line breaks to the CSV for some reason :shrug:
    actual = re.sub(r"\n+", "\n", actual)

    assert actual == request.getfixturevalue(result)
