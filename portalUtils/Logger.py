import os
import logging
from configs import Config

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format=Config.LOG_FORMAT)


class Logger:
    @staticmethod
    def get_logger(service_name, class_name):
        logger = logging.getLogger(service_name + '.' + class_name)
        service_log_file_name = service_name + ".log"
        if not os.path.exists(Config.LOG_PATH):
            os.makedirs(Config.LOG_PATH)
        service_log_file_path = os.path.join(Config.LOG_PATH, service_log_file_name)
        file_log_handler = logging.FileHandler(service_log_file_path)
        file_log_handler.setFormatter(logging.Formatter(Config.LOG_FORMAT))
        logger.addHandler(file_log_handler)
        return logger
