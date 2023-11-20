import pandas as pd
import os
from requests import Timeout
import socket
from config import Options
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials
from logger import Logger

logger = Logger

options = Options()

SCOPES = ["https://www.googleapis.com/auth/analytics.readonly"]
KEY_FILE_LOCATION = options.client_secrets


def initialize_analyticsreporting():
    credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
    analytics = build("analyticsreporting", "v4", credentials=credentials)

    return analytics


Analytics = initialize_analyticsreporting()

try:
    Accounts = pd.read_csv(options.ga_accounts, sep=",", dtype=str)
except pd.errors.EmptyDataError:
    logger.error("Accounts.csv has no entry, read failed.")
    raise RuntimeError


class Report:
    def __init__(self):
        self._category = None
        self._name = None
        self._view_id = None
        self._view_name = None
        self._date_range = [{'startDate': '7daysAgo', 'endDate': 'today'}]
        self._dimensions = []
        self._metrics = []
        self._segments = []
        self._dimension_filters = []
        self._metric_filters = []

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        self._category = value

    @category.deleter
    def category(self):
        del self._category

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @name.deleter
    def name(self):
        del self._name

    @property
    def view_id(self):
        return self._view_id

    @view_id.setter
    def view_id(self, value):
        self._view_id = value

    @view_id.deleter
    def view_id(self):
        del self._view_id

    @property
    def view_name(self):
        return self._view_name

    @view_name.setter
    def view_name(self, value):
        self._view_name = value

    @view_name.deleter
    def view_name(self):
        del self._view_name

    @property
    def date_range(self):
        return self._date_range

    @date_range.setter
    def date_range(self, value):
        self._date_range = value

    @date_range.deleter
    def date_range(self):
        del self._date_range

    @property
    def dimensions(self):
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value):
        self._dimensions = value

    @dimensions.deleter
    def dimensions(self):
        del self._dimensions

    @property
    def metrics(self):
        return self._metrics

    @metrics.setter
    def metrics(self, value):
        self._metrics = value

    @metrics.deleter
    def metrics(self):
        del self._metrics

    @property
    def segments(self):
        return self._segments

    @segments.setter
    def segments(self, value):
        self._segments = value

    @segments.deleter
    def segments(self):
        del self._segments

    @property
    def dimension_filters(self):
        return self._dimension_filters

    @dimension_filters.setter
    def dimension_filters(self, value):
        self._dimension_filters = value

    @dimension_filters.deleter
    def dimension_filters(self):
        del self._dimension_filters

    @property
    def metric_filters(self):
        return self._metric_filters

    @metric_filters.setter
    def metric_filters(self, value):
        self._metric_filters = value

    @metric_filters.deleter
    def metric_filters(self):
        del self._metric_filters

    def debug(self):

        # TODO: Create a debug export file / log for each run contains a list of reports...
        print(self.category,
              self.name,
              self.view_id,
              self.view_name,
              self.date_range,
              self.dimensions,
              self.metrics,
              self.segments,
              self.dimension_filters,
              self.metric_filters)

    def process(self):
        from reports.request import request
        from reports.manipulate import manipulate
        from reports.export import export
        from reports.merge import merge

        accounts = Accounts
        exports = []

        import datetime

        def get_weekly_calendar(year, calendar_week):
            monday = datetime.datetime.strptime(f'{year}-{calendar_week}-1', "%Y-%W-%w").date()
            return [{"startDate": (monday - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                     "endDate": (monday + datetime.timedelta(days=5.9)).strftime("%Y-%m-%d")}]

        # todo: option get set
        start_date = datetime.date(2019, 1, 1)
        end_date = datetime.date.today()

        date_list = []

        for y in range(start_date.year, end_date.year + 1):
            for w in range(0, abs(datetime.date(y, 1, 1) - datetime.date(y + 1, 1, 1)).days // 7):
                if y < end_date.year:
                    date_list.append([str(y) + "-" + str((w % 52) + 1).zfill(2), get_weekly_calendar(y, w % 52)])
                elif y == end_date.year:
                    if w < int(datetime.datetime.today().strftime("%U")):
                        date_list.append([str(y) + "-" + str((w % 52) + 1).zfill(2), get_weekly_calendar(y, w % 52)])

        failed = []

        def retry_failed(fails):
            if fails:
                logger.info("RETRY failed reports:")
                logger.info(fails)
                retried_exports = []
                for report, token, date_list in fails:
                    report.date_range = date_list[1]
                    try:
                        while token is not None:
                            resp, token = request(report, page_token)
                            if token is None:
                                file_uid2 = "0"
                            else:
                                file_uid2 = page_token

                            df2 = manipulate(resp, report.view_id, report.view_name, date_list[0])
                            export(df2, date_list[0] + "__" + report.view_id + "__" + report.category + report.name + "__" + file_uid2)
                            retried_exports.insert(-1, date_list[0] + "__" + report.view_id + "__" + report.category + report.name + "__" + file_uid2 + ".csv")
                            report.debug()
                    except HttpError as a:
                        logger.critical("Error while requesting ->")
                        logger.critical(str(a))
                        pass

        for date_item in date_list:
            for i, account in accounts.iterrows():
                self.view_id = account["viewId"]
                self.view_name = account["viewName"]
                self.date_range = date_item[1]

                page_token = ""

                if os.path.exists(os.path.join(options.dir_response, date_item[0] + "__" + self.view_id + "__" + self.category + self.name + "__" + "0.csv")):
                    logger.info("SKIPPED: " + date_item[0] + "__" + self.view_id + "__" + self.category + self.name + "__" + "0.csv")
                    print("SKIPPED: " + date_item[0] + "__" + self.view_id + "__" + self.category + self.name + "__" + "0.csv")
                else:
                    try:
                        while page_token is not None:
                            response, page_token = request(self, page_token)
                            if page_token is None:
                                file_uid = "0"
                            else:
                                file_uid = page_token

                            df = manipulate(response, self.view_id, self.view_name, date_item[0])
                            export(df, date_item[0] + "__" + self.view_id + "__" + self.category + self.name + "__" + file_uid)
                            exports.insert(-1, date_item[0] + "__" + self.view_id + "__" + self.category + self.name + "__" + file_uid + ".csv")
                            self.debug()
                    except HttpError as e:
                        logger.critical("HttpError occurred while requesting ->")
                        logger.critical(vars(self))
                        logger.critical(str(e))
                        print("HttpError occurred while requesting -> \n\n")
                        print(vars(self))
                        failed.append([self, page_token, date_item])
                        print(e)
                        pass
                    except Timeout as t:
                        logger.critical("Timeout error occurred while requesting ->")
                        logger.critical(vars(self))
                        logger.critical(str(t))
                        print("Timeout error occurred while requesting -> \n\n")
                        print(vars(self))
                        failed.append([self, page_token, date_item])
                        print(t)
                        pass
                    except socket.timeout as s:
                        logger.critical("socket.timeout error occurred while requesting ->")
                        logger.critical(vars(self))
                        logger.critical(str(s))
                        print("socket.timeout error occurred while requesting -> \n\n")
                        print(vars(self))
                        failed.append([self, page_token, date_item])
                        print(s)
                        pass

        retry_failed(failed)


filter_data = pd.read_csv("config/filter_list_scope.csv",encoding='cp1252')
filter_list = filter_data["Page Path"].values.tolist()
