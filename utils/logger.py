# utils/logger.py
import sys
import json
from loguru import logger
from pathlib import Path


def setup_logger(logging_config):
    log_date_sdt = logging_config.get("log_date_sdt", "US")

    def serialize(record):
        module_line = record['name']
        message = record["message"]

        if 'args' in record and record["args"]:
            message = message.format(*record["args"])

        function_name = f"{record['function']}: {record['line']}"

        time_format = "%Y-%m-%d %H:%M:%S"
        if log_date_sdt == "EU":
            time_format = "%d-%m-%Y %H:%M:%S"

        subset = {
            "time": record["time"].strftime(time_format),
            "level": record["level"].name,
            "module": module_line,
            "function": function_name,
            "msg": message
        }
        return json.dumps(subset)

    def patching(record):
        record["extra"]["serialized"] = serialize(record)
        return record

    logger.remove()

    format_string = "{extra[serialized]}"
    logger.add(sys.stderr, format=format_string, filter=patching, level="DEBUG")

    if logging_config.get("log_to_file"):
        log_file_path = Path(
            logging_config.get("logs_directory", "data/logs")) / "logfile_{time}.log"
        logger.add(log_file_path,
                   rotation=logging_config.get("log_file_size", "1MB"),
                   retention=logging_config.get("log_backup_count", 3),
                   format=format_string, filter=patching, level="DEBUG",
                   compression="gz")

    logger.info("Logger started with configuration: {}", json.dumps(logging_config))
    return logger


if __name__ == "__main__":
    setup_logger(
        {"log_to_file": True, "logs_directory": "./logs", "log_file_size": "1MB",
         "log_backup_count": 3})
    logger.info("Test message")
