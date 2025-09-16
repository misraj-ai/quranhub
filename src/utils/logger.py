import logging
import os
import sys
import time
from pythonjsonlogger import jsonlogger

class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record['time'] = int(time.time() * 1000)
        log_record['message'] = log_record.pop('message', '')
        log_record['level'] = log_record.pop('levelname', '')

json_formatter = CustomJsonFormatter(
    fmt='%(levelname)s %(message)s %(funcName)s %(asctime)s'
)

logger = logging.getLogger(__name__)

# Prevent propagation to avoid duplicate logs
logger.propagate = False

# Remove existing handlers
if logger.hasHandlers():
    logger.handlers.clear()

# Set log level from env
log_level = os.environ.get('LOG_LEVEL', 'INFO').upper()
if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
    log_level = "INFO"
logger.setLevel(getattr(logging, log_level))

# Stream handler with JSON formatter
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(json_formatter)
logger.addHandler(stream_handler)
