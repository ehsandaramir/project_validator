from pprint import pprint

from error import Error
from graph_node import GraphNode


class GraphValidator:

    def __init__(self, source_root, config, source_path):
        self.config = config
        self.root = source_root
        self.source_path = source_path

    @staticmethod
    def _validate_node(source_path, node: GraphNode, config, report):
        if node.cat != config.tag:
            report.append(
                Error('dynamic', config.tag, source_path, '{} does not match: `{}`'.format(config.tag, node.cat)))

        for conf in config:
            for child in node.children:
                if child.name == conf.attrib['name']:
                    GraphValidator._validate_node(source_path, child, conf, report)
                    break
            report.append(
                Error('dynamic', conf.tag, source_path, '{} not found `{}`'.format(conf.tag, conf.attrib['name'])))

    def validate(self):
        report = []
        try:
            GraphValidator._validate_node(self.source_path, self.root, self.config, report)
        except AttributeError as exc:
            print('an error occurs during validating')
        pprint(report)
