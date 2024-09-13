import logging


class ColorFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\033[94m",  # Blue
        logging.INFO: "\033[92m",  # Green
        logging.WARNING: "\033[93m",  # Yellow
        logging.ERROR: "\033[91m",  # Red
        logging.CRITICAL: "\033[95m",  # Magenta
    }
    RESET = "\033[0m"  # Reset color

    def format(self, record):
        log_color = self.COLORS.get(record.levelno, self.RESET)  # Get color based on log level
        message = super().format(record)
        return f"{log_color}{message}{self.RESET}"  # Colorize the log message


class logger:
    def __init__(self, log_file='app.log', log_level=logging.INFO):
        # Create a logger object
        self.logger = logging.getLogger('BasicLogger')
        self.logger.setLevel(log_level)

        # Avoid adding multiple handlers
        if not self.logger.hasHandlers():
            # Create formatter to include timestamp, log level, and message
            file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

            # Console handler (for console output)
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(ColorFormatter('%(asctime)s [%(levelname)s] %(message)s'))

            # File handler (for file output)
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(file_formatter)

            # Add handlers to the logger
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def log(self, message, level=logging.INFO):
        if level == logging.DEBUG:
            self.logger.debug(message)
        elif level == logging.INFO:
            self.logger.info(message)
        elif level == logging.WARNING:
            self.logger.warning(message)
        elif level == logging.ERROR:
            self.logger.error(message)
        elif level == logging.CRITICAL:
            self.logger.critical(message)
        else:
            self.logger.info(message)

