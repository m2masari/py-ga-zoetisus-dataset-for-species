import json
import os
from reports import Analytics
from config import Options
from logger import Logger
from ratelimit import limits, sleep_and_retry

logger = Logger
options = Options()


@sleep_and_retry
@limits(calls=95, period=100)
def request(report, page_token_var):
    response = Analytics.reports().batchGet(
        # TODO: Validate values and prevent false query
        body={
            "reportRequests": [
                {
                    "viewId": report.view_id,
                    "dateRanges": report.date_range,
                    "metrics": [{"expression": i} for i in report.metrics],
                    "metricFilterClauses": [{"filters": report.metric_filters}],
                    "dimensions": [{"name": j} for j in report.dimensions],
                    "dimensionFilterClauses": [{"filters": report.dimension_filters}],
                    "segments": [{"segmentId": k} for k in report.segments],
                    "includeEmptyRows": True,
                    "pageSize": 100000,
                    "pageToken": page_token_var
                }]
        }
    ).execute()

    response_name = report.view_id + report.category + report.name

    if 'rowCount' in response['reports'][0]['data']:
        row_count = response['reports'][0]['data']['rowCount']
    else:
        row_count = 0

    page_token = response.get("reports")[0].get('nextPageToken', None)

    logger.critical(response_name + ".json has " + str(row_count) + " rows of data without headers.")

    with open(os.path.join(options.dir_request, response_name + ".json"), "w") as json_file:
        json.dump(response, json_file)

    return response, page_token
