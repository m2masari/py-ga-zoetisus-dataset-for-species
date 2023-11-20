import os
import pandas as pd
from config import Options
from logger import Logger

logger = Logger
options = Options()


def export(df, file_name):
    try:
        df.to_csv(os.path.join(options.dir_response, file_name + ".csv"), index=False, encoding='utf-8-sig')
        logger.critical(file_name + ".csv has " + str(df.shape[0]) + " rows of data without headers.")
        logger.info("Success: Exported to " + os.path.join(options.dir_export, file_name + ".csv"))
    except Exception as e:
        logger.critical(file_name + ".csv could not be exported.")
        logger.critical(str(e))
        print(str(e))
    return




