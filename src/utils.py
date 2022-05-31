"""Utils"""
import os
import pathlib
import sqlite3

from loguru import logger

log_dir = pathlib.Path.home()
log_dir.joinpath("logs").mkdir(parents=True, exist_ok=True)
log_dir.joinpath("db").mkdir(parents=True, exist_ok=True)


logger.add(
    log_dir.joinpath("logs").joinpath("wg-statistics.log"),
    format="{time} [{level}] {module} {name} {function} - {message}",
    level="DEBUG",
    compression="zip",
    rotation="30 MB",
)

conn = sqlite3.connect(os.path.join(log_dir.joinpath("db"), "wg-stats.db"))
cursor = conn.cursor()


def _init_db():
    """Инициализирует БД"""
    init_path = pathlib.Path(__file__).resolve().parent.parent.joinpath("sql/stats.sql")
    with open(init_path, "r", encoding='utf-8') as file:
        init_src = file.read()
    cursor.executescript(init_src)
    conn.commit()


def check_db_exists():
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT count(*) FROM sqlite_master WHERE name in ('stats', 'wg0_users', 'user_map', 'v_stats')")
    table_exists = cursor.fetchall()[0][0]
    if table_exists >= 4:
        return
    _init_db()


def insert(table: str, column_values: dict):
    """insert Dict to sqlite3 tables"""
    columns = ", ".join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ", ".join("?" * len(column_values.keys()))
    cursor.executemany(f"INSERT INTO {table} " f"({columns}) " f"VALUES ({placeholders})", values)
    conn.commit()


check_db_exists()
