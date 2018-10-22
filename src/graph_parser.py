from src.graph_node import GraphNode


class GraphParser:

    def __init__(self, source):
        self.source = source
        self.root = None
        self.current_node = None
        self.in_method_counter = 0

    def parse(self):
        for line_number in range(len(self.source)):
            if self.current_node is not None:
                self.current_node.add_to_content(self.source[line_number])

            if self.source[line_number].find('{') >= 0:
                if self.current_node is None:
                    self.root = GraphNode(self.current_node, self.source[line_number - 1])
                    self.current_node = self.root
                else:
                    if self.current_node.cat == 'method':
                        self.in_method_counter += 1
                    else:
                        tmp = GraphNode(self.current_node, self.source[line_number - 1])
                        self.current_node.children.append(tmp)
                        self.current_node = tmp

            if self.source[line_number].find('}') >= 0:
                if self.current_node.cat == 'method' and self.in_method_counter > 0:
                    self.in_method_counter -= 1
                else:
                    self.current_node = self.current_node.parent

        return self.root
