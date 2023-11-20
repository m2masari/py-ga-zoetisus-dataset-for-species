import os
import re
import pandas as pd
from config import Options
from logger import Logger
import multiprocessing
from multiprocessing import Pool

logger = Logger
options = Options()


def concatenate():
    reports = []
    for f in list(filter(lambda x: ".csv" in x, os.listdir(options.dir_response))):
        reports.append(f.split('__'))

    df_files = pd.DataFrame(reports, columns=["date_week", "view_id", "report_name", "uid_csv"])
    report_names = df_files["report_name"].sort_values().drop_duplicates().to_list()

    pool = Pool(processes=multiprocessing.cpu_count())
    # pool = Pool(processes=1)
    pool.map(concat, report_names)
    pool.close()


def concat(r):
    print("CONCATENATING Report:" + r)
    logger.info("CONCATENATING Report:" + r)
    regex = r"\d{4}-(\d{2})__\d+__(" + r + ")__(\d|\d{6})+.csv"
    matched_files = []

    for files in os.listdir(options.dir_response):
        matches = re.finditer(regex, files, re.IGNORECASE | re.DOTALL)
        for matchNum, match in enumerate(matches, start=1):
            matched_files.append(match.group())

    try:
        df = pd.concat([pd.read_csv(os.path.join(options.dir_response, report)) for report in matched_files])
        df.sort_values(by=["ga:date"], inplace=True)
        df["ga:date"] = pd.to_datetime(df["ga:date"], format='%Y%m%d')
        df.to_csv(os.path.join(options.dir_export, r + ".csv"), index=False, encoding='utf-8-sig')
        logger.critical(r + ".csv has " + str(df.shape[0]) + " rows of merged data without headers.")
        logger.info("Success: Exported to " + os.path.join(options.dir_export, r + ".csv"))
    except Exception as e:
        logger.critical(r + ".csv could not be merged and/or exported.")
        logger.critical(str(e))
        print(str(e))


