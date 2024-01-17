# utils/logger.py
import sys
import json
from loguru import logger
from pathlib import Path


# Define a function to set up the logger with custom configuration
def setup_logger(logging_config):
    # Get the log_date_sdt from the provided logging_config or default to "US"
    log_date_sdt = logging_config.get("log_date_sdt", "US")

    # Define a function to serialize log records into JSON format
    def serialize(record):
        module_line = record['name']
        message = record["message"]

        if 'args' in record and record["args"]:
            message = message.format(*record["args"])

        function_name = f"{record['function']}: {record['line']}"

        # Define time format based on log_date_sdt setting
        time_format = "%Y-%m-%d %H:%M:%S"
        if log_date_sdt == "EU":
            time_format = "%d-%m-%Y %H:%M:%S"

        # Create a dictionary with log record data
        subset = {
            "time": record["time"].strftime(time_format),
            "level": record["level"].name,
            "module": module_line,
            "function": function_name,
            "msg": message
        }
        return json.dumps(subset)

    # Define a function to add serialized log data to log records
    def patching(record):
        record["extra"]["serialized"] = serialize(record)
        return record

    # Remove any existing logger configurations
    logger.remove()

    # Define the log output format using the serialized function
    format_string = "{extra[serialized]}"

    # Add a console logger with the defined format and patching function
    logger.add(sys.stderr, format=format_string, filter=patching, level="DEBUG")

    # Check if log_to_file is True in the logging configuration
    if logging_config.get("log_to_file"):
        # Define the log file path with rotation and retention settings
        log_file_path = Path(
            logging_config.get("logs_directory", "data/logs")) / "logfile_{time}.log"
        logger.add(log_file_path,
                   rotation=logging_config.get("log_file_size", "1MB"),
                   retention=logging_config.get("log_backup_count", 3),
                   format=format_string, filter=patching, level="DEBUG",
                   compression="gz")

    # Log a message indicating that the logger has been started with the provided configuration
    logger.info("Logger started with configuration: {}", json.dumps(logging_config))

    # Return the configured logger instance
    return logger


# Entry point when the script is executed directly
if __name__ == "__main__":
    # Configure the logger with default settings and log a test message
    setup_logger(
        {"log_to_file": True, "logs_directory": "data/logs", "log_file_size": "1MB",
         "log_backup_count": 3})
    logger.info("Test message")
