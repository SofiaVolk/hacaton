import logging.config
import time
#import matplotlib.pyplot as plt

from multiprocessing import Process

LOGGING = {
    'version': 1,
    'formatters': {  # Форматирование сообщения
        'simple': {
            'format': '[%(asctime)s] %(levelname)-8s %(module)-s - %(message)-s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },

    'handlers': {  # Обработчики сообщений
        'api_log_handler': {
            'class': 'logging.FileHandler',
            'filename': 'api_logs.txt',
            'formatter': 'simple',
        },
        'streamlogger': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },

    'loggers': {   # Логгеры
        'api_logger': {
            'handlers': ['api_log_handler', 'streamlogger'],
            'level': 'INFO',
        },
    },
}


logging.config.dictConfig(LOGGING)
api_logger = logging.getLogger('api_logger')


class Logproc(Process):
    #def __init__(self):
        #super().__init__()

    def run(self):
        # time.sleep(1)
        with open('api_logs.txt', 'r') as f:
            data = f.readlines()
        for line in data:
            timestamp_human_readable = line.split()[-1]
            #timestamp = timestamp_human_readable.split(':')
            print(timestamp_human_readable)

