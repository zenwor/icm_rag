import csv
import logging
import sys
from pathlib import Path

general_format = "%(levelname)s - %(filename)s (%(funcName)s): %(message)s"
logging.basicConfig(level=logging.INFO, format=general_format)

log_enabled = True


def set_log_enabled(flag: bool) -> None:
    """
    Enable / disable logging, based on flag.

    Args:
        flag (bool): Flag to set the logging to.

    Returns:
        None
    """
    global log_enabled
    log_enabled = flag


def set_log_file(log_file: str) -> None:
    """
    Set logging file.

    Args:
        log_file (str): Path to local logging file.

    Returns:
        None
    """
    if log_file is not None:
        logger = logging.getLogger()
        logger.handlers = []

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter(general_format))

        logger.addHandler(file_handler)


def log_info(msg) -> None:
    if log_enabled:
        logging.info(msg)


def log_warning(msg) -> None:
    if log_enabled:
        logging.warning(msg)


def log_error(msg) -> None:
    if log_enabled:
        logging.error(msg)
        sys.exit("")


def log_debug(msg) -> None:
    if log_enabled:
        logging.debug(msg)


def log_critical(msg) -> None:
    if log_enabled:
        logging.critical(msg)


def log_experiment(setup: dict, res: dict, log_path: Path) -> None:
    """
    Log experiments to the given local log file.

    args:
        setup (dict): General experimental setup. Contains information such as
            chunk size, chunk overlap, top-k etc.
        res (dict): Experiment results. Contains information such as recall
            and precision metrics.
        log_path (Path): Path to local log file.

    Returns:
        None
    """
    # Build the entry, in order
    entry = [
        setup["exp_name"],
        setup["chunker"],
        setup["chunk_size"],
        setup["chunk_overlap"],
        setup["ret_type"],
        setup["k"],
        res.get("recall", "N/A"),
        res.get("precision", "N/A"),
    ]

    # Log file in the CSV Format
    with open(log_path, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(entry)
