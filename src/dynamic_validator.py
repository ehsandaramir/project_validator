from os import path
import xml.etree.ElementTree as ET

from project_validator import ProjectValidator


class DynamicValidator:

    def __init__(self, config_path: str, test_path: str):
        tree = ET.parse(config_path)
        self.config = tree.getroot()
        self.report = []
        self.test = test_path

    def _validate_project(self, config):
        project_validator = ProjectValidator(self.report, config, self.test)
        project_validator.validate()

    def validate(self):
        if self.config.tag == 'project':
            self._validate_project(self.config)
        return self.report
