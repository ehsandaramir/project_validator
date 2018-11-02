import logging

from ..report.error import Error


class BaseReport:
    reports = {}
    recently_added_section: str = None
    report_counter = 0

    @staticmethod
    def add_section(title: str):
        logging.debug('adding report section: %s', title)
        BaseReport.reports[title] = []
        BaseReport.recently_added_section = title

    @staticmethod
    def add_report(err: Error, section: str = None):
        logging.debug('adding report item: %s', err.__str__())
        if section:
            if BaseReport.recently_added_section:
                BaseReport.reports[section].append(err)
                BaseReport.report_counter += 1
            else:
                BaseReport.add_section(section)
                BaseReport.reports[section].append(err)
                BaseReport.report_counter += 1
        else:
            if BaseReport.recently_added_section:
                BaseReport.reports[BaseReport.recently_added_section].append(err)
            else:
                raise KeyError('please create a section first of pass it to function')

    @staticmethod
    def export_report(file_name: str, clear_after: bool=True):
        raise NotImplementedError()

    @staticmethod
    def clear_report():
        logging.debug('clear error accumulator')
        BaseReport.reports = {}
        BaseReport.recently_added_section = None
        BaseReport.report_counter = 0
