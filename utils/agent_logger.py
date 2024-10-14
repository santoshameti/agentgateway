import logging
from typing import Any, Dict, Optional

class AgentLogger:
    def __init__(self, name: str, level: str = "ERROR", trace_id: Optional[str] = ""):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.trace_id = trace_id

        # Create console handler and set level
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # Create formatter
        if self.trace_id is not None:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(trace_id)s - %(message)s')
        else:
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        # Add formatter to ch
        ch.setFormatter(formatter)

        # Add ch to logger
        self.logger.addHandler(ch)

    def _log(self, level: str, message: str, extra: Optional[Dict[str, Any]] = None):
        if extra is None:
            extra = {}
        if self.trace_id is not None:
            extra['trace_id'] = self.trace_id
        getattr(self.logger, level)(message, extra=extra)

    def info(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log('info', message, extra)

    def warning(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log('warning', message, extra)

    def error(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log('error', message, extra)

    def debug(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log('debug', message, extra)

    def critical(self, message: str, extra: Optional[Dict[str, Any]] = None):
        self._log('critical', message, extra)

    def set_level(self, level: str):
        self.logger.setLevel(level)

    def set_trace_id(self, trace_id: str):
        self.trace_id = trace_id

    def add_file_handler(self, filename: str, level: str = "INFO"):
        file_handler = logging.FileHandler(filename)
        file_handler.setLevel(level)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(trace_id)s - %(message)s'))
        self.logger.addHandler(file_handler)