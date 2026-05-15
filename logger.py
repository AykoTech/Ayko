import logging
from pathlib import Path

def setup_logger(name):
    Path("logs").mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    h = logging.FileHandler(f"logs/{name}.log")
    h.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
    logger.addHandler(h)
    logger.addHandler(logging.StreamHandler())
    return logger
