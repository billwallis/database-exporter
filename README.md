<span align="center">

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![tests](https://github.com/billwallis/database-exporter/actions/workflows/tests.yaml/badge.svg)](https://github.com/billwallis/database-exporter/actions/workflows/tests.yaml)
[![coverage](https://raw.githubusercontent.com/billwallis/database-exporter/refs/heads/main/coverage.svg)](https://smarie.github.io/python-genbadge/)

[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/billwallis/database-exporter/main.svg)](https://results.pre-commit.ci/latest/github/billwallis/database-exporter/main)
[![GitHub last commit](https://img.shields.io/github/last-commit/billwallis/database-exporter)](https://shields.io/badges/git-hub-last-commit)

</span>

---

> [!WARNING]
>
> The functionality in this project is still inefficient and limited.

# Database Exporter 📦📤

Export database query result sets.

This tool is database-agnostic -- just provide a class that connects to your database with an execute method, and the query whose result set you want to export.

## Installation ⬇️

While in preview, this package is only available from GitHub:

```
pip install git+https://github.com/billwallis/database-exporter@v0.0.2
```

This will be made available on PyPI once it's ready for general use.

## Usage 📖

The package exposes functions which require a database connection/cursor class that implements an `execute` method.

### SQLite Example

> Official documentation: https://docs.python.org/3/library/sqlite3.html

```python
import pathlib
import sqlite3

import database_exporter


def main() -> None:
    db_conn = sqlite3.connect(":memory:")  # Or a path to a database file
    query_path = pathlib.Path("path/to/query.sql")
    database_exporter.query_to_csv(
        conn=db_conn,
        query=query_path.read_text("utf-8"),
        filepath=query_path.with_suffix(".csv"),
    )


if __name__ == "__main__":
    main()
```

### Snowflake Example

> Official documentation: https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-example

```python
import pathlib

import database_exporter
import snowflake.connector  # snowflake-connector-python


# This dictionary is just for illustration purposes, and
# you should use whatever connection method you prefer
CREDENTIALS = {
    "user": "XXX",
    "password": "XXX",
    "account": "XXX",
    "warehouse": "XXX",
    "role": "XXX",
    "database": "XXX",
}


def main() -> None:
    db_conn = snowflake.connector.SnowflakeConnection(**CREDENTIALS)
    query_path = pathlib.Path("path/to/query.sql")
    with db_conn.cursor() as cursor:
        database_exporter.query_to_csv(
            conn=cursor,
            query=query_path.read_text("utf-8"),
            filepath=query_path.with_suffix(".csv"),
        )
    db_conn.close()


if __name__ == "__main__":
    main()
```

## Contributing

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) and then install the dependencies:

```shell
uvx --from poethepoet poe install
```
