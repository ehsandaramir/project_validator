import os

from project_validator.graph.graph_parser import GraphParser
from project_validator.graph.hierarchy_node import HierarchyNode


class HierarchyParser:

    def __init__(self, root):
        self._root = root
        self._tree = HierarchyNode(None, root)

        for csproj in self._tree.csproj_nodes:
            for source in csproj.parent.children:
                if source.cat == 'source':
                    print(source.path)

                    content = self._get_source(source.path)
                    gp = GraphParser(content)
                    gp.parse()
                    csproj.children.append(gp.root)


    @staticmethod
    def _get_source(source_path: str):
        if os.path.exists(source_path):
            hnd = open(source_path, 'r')
            content = hnd.readlines()
            return HierarchyParser._clean_source(content)
        else:
            raise FileNotFoundError('source not found')


    @staticmethod
    def _clean_source(source: [str]):
        result = []
        for line in source:
            line = line.strip()
            if len(line) > 0 and line.find('using') < 0:
                result.append(line)
        return result
