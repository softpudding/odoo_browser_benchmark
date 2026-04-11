"""Database snapshot and restore helpers for benchmark episodes.

Provides PostgreSQL-based snapshot management so each benchmark episode
starts from a known clean state. Uses pg_dump/pg_restore for portability.

Usage::

    from benchmark.db import DatabaseManager

    db = DatabaseManager(db_user="yangxiao")

    # Create a snapshot from a running database
    db.create_snapshot("odoo_dev", "website_hr_recruitment_base")

    # Restore before each benchmark episode
    db.restore_snapshot("website_hr_recruitment_base", "benchmark_episode_1")

    # Clean up
    db.drop_database("benchmark_episode_1")
"""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any


class DatabaseManager:
    """Manages PostgreSQL database snapshots for benchmark isolation."""

    def __init__(
        self,
        db_user: str | None = None,
        db_host: str | None = None,
        db_port: int | None = None,
        snapshot_dir: str | None = None,
    ) -> None:
        self.db_user = db_user or os.getenv("PGUSER", os.getenv("USER", "odoo"))
        self.db_host = db_host or os.getenv("PGHOST")
        self.db_port = db_port or int(os.getenv("PGPORT", "5432"))
        self.snapshot_dir = Path(
            snapshot_dir or os.getenv("BENCHMARK_SNAPSHOT_DIR", "/tmp/benchmark_snapshots")
        )
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)

    def _pg_env(self) -> dict[str, str]:
        """Build environment for pg_* commands."""
        env = dict(os.environ)
        if self.db_user:
            env["PGUSER"] = self.db_user
        if self.db_host:
            env["PGHOST"] = self.db_host
        if self.db_port:
            env["PGPORT"] = str(self.db_port)
        return env

    def _run(self, cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess:
        return subprocess.run(
            cmd, env=self._pg_env(), capture_output=True, text=True, **kwargs,
        )

    def database_exists(self, db_name: str) -> bool:
        result = self._run([
            "psql", "-tAc",
            f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'",
            "postgres",
        ])
        return result.stdout.strip() == "1"

    def create_snapshot(self, source_db: str, snapshot_name: str) -> Path:
        """Dump a database to a snapshot file.

        Args:
            source_db: Name of the source database to dump.
            snapshot_name: Logical name for the snapshot.

        Returns:
            Path to the snapshot file.
        """
        snapshot_path = self.snapshot_dir / f"{snapshot_name}.dump"
        result = self._run([
            "pg_dump", "-Fc", "-f", str(snapshot_path), source_db,
        ])
        if result.returncode != 0:
            raise RuntimeError(f"pg_dump failed: {result.stderr}")
        return snapshot_path

    def restore_snapshot(self, snapshot_name: str, target_db: str) -> str:
        """Restore a snapshot into a fresh database.

        Drops the target database if it exists, creates a new one,
        and restores the snapshot into it.

        Args:
            snapshot_name: Logical name of the snapshot to restore.
            target_db: Name for the restored database.

        Returns:
            The target database name.
        """
        snapshot_path = self.snapshot_dir / f"{snapshot_name}.dump"
        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot not found: {snapshot_path}")

        # Drop target if exists
        if self.database_exists(target_db):
            self.drop_database(target_db)

        # Create empty database
        result = self._run(["createdb", target_db])
        if result.returncode != 0:
            raise RuntimeError(f"createdb failed: {result.stderr}")

        # Restore
        result = self._run([
            "pg_restore", "--no-owner", "--no-acl", "-d", target_db,
            str(snapshot_path),
        ])
        # pg_restore returns non-zero on warnings too, so only fail on
        # actual errors (check stderr for FATAL/ERROR)
        if result.returncode != 0 and "FATAL" in result.stderr:
            raise RuntimeError(f"pg_restore failed: {result.stderr}")

        return target_db

    def clone_database(self, source_db: str, target_db: str) -> str:
        """Clone a database using CREATE DATABASE ... TEMPLATE.

        Faster than dump/restore for local use. Requires no active
        connections to the source database.

        Args:
            source_db: Name of the source database.
            target_db: Name for the clone.

        Returns:
            The target database name.
        """
        if self.database_exists(target_db):
            self.drop_database(target_db)

        # Terminate connections to source
        self._run([
            "psql", "-c",
            f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
            f"WHERE datname = '{source_db}' AND pid != pg_backend_pid()",
            "postgres",
        ])

        result = self._run([
            "createdb", "-T", source_db, target_db,
        ])
        if result.returncode != 0:
            raise RuntimeError(f"createdb -T failed: {result.stderr}")
        return target_db

    def drop_database(self, db_name: str) -> None:
        """Drop a database if it exists."""
        # Terminate connections first
        self._run([
            "psql", "-c",
            f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
            f"WHERE datname = '{db_name}' AND pid != pg_backend_pid()",
            "postgres",
        ])
        result = self._run(["dropdb", "--if-exists", db_name])
        if result.returncode != 0:
            raise RuntimeError(f"dropdb failed: {result.stderr}")

    def list_snapshots(self) -> list[str]:
        """List available snapshot names."""
        return [
            p.stem for p in self.snapshot_dir.glob("*.dump")
        ]
