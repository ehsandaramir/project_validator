from src.error import Error
import os.path as path

from src.source_validator import SourceValidator


class ProjectValidator:

    def __init__(self, report, config, path_target):
        self.report = report
        self.config = config
        self.path_target = path.join(path_target, config.attrib['path'])

    def _validate_source(self, config):
        print('validating source {}'.format(config.attrib['path']))
        source_validator = SourceValidator(self.report, config, path.join(self.path_target, config.attrib['path']))
        source_validator.validate()

    def validate(self):
        print('validating project `{}` at {}'.format(self.config.tag, self.config.attrib['path']))

        if path.exists(self.path_target):
            for source in self.config:
                self._validate_source(source)
        else:
            self.report.append(Error('dynamic', 'project', self.path_target, 'project does not exist'))

        return self.report
