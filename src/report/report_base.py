from src.report.error import Error


class BaseReport:
    reports = {}
    recently_added_section: str = None

    @staticmethod
    def add_section(title: str):
        BaseReport.reports[title] = []
        BaseReport.recently_added_section = title

    @staticmethod
    def add_report(err: Error, section: str = None):
        if section:
            if BaseReport.recently_added_section:
                BaseReport.reports[section].append(err)
            else:
                BaseReport.add_section(section)
                BaseReport.reports[section].append(err)
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
        BaseReport.reports = {}
        BaseReport.recently_added_section = None
