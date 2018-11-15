import os
import re
from typing import Union

from project_validator.exceptions.project_empty import ProjectEmpty
from project_validator.graph.graph_parser import GraphParser
from project_validator.graph.hierarchy_node import HierarchyNode


class HierarchyParser:

    def __init__(self, root):
        self._root = root
        self._tree = HierarchyNode(None, root)

        for csproj in self._tree.csproj_nodes:
            csproj_content = []
            for source in csproj.children:
                if source.cat == 'source':
                    csproj_content += self._get_source(source.path)

            if len(csproj_content):
                gp = GraphParser(csproj_content)
                gp.parse()
                csproj.children.append(gp.root)
            else:
                raise ProjectEmpty(f'empty project in path {csproj.parent.path}')


    def lookup_by_name(self, name_regex: str) -> Union[HierarchyNode, None]:
        bfs_queue = [self._tree]
        while len(bfs_queue):
            current = bfs_queue.pop(0)
            bfs_queue += current.children

            if re.match(name_regex, current.name):
                return current
        return None

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
        for line_no, line in enumerate(source):
            line = line.strip()

            if len(line) == 0:
                continue

            if line.find('using') >= 0:
                continue

            result.append(line)
            print(line_no)
        print('----------------------------')
        return result
