from src.error import Error
import os.path as path

from src.source_validator import SourceValidator


class ProjectValidator:

    def __init__(self, report, config):
        self.report = report
        self.config = config

    def _validate_source(self, config, path_target):
        print('validating source {}'.format(config.attrib['path']))
        source_validator = SourceValidator(self.report, config, path.join(path_target, config.attrib['path']))
        source_validator.validate()

    def validate(self, path_target):
        print('validating project `{}` at {}'.format(self.config.attrib['name'], self.config.attrib['path']))
        path_target = path.join(path_target, self.config.attrib['path'])

        if path.exists(path_target):
            for source in self.config:
                self._validate_source(source, path_target)
        else:
            self.report.append(Error('dynamic', 'project', path_target, 'project does not exist'))

        return self.report
