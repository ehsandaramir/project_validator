from error import Error
import os.path as path

from source_validator import SourceValidator


class ProjectValidator:

    def __init__(self, report, config, test):
        self.report = report
        self.config = config
        self.base_path = path.join(test, config.attrib['path'])

    def _validate_source(self, config):
        print('validating source {}'.format(config.attrib['path']))
        source_validator = SourceValidator(self.report, config, path.join(self.base_path, config.attrib['path']))
        source_validator.validate()

    def validate(self):
        print('validating project `{}` at {}'.format(self.config.tag, self.config.attrib['path']))

        if path.exists(self.base_path):
            for source in self.config:
                self._validate_source(source)
        else:
            self.report.append(Error('dynamic', 'project', self.base_path, 'project does not exist'))

        return self.report
