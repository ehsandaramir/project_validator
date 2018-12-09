import os
from typing import Union


class HierarchyNode:

    project_nodes = []

    def __init__(self, parent, path: str, make_children: bool=True):
        self.parent = parent
        self.children = []
        self.cat = ''
        self.name = ''
        self.ext = ''
        self.path = path

        self._evaluate_name_ext()
        self._evaluate_category()

        if make_children:
            self._make_children()

    def _evaluate_category(self):
        if self.parent is None:
            self.cat = 'root'
        else:
            if self.ext == 'd':
                if self.name.find('TestData') >= 0:
                    self.cat = 'test_data'
            else:
                if self.ext == 'cs':
                    self.cat = 'source'
                elif self.ext == 'csproj':
                    self.cat = 'csproj'
                    self.parent.cat = 'project'
                elif self.ext == 'sln':
                    self.cat = ''
                    self.parent.cat = 'solution'

    def _evaluate_name_ext(self):
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

                if new_node.cat != '':
                    if new_node.ext == 'd':
                        if self.cat == 'project':
                            if new_node.cat == 'test_data':
                                self.children.append(new_node)
                        else:
                            self.children.append(new_node)
                    else:
                        self.children.append(new_node)

        if self.cat == 'project':
            HierarchyNode.project_nodes.append(self)

    def get_csproj_node(self):
        for node in self.children:
            if node.cat == 'csproj':
                return node
        return None

    def __repr__(self):
        return '<{}({}:{}) :: {}>'.format(self.cat, self.name, self.ext, self.path)

