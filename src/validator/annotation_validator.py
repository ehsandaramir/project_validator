from src.report.error import Error
from src.graph.graph_node import GraphNode
from src.validator.base_validator import BaseValidator


class AnnotationValidator(BaseValidator):

    def _validate(self, node: GraphNode, source: str, terms, errors):
        all_found = True
        for term in terms:
            found = False
            for ann in node.annotations:
                if ann.find(term) >= 0:
                    found = True
                    break
            if not found:
                all_found = False
                errors.append(
                    Error('dynamic', self._config.attrib['category'], source,
                          '{}: `{}` not found on `{}` {}'.format(self.name, term, node.name, node.cat)))
        return all_found
