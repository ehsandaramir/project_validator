from os import path
import xml.etree.ElementTree as ET

from src.project_validator import ProjectValidator
from src.validator.validator_factory import ValidatorFactory


class DynamicValidator:

    def __init__(self, config_path: str, validators_path: str, path_target: str):
        self.path_target = path_target
        ValidatorFactory.load_validators(validators_path)

        target_tree = ET.parse(config_path)
        self.config = target_tree.getroot()

    def _validate_project(self, config, solution_path):
        print('solution path: {}'.format(solution_path))
        project_validator = ProjectValidator(config)
        project_validator.validate(solution_path)

    def _initialize_validators(self, val_tree):
        pass

    def validate(self):
        if self.config.tag == 'solution':
            for prj in self.config:
                self._validate_project(prj, path.join(self.path_target, self.config.attrib['path']))
