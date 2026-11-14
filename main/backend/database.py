import sqlite3, json
from contextlib import contextmanager
from .config import DB_PATH
SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY, email TEXT UNIQUE, name TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS projects(id TEXT PRIMARY KEY, title TEXT NOT NULL, topic TEXT DEFAULT '', language TEXT DEFAULT 'pt-BR', duration INTEGER DEFAULT 60, aspect_ratio TEXT DEFAULT '16:9', resolution TEXT DEFAULT '1280x720', fps INTEGER DEFAULT 24, style TEXT DEFAULT 'cinematic', status TEXT DEFAULT 'draft', created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS scenes(id TEXT PRIMARY KEY, project_id TEXT NOT NULL REFERENCES projects(id) ON DELETE CASCADE, position INTEGER NOT NULL, title TEXT, prompt TEXT, duration REAL DEFAULT 5, engine TEXT DEFAULT 'ltx', status TEXT DEFAULT 'planned', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS assets(id TEXT PRIMARY KEY, project_id TEXT REFERENCES projects(id) ON DELETE SET NULL, kind TEXT NOT NULL, path TEXT NOT NULL, metadata TEXT DEFAULT '{}', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS generation_jobs(id TEXT PRIMARY KEY, project_id TEXT REFERENCES projects(id) ON DELETE SET NULL, provider TEXT, model TEXT, prompt TEXT, status TEXT DEFAULT 'queued', external_id TEXT, result_path TEXT, cost REAL, error TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS render_jobs(id TEXT PRIMARY KEY, project_id TEXT REFERENCES projects(id) ON DELETE SET NULL, status TEXT DEFAULT 'queued', engine TEXT, output_path TEXT, progress REAL DEFAULT 0, error TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP, updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS engine_integrations(id TEXT PRIMARY KEY, name TEXT UNIQUE NOT NULL, kind TEXT, configured INTEGER DEFAULT 0, available INTEGER DEFAULT 0, details TEXT DEFAULT '{}', checked_at TEXT);
CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY, value TEXT NOT NULL, updated_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS logs(id INTEGER PRIMARY KEY AUTOINCREMENT, level TEXT, message TEXT, metadata TEXT DEFAULT '{}', created_at TEXT DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS usage_records(id INTEGER PRIMARY KEY AUTOINCREMENT, provider TEXT, model TEXT, units REAL DEFAULT 0, cost REAL, project_id TEXT, created_at TEXT DEFAULT CURRENT_TIMESTAMP);
"""
@contextmanager
def connect():
    con=sqlite3.connect(DB_PATH, timeout=30); con.row_factory=sqlite3.Row
    try:
        con.executescript(SCHEMA); yield con; con.commit()
    finally: con.close()
def init_db():
    with connect() as c: pass
