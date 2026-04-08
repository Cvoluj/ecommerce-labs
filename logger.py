import logging
import sys
from pythonjsonlogger.json import JsonFormatter


def _setup() -> None:
    formatter = JsonFormatter(
        fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%SZ",
        rename_fields={"asctime": "timestamp", "levelname": "level", "name": "logger"},
    )

    file_handler = logging.FileHandler("app.log")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.addHandler(file_handler)
    root.addHandler(stream_handler)

    for name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
        uv = logging.getLogger(name)
        uv.handlers = []
        uv.propagate = True
_setup()

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
