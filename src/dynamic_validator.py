from os import path
import xml.etree.ElementTree as ET

from src.project_validator import ProjectValidator


class DynamicValidator:

    def __init__(self, config_path: str, path_target: str):
        tree = ET.parse(config_path)
        self.config = tree.getroot()
        self.report = []
        self.path_target = path_target

    def _validate_project(self, config, solution_path):
        print('solution path: {}'.format(solution_path))
        project_validator = ProjectValidator(self.report, config, solution_path)
        project_validator.validate()

    def validate(self):
        if self.config.tag == 'project':
            self._validate_project(self.config)
        elif self.config.tag == 'solution':
            for prj in self.config:
                self._validate_project(prj, path.join(self.path_target, self.config.attrib['path']))
        return self.report
