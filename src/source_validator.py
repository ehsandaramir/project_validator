from os import path
from src.report.error import Error
from src.graph.graph_parser import GraphParser
from src.graph.graph_validator import GraphValidator
from src.report.report_xml import XmlReport


class SourceValidator:

    def __init__(self, config, source_path):
        self.config = config
        self.source_path = source_path

    def _get_source(self):
        if path.exists(self.source_path):
            hnd = open(self.source_path, 'r')
            content = hnd.readlines()
            return content
        else:
            # self.report.append(Error('dynamic', 'source', self.source_path, 'file does not exist'))
            XmlReport.add_report(Error('dynamic', 'source', self.source_path, 'file does not exist'))
            raise FileNotFoundError('source not found')

    @staticmethod
    def _clean_source(source: [str]):
        result = []
        for line in source:
            line = line.strip()
            if len(line) > 0 and line.find('using') < 0:
                result.append(line)
        return result

    def _validate_namespace(self, config):
        try:
            source = self._get_source()
            source = SourceValidator._clean_source(source)

            graph_parser = GraphParser(source)
            graph_parser.parse()

            graph_validator = GraphValidator(graph_parser.root, config, self.source_path)
            graph_validator.validate()

        except FileNotFoundError:
            pass

    def validate(self):
        for child in self.config:
            self._validate_namespace(child)
