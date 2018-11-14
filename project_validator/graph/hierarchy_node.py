import os


class HierarchyNode:

    csproj_nodes = []

    def __init__(self, parent, path: str):
        self.parent = parent
        self.children = []
        self.cat = None
        self.name = ''
        self.ext = ''
        self.path = path

        self._evaluate_ext()
        self._make_children()


    def _evaluate_category(self):
        if self.parent is None:
            self.cat = 'root'


    def _evaluate_ext(self):
        tokens = self.path.split('/')
        tokens = tokens[-1].split('.', 1)
        if len(tokens) > 1:
            self.ext = tokens[1]
            self.name = self.path.split('/')[-1].split('.', 1)[0]
        else:
            self.ext = 'd'
            self.name = tokens[0]



    def contains_child_ext(self, lookup_ext):
        for child in self.children:
            if child.ext == lookup_ext:
                return True
        return False


    def _make_children(self):
        if os.path.isdir(self.path):
            for entity in os.listdir(self.path):
                new_node = HierarchyNode(self, os.path.join(self.path, entity))

                if new_node.ext == 'csproj':
                    self.cat = 'csproj'
                    self.children.append(new_node)
                    HierarchyNode.csproj_nodes.append(new_node)
                if new_node.ext == 'sln':
                    self.cat = 'sln'
                if new_node.ext == 'cs':
                    new_node.cat = 'source'
                    self.children.append(new_node)
                if new_node.ext == 'd':
                    if self.cat == 'csproj':
                        if new_node.name.find('TestData') >= 0:
                            new_node.cat = 'test_data'
                            self.children.append(new_node)
                    else:
                        self.children.append(new_node)


    def __repr__(self):
        return '<{}({}:{}) :: {}>'.format(self.cat, self.name, self.ext, self.path)
