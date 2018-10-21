from graph_node import GraphNode


class GraphParser:

    def __init__(self, source):
        self.source = source
        self.root = None
        self.last_parent = None

    def parse(self):
        for line_number in range(len(self.source)):
            if self.last_parent is not None:
                self.last_parent.add_to_content(self.source[line_number])

            if self.source[line_number].find('{') >= 0:
                if self.last_parent is None:
                    self.root = GraphNode(self.last_parent, self.source[line_number-1])
                    self.last_parent = self.root
                else:
                    tmp = GraphNode(self.last_parent, self.source[line_number-1])
                    self.last_parent.children.append(tmp)
                    self.last_parent = tmp

            if self.source[line_number].find('}') >= 0:
                self.last_parent = self.last_parent.parent

        return self.root
