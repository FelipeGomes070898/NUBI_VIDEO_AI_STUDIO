from pathlib import Path
import os
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = Path(os.getenv("NUBI_DATA_DIR", ROOT / "storage")).expanduser().resolve()
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = Path(os.getenv("NUBI_DB_PATH", DATA_DIR / "nubi.sqlite3")).expanduser()
OUTPUT_DIR = Path(os.getenv("NUBI_OUTPUT_DIR", DATA_DIR / "outputs")).expanduser()
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
HOST = os.getenv("NUBI_HOST", "127.0.0.1")
PORT = int(os.getenv("NUBI_PORT", "8000"))
