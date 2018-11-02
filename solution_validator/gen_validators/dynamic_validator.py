import logging
from os import path
import xml.etree.ElementTree as ET

from solution_validator.gen_validators.project_validator import ProjectValidator
from solution_validator.report.report_xml import XmlReport
from solution_validator.node_validators.validator_factory import ValidatorFactory


class DynamicValidator:

    def __init__(self, config_path: str, validators_path: str, path_target: str):
        self.path_target = path_target
        ValidatorFactory.load_validators(validators_path)

        target_tree = ET.parse(config_path)
        self.config = target_tree.getroot()

    def _validate_project(self, config, solution_path):
        logging.info('solution path: {}'.format(solution_path))
        project_validator = ProjectValidator(config)
        project_validator.validate(solution_path)

    def _initialize_validators(self, val_tree):
        pass

    def validate(self):
        logging.debug('dynamic validation started')

        if self.config.tag == 'solution':
            for prj in self.config:
                logging.debug('validating project %s started', prj.attrib['name'])
                XmlReport.add_section(prj.attrib['name'])
                self._validate_project(prj, path.join(self.path_target, self.config.attrib['path']))
                logging.debug('validating project %s finished', prj.attrib['name'])

        logging.debug('dynamic validation finished')
