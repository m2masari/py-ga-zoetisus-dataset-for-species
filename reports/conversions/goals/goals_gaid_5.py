from reports import Report
from reports import filter_list
from logger import Logger

logger = Logger


def process():
    report = Report()
    report.category = "Goal5Conversions"
    report.name = "GoalURLs"
    report.dimensions = ["ga:date", "ga:segment", "ga:goalCompletionLocation"]
    report.segments = ["gaid::-1", "gaid::-2", "gaid::-3", "sessions::condition::ga:country==United States"]
    report.metrics = ["ga:goal5Starts", "ga:goal5Completions", "ga:goal5Value", "ga:goal5ConversionRate",
                      "ga:goal5Abandons", "ga:goal5AbandonRate"]
    report.dimension_filters = [{
        "dimensionName": "ga:goalCompletionLocation",
        "operator": "IN_LIST",
        "expressions": filter_list
    }]
    report.process()


if __name__ == '__main__':
    raise RuntimeError("{name} can't be run directly!".format(name=__file__))
    logger.critical("Runtime Error: File called directly!")
else:
    process()
