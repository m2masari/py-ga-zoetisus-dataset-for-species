import pandas as pd
from config import Options
from logger import Logger

logger = Logger
options = Options()


def manipulate(response, view_id, view_name, week_no):
    for report in response.get('reports', []):
        column_h = report.get('columnHeader', {})
        dimension_h = column_h.get('dimensions', [])
        metric_h = [i.get('name', {}) for i in column_h.get('metricHeader', {}).get('metricHeaderEntries', [])]
        final_rows = []

        for row in report.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [])[0].get('values', {})
            row_obj = {}

            for header, dimension in zip(dimension_h, dimensions):
                row_obj[header] = dimension

            for metric_headers, metric in zip(metric_h, metrics):
                row_obj[metric_headers] = metric

            final_rows.append(row_obj)

    df = pd.DataFrame(final_rows)
    df["ga:viewId"] = view_id
    df["ga:viewName"] = view_name
    df["ga:weekNo"] = week_no

    return df


