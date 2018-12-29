import logging
from ..graph.graph_node import GraphNode


class GraphParser:

    def __init__(self, source: [str]):
        self.source = source
        self.root = GraphNode(None, 'csproj')
        self.current_node = self.root
        self.in_method_counter = 0

    def _extract_annotations(self, line_number):
        logging.debug('extracting annotations: `{}`'.format(self.source[line_number]))
        annotations = []
        reverse_line_counter = 2
        while line_number > reverse_line_counter and self.source[line_number - reverse_line_counter].find('[') >= 0:
            line = self.source[line_number - reverse_line_counter]
            line = line.strip().replace(' ', '')
            line = line[1:-1]
            annotations += line.split(',')
            reverse_line_counter += 1

        logging.info('annotations: {}'.format(annotations.__str__()))
        return annotations

    def parse(self):
        logging.debug('start parsing source graph')

        for line_number, line in enumerate(self.source):
            if self.current_node is not None:
                self.current_node.add_to_content(line)

            if line.find('{') >= 0:
                logging.debug('`{{` opener found at line number: {}'.format(line_number))

                if self.current_node.cat == 'method':
                    logging.debug('low level indentation found... ignoring')
                    self.in_method_counter += 1
                else:
                    logging.debug('top level indentation found {}'.format(line_number - 1))
                    tmp = GraphNode(
                        self.current_node,
                        self.source[line_number - 1],
                        self._extract_annotations(line_number))

                    if self.current_node.cat == 'csproj' and len(self.current_node.children):
                        found = False
                        for child in self.current_node.children:
                            if tmp.name == child.name:
                                self.current_node = child
                                found = True
                                break
                        if not found:
                            self.current_node.children.append(tmp)
                            self.current_node = tmp
                    else:
                        self.current_node.children.append(tmp)
                        self.current_node = tmp

            if line.find('}') >= 0:
                logging.debug('`}}` closer found at line number: {}'.format(line_number))
                if self.current_node.cat == 'method' and self.in_method_counter > 0:
                    self.in_method_counter -= 1
                else:
                    self.current_node = self.current_node.parent

        return self.root
