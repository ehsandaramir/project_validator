from error import Error
from graph_parser import GraphParser


class ClassValidator:

    def __init__(self, report, config, source: [str], file_path: str):
        self.report = report
        self.source = source
        self.config = config
        self.path = file_path

    def _validate_class(self, source):
        if source[0].split(' ')[1] == self.config.attrib['name']:
            print('class name correct')
            del source[0]
            del source[-1]
        else:
            self.report.append(Error('dynamic', 'class', self.path, 'class name does not match'))

    def _validate_method(self, config, source):
        print('validating method {}'.format(config.attrib['name']))

    def validate(self):
        print('validating class `{}`'.format(self.config.attrib['name']))

        # if self.config.tag == 'class':
        #     self._validate_class(self.source)
        #
        #     for method in self.config:
        #         if method.tag == 'method':
        #             self._validate_method(method, self.source)
        # else:
        #     self.report.append(Error('dynamic', 'class', self.path, 'config is corrupt; class must be in ns'))

        # gp = GraphParser(self.source)
        # gp.parse()

