import logging
from xml.etree import ElementTree

from project_validator.gen_validators.porject_val import ProjectVal
from project_validator.graph.hierarchy_parser import HierarchyParser
from .gen_validators.dynamic_validator import DynamicValidator
from .report.report_xml import XmlReport
from .gen_validators.static_validator import StaticValidator


class BundledValidator:

    def __init__(self, information: dict):
        logging.debug('creating bundled node_validators for %s')

        self._info = information
        self.hierarchy = HierarchyParser(information.get('input'))

        target_tree = ElementTree.parse(information.get('config'))
        self.config = target_tree.getroot()

        for solution in self.config:
            solution_node = self.hierarchy.lookup_by_name_and_cat(solution.attrib['name'], 'solution')
            if solution_node:
                print('sol found')
                for project in solution:
                    project_node = self.hierarchy.lookup_by_name_and_cat(project.attrib['name'], 'project')
                    if project_node and project_node.parent.name == solution.attrib['name']:
                        print('project found')
                        validator = ProjectVal(project_node)
                        status = True
                        for val_config in project:
                            if not validator.exec(val_config):
                                status = False
                        if status:
                            print('successful')
                        else:
                            print('failed!')
                    else:
                        print('project not found')
            else:
                print('sol not found')

        self._init_validators()
        self._validate()

    def _init_validators(self):
        logging.debug('initializing node_validators: static')

        self._static_validator = StaticValidator(self._info.get('touchstone'), self._info.get('input'))

        logging.debug('initializing node_validators: dynamic')
        #self._dynamic_validator = DynamicValidator(self._info.get('config'), self._info.get('validators'),
        #                                           self._info.get('input'))

    def _validate(self):
        logging.debug('bundled validation started')

        XmlReport.add_section('static')
        self._static_validator.validate()

        # section added internally
        #self._dynamic_validator.validate()

        #XmlReport.export_report(self._info.get('report'), False)
