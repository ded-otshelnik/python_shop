import logging

from django.conf import settings


logging.basicConfig(level=settings.LOGGING_LEVEL)


class CustomFormatter(logging.Formatter):
    def format(self, record):
        # Customize the log format here
        log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Set up logging configuration
class Logger:
    _instance = None

    @classmethod
    def get_instance(cls, name=None):
        if cls._instance is None:
            cls._instance = logging.getLogger(name)
            cls._instance.setLevel(logging.DEBUG)
            handler = logging.StreamHandler()
            handler.setFormatter(CustomFormatter())
            cls._instance.addHandler(handler)
        return cls._instance
