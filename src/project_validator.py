from src.report.error import Error
import os.path as path
import logging
from src.report.report_xml import XmlReport
from src.source_validator import SourceValidator


class ProjectValidator:

    def __init__(self, config):
        self.config = config

    def _validate_source(self, config, path_target):
        logging.debug('validating source {}'.format(config.attrib['path']))
        source_validator = SourceValidator(config, path.join(path_target, config.attrib['path']))
        source_validator.validate()

    def validate(self, path_target):
        logging.debug('validating project `{}` at {}'.format(self.config.attrib['name'], self.config.attrib['path']))
        path_target = path.join(path_target, self.config.attrib['path'])

        if path.exists(path_target):
            for source in self.config:
                self._validate_source(source, path_target)
        else:
            logging.info('project does not exist %s', path_target)
            XmlReport.add_report(Error('dynamic', 'project', path_target, 'project does not exist'))
