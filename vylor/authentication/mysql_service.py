from __future__ import annotations

import os
from threading import Lock

from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker


class MySQLService:
    _instance: "MySQLService" | None = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self) -> None:
        self.db_name = os.getenv("MYSQL_DB")
        self.db_user = os.getenv("MYSQL_USER")
        self.db_password = os.getenv("MYSQL_PASSWORD")
        self.db_host = os.getenv("MYSQL_HOST", "127.0.0.1")
        self.db_port = os.getenv("MYSQL_PORT", "3306")

        missing = [
            name
            for name, value in (
                ("MYSQL_DB", self.db_name),
                ("MYSQL_USER", self.db_user),
                ("MYSQL_PASSWORD", self.db_password),
            )
            if not value
        ]
        if missing:
            raise EnvironmentError(
                f"Missing MySQL configuration for {', '.join(missing)}."
            )

        self.connection_string = self._create_connection_string()
        self.engine = create_engine(
            self.connection_string, pool_pre_ping=True, future=True
        )
        self.Session = sessionmaker(bind=self.engine, future=True)

        self._test_connection()
        self._ensure_users_table()

    def _create_connection_string(self) -> str:
        return (
            f"mysql+pymysql://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    def _test_connection(self) -> None:
        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
        except OperationalError as exc:
            print(f"❌ Failed to connect to MySQL: {exc}")
            raise SystemExit("Unable to connect to MySQL during startup.")

    def _ensure_users_table(self) -> None:
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
        with self.engine.begin() as connection:
            connection.execute(text(create_table_sql))

    def get_session(self) -> Session:
        return self.Session()