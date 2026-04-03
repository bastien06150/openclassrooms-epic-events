from pathlib import Path

TOKEN_DIR = Path.home() / ".epic_events"
TOKEN_FILE = TOKEN_DIR / "token"


def save_token(token: str) -> None:
    TOKEN_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_FILE.write_text(token, encoding="utf-8")


def load_token() -> str | None:
    if not TOKEN_FILE.exists():
        return None
    return TOKEN_FILE.read_text(encoding="utf-8").strip()


def delete_token() -> None:
    if TOKEN_FILE.exists():
        TOKEN_FILE.unlink()
