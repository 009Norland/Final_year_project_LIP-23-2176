import logging, sys
from pathlib import Path
from config.settings import LOG_LEVEL, LOG_FILE
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

def get_logger(name):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(getattr(logging, LOG_LEVEL.upper(), logging.INFO))
    fmt = logging.Formatter("[%(asctime)s]  %(levelname)-8s  %(name)s — %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    ch = logging.StreamHandler(sys.stdout); ch.setFormatter(fmt); logger.addHandler(ch)
    fh = logging.FileHandler(LOG_FILE, encoding="utf-8"); fh.setFormatter(fmt); logger.addHandler(fh)
    return logger
