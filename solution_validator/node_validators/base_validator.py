from solution_validator.graph.graph_node import GraphNode


class BaseValidator:

    def __init__(self, validator_config):
        self.name = validator_config.attrib['name']
        self._config = validator_config
        self._attribute = validator_config.attrib['attribute']

    def validate(self, node: GraphNode, source: str, params) -> (bool, list):
        errors = []
        terms = params[self._attribute].replace(' ', '').split(';')
        return self._validate(node, source, terms, errors), errors

    def _validate(self, node: GraphNode, source: str, terms, errors) -> bool:
        pass
