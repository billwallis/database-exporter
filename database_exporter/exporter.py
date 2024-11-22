"""
A module for timing SQL queries.
"""

import csv
import json
import pathlib
from collections.abc import Iterable
from typing import Any, Protocol


class DatabaseCursor(Protocol):
    """
    Database cursor to fetch results.
    """

    description: list[str]

    def fetchall(self) -> list[tuple]:
        """
        Fetch all results.
        """


class DatabaseConnection(Protocol):
    """
    Database connector to run SQL against the database.
    """

    def execute(self, *args, **kwargs) -> DatabaseCursor:
        """
        Execute a statement.
        """


class Writer(Protocol):
    """
    Row-wise file writer.
    """

    def writerow(self, row: Iterable) -> None:
        """
        Write a row to the file.
        """


def _marshal(row: Iterable):
    """
    Convert dict and list values in a row to JSON.
    """

    def _to_json(value: Any):
        is_jsonable = isinstance(value, bool | dict | list)
        return json.dumps(value) if is_jsonable else value

    return tuple(_to_json(value) for value in row)


class CSVWriterWithJSONMarshalling:
    """
    Default Python CSV writer that marshals Python types into JSON.
    """

    def __init__(self, *args, **kwargs):
        self.writer = csv.writer(*args, **kwargs)

    def writerow(self, row: Iterable) -> None:
        self.writer.writerow(_marshal(row))


def _custom_writer(file: Any) -> Writer:
    return CSVWriterWithJSONMarshalling(
        file,
        delimiter=",",
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL,
    )


def _write_to_csv(
    result_set: list[tuple],
    headers: list[str],
    filepath: pathlib.Path,
    csv_writer: Writer = None,
) -> None:
    """
    Write the result set to a CSV.
    """

    filepath.parent.mkdir(parents=True, exist_ok=True)

    # Use a temporary file to avoid partial writes for atomicity
    temp_file = filepath.with_suffix(".tmp")
    with temp_file.open("w+") as f:
        csv_writer = csv_writer or _custom_writer(f)
        csv_writer.writerow(headers)
        for row in result_set:
            csv_writer.writerow(_marshal(row))

    temp_file.replace(filepath)


def query_to_csv(
    conn: DatabaseConnection,
    query: str,
    filepath: str | pathlib.Path,
    csv_writer: Writer = None,
) -> None:
    """
    Run the SQL query and save the result to a CSV.

    :param conn: The database connector. Must implement an ``execute``
        method.
    :param query: The SQL query to run.
    :param filepath: The path to save the CSV file.
    :param csv_writer: The writer to use. Defaults to a CSV writer that
        marshals JSON values.
    """
    results = conn.execute(query)
    result_set = results.fetchall()
    filepath = pathlib.Path(filepath)

    print(f"Writing {len(result_set):,} rows to '{filepath}'...")
    _write_to_csv(
        result_set=result_set,
        headers=[header[0] for header in results.description],
        filepath=filepath,
        csv_writer=csv_writer,
    )
