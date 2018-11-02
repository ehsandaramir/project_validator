from os import path
import logging
from src.report.error import Error
from src.graph.graph_parser import GraphParser
from src.graph.graph_validator import GraphValidator
from src.report.report_xml import XmlReport


class SourceValidator:

    def __init__(self, config, source_path):
        self._config = config
        self._source_path = source_path

    def _get_source(self):
        if path.exists(self._source_path):
            hnd = open(self._source_path, 'r')
            content = hnd.readlines()
            return content
        else:
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

            graph_validator = GraphValidator(graph_parser.root, config, self._source_path)
            graph_validator.validate()

        except FileNotFoundError:
            logging.info('file does not exist %s', self._source_path)
            XmlReport.add_report(Error('dynamic', 'source', self._source_path, 'file does not exist'))

    def validate(self):
        logging.debug('validating source %s', self._source_path)
        for child in self._config:
            self._validate_namespace(child)
        logging.debug('source %s examined', self._source_path)
