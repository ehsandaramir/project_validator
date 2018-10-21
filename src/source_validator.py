from os import path
from pprint import pprint

from class_validator import ClassValidator
from error import Error
from graph_parser import GraphParser
from graph_validator import GraphValidator


class SourceValidator:

    def __init__(self, report, config, source_path):
        self.report = report
        self.config = config
        self.source_path = source_path

    def _get_source(self):
        if path.exists(self.source_path):
            hnd = open(self.source_path, 'r')
            content = hnd.readlines()
            # pprint(content)
            return content
        else:
            self.report.append(Error('dynamic', 'source', self.source_path, 'does not exist'))
            return []

    def _clean_source(self, source: [str]):
        result = []
        for line in source:
            line = line.strip()
            if len(line) > 0 and line.find('using') < 0:
                result.append(line)
        pprint(result)
        return result

    def _derive_namespace(self, source: [str]):
        namespace = ''
        for index in range(len(source)):
            if source[index].find('namespace') >= 0:
                namespace = source[index].split(' ')[1]
                del source[index]
                del source[index]
                del source[-1]
                break
        return namespace

    def _validate_namespace(self, namespace_config):
        print('validating namespace: {}'.format(namespace_config.attrib['name']))
        source = self._get_source()
        source = self._clean_source(source)

        gp = GraphParser(source)
        gp.parse()

        gv = GraphValidator(gp.root, namespace_config, self.source_path)
        gv.validate()

        # namespace = self._derive_namespace(source)
        #
        # if namespace == namespace_config.attrib['name']:
        #     print('namespace validated successfully')
        #     for cls in namespace_config:
        #         class_validator = ClassValidator(self.report, cls, source, self.source_path)
        #         class_validator.validate()
        # else:
        #     self.report.append(
        #         Error('dynamic',
        #               'namespace',
        #               self.source_path,
        #               'expected: `{}` got: `{}`'.format(namespace_config.attrib['name'], namespace))
        #     )

    def validate(self):
        for child in self.config:
            self._validate_namespace(child)
        return self.report
