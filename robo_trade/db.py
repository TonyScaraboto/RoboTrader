from __future__ import annotations
import os
import psycopg2
import psycopg2.extras
import logging
from typing import Any, Dict, List, Optional, Tuple

# Simple PostgreSQL helper for operations storage


def _get_conn_params() -> Optional[dict]:
    url = os.getenv("DATABASE_URL")
    if url:
        return {"dsn": url, "sslmode": os.getenv("PGSSLMODE")}

    host = os.getenv("POSTGRES_HOST")
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD", "")  # Allow empty password
    port = os.getenv("POSTGRES_PORT", "5432")

    if not (host and dbname and user):
        return None

    return {
        "host": host,
        "dbname": dbname,
        "user": user,
        "password": password or None,  # Pass None if empty
        "port": int(port),
        "sslmode": os.getenv("PGSSLMODE", "prefer"),
    }


def get_connection():
    params = _get_conn_params()
    if not params:
        return None
    try:
        if "dsn" in params:
            conn = psycopg2.connect(params["dsn"], sslmode=params.get("sslmode") or "prefer")
        else:
            conn = psycopg2.connect(**{k: v for k, v in params.items() if v is not None})
        conn.autocommit = True
        return conn
    except Exception:
        return None


def ensure_schema() -> None:
    conn = get_connection()
    if not conn:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS operations (
                  id SERIAL PRIMARY KEY,
                  symbol TEXT,
                  timeframe TEXT,
                  mode TEXT,
                  entry_direction TEXT,
                  candle_direction TEXT,
                  stake_brl NUMERIC,
                  win BOOLEAN,
                  profit_brl NUMERIC,
                  created_at TIMESTAMPTZ DEFAULT NOW()
                );
                CREATE INDEX IF NOT EXISTS idx_operations_created_at ON operations(created_at);
                CREATE INDEX IF NOT EXISTS idx_operations_symbol ON operations(symbol);
                """
            )
        conn.close()
    except Exception as e:
        logging.warning(f"Could not ensure schema: {e}")


def insert_operation(row: Dict[str, Any]) -> bool:
    conn = get_connection()
    if not conn:
        return False
    columns = [
        "symbol",
        "timeframe",
        "mode",
        "entry_direction",
        "candle_direction",
        "stake_brl",
        "win",
        "profit_brl",
    ]
    values = [row.get(col) for col in columns]
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO operations (symbol, timeframe, mode, entry_direction, candle_direction, stake_brl, win, profit_brl)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """,
                values,
            )
        conn.close()
        return True
    except Exception:
        conn.close()
        return False


def fetch_operations(limit: int = 200) -> List[Dict[str, Any]]:
    conn = get_connection()
    if not conn:
        return []
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, symbol, timeframe, mode, entry_direction, candle_direction, stake_brl, win, profit_brl, created_at
                FROM operations
                ORDER BY created_at ASC
                LIMIT %s
                """,
                (limit,),
            )
            rows = cur.fetchall()
            return [dict(row) for row in rows]  # Convert RealDictRow to dict
    except Exception as e:
        logging.warning(f"Error fetching operations: {e}")
        return []
    finally:
        conn.close()


def fetch_summary() -> Tuple[int, int, float]:
    conn = get_connection()
    if not conn:
        return 0, 0, 0.0
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT 
                  COUNT(*) FILTER (WHERE win IS TRUE) AS wins,
                  COUNT(*) FILTER (WHERE win IS NOT TRUE) AS losses,
                  COALESCE(SUM(profit_brl), 0) AS total_profit
                FROM operations
                """
            )
            wins, losses, total_profit = cur.fetchone()
            return int(wins or 0), int(losses or 0), float(total_profit or 0.0)
    except Exception:
        return 0, 0, 0.0
    finally:
        conn.close()
