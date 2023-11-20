from reports import Report
from reports import filter_list
from logger import Logger

logger = Logger


def process():
    report = Report()
    report.category = "Audience"
    report.name = "InternalSearch"
    report.dimensions = ["ga:date", "ga:segment", "ga:searchKeyword", "ga:pagePath"]
    report.segments = ["gaid::-1", "gaid::-2", "gaid::-3", "sessions::condition::ga:country==United States"]
    report.metrics = ["ga:searchUniques"]
    report.process()


if __name__ == '__main__':
    raise RuntimeError("{name} can't be run directly!".format(name=__file__))
    logger.critical("Runtime Error: File called directly!")
else:
    process()
