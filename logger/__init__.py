import os
from config import Options
import logging
from datetime import datetime

options = Options()

if not os.path.exists(options.dir_log):
    try:
        os.mkdir(options.dir_log)
    except OSError as error:
        print(error)

if not os.path.exists(os.path.join(options.dir_log, "debug")):
    try:
        os.mkdir(os.path.join(options.dir_log, "debug"))
    except OSError as error:
        print(error)

if not os.path.exists(os.path.join(options.dir_log, "error")):
    try:
        os.mkdir(os.path.join(options.dir_log, "error"))
    except OSError as error:
        print(error)

if not os.path.exists(os.path.join(options.dir_log, "data")):
    try:
        os.mkdir(os.path.join(options.dir_log, "data"))
    except OSError as error:
        print(error)

log_filename = datetime.now().strftime("%Y-%m-%d-%H%M")
logging.basicConfig(format="%(asctime)s::%(levelname)s::%(filename)s::%(funcName)s::%(lineno)d::%(message)s",
                    level="DEBUG")
logger = logging.getLogger()
log_formatter = logging.Formatter("%(asctime)s::%(levelname)s::%(filename)s::%(funcName)s::%(lineno)d::%(message)s")

# Console Handler - Enable if needed
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.DEBUG)
# console_handler.setFormatter(log_formatter)
# logger.addHandler(console_handler)

debug_handler = logging.FileHandler(mode="a", filename=os.path.join(options.dir_log, "debug", log_filename + ".log"))
debug_handler.setLevel(logging.DEBUG)
debug_handler.setFormatter(log_formatter)
logger.addHandler(debug_handler)

error_handler = logging.FileHandler(mode="a", filename=os.path.join(options.dir_log, "error", log_filename + ".log"))
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(log_formatter)
logger.addHandler(error_handler)

data_handler = logging.FileHandler(mode="a", filename=os.path.join(options.dir_log, "data", log_filename + ".log"))
data_handler.setLevel(logging.CRITICAL)
data_handler.setFormatter(log_formatter)
logger.addHandler(data_handler)

logger.debug("Logging module inited.")

Logger = logger

"""
USAGE

from logger import Logger
logger = Logger
logger.debug("Your log...")
"""
