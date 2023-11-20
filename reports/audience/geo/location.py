from reports import Report
from reports import filter_list
from logger import Logger

logger = Logger


def process():
    report = Report()
    report.category = "Audience"
    report.name = "GeoLocation"
    report.dimensions = ["ga:date", "ga:segment", "ga:country", "ga:city", "ga:continent",
                         "ga:pagePath", "ga:region", "ga:metro", "ga:hour"]
    report.segments = ["gaid::-1", "gaid::-2", "gaid::-3", "sessions::condition::ga:country==United States"]
    report.metrics = ["ga:users", "ga:newUsers", "ga:sessions", "ga:pageViews", "ga:bounceRate",
                      "ga:pageViewsPerSession", "ga:avgSessionDuration"]
    report.dimension_filters = [{
        "dimensionName": "ga:pagePath",
        "operator": "IN_LIST",
        "expressions": filter_list
    }]
    report.process()



if __name__ == '__main__':
    raise RuntimeError("{name} can't be run directly!".format(name=__file__))
    logger.critical("Runtime Error: File called directly!")
else:
    process()
