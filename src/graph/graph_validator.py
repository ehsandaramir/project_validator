from src.report.error import Error
from src.graph.graph_node import GraphNode
from src.validator.validator_factory import ValidatorFactory


class GraphValidator:

    def __init__(self, source_root, report, config, source_path):
        self.config = config
        self.root = source_root
        self.source_path = source_path
        self.report = report

    def _validate_node_attributes(self, node: GraphNode, attributes: dict) -> bool:
        print(attributes)
        all_passed = True

        for attribute in attributes:
            if ValidatorFactory.has_validator(attribute):
                status, errors = ValidatorFactory\
                    .get_validator_by_attr(attribute)\
                    .validate(node, self.source_path, attributes)
                self.report += errors
                if not status:
                    all_passed = False

        return all_passed

    def _validate_node_existence(self, node: GraphNode, config):
        print('matching node {}\n\tto config {}: {}'.format(node, config.tag, config.attrib))
        if node.cat != config.tag:
            self.report.append(
                Error('dynamic', config.tag, self.source_path, '{} does not match: `{}`'.format(config.tag, node.cat)))

        self._validate_node_attributes(node, config.attrib)

        for conf in config:
            child_found = False
            for child in node.children:
                if child.name == conf.attrib['name']:
                    child_found = True
                    self._validate_node_existence(child, conf)
                    break

            if not child_found:
                self.report.append(Error(
                    'dynamic',
                    conf.tag,
                    self.source_path,
                    '{} not found `{}`'.format(conf.tag, conf.attrib['name'])
                ))

    def validate(self):
        try:
            self._validate_node_existence(self.root, self.config)
        except AttributeError as exc:
            print('*** an error occurred during validation ***')
