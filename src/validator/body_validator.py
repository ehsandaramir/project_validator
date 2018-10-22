from src.error import Error
from src.graph_node import GraphNode
from src.validator.annotation_validator import BaseValidator


class BodyValidator(BaseValidator):

    def _validate(self, node: GraphNode, source: str, terms, errors) -> bool:
        all_found = True
        for term in terms:
            found = False
            for line in node.content:
                if line.find(term) >= 0:
                    found = True
                    break
            if not found:
                all_found = False
                errors.append(
                    Error('dynamic', self._config.attrib['category'], source,
                          '{}: `{}` not found on `{}` {}'.format(self.name, term, node.name, node.cat)))
        return all_found
