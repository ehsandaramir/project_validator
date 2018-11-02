import logging
from .gen_validators.dynamic_validator import DynamicValidator
from .report.report_xml import XmlReport
from .gen_validators.static_validator import StaticValidator


class BundledValidator:

    def __init__(self, information: dict):
        logging.debug('creating bundled node_validators for %s')

        self._info = information
        self._init_validators()
        self._validate()

    def _init_validators(self):
        logging.debug('initializing node_validators: static')

        self._static_validator = StaticValidator(self._info.get('touchstone'), self._info.get('input'))

        logging.debug('initializing node_validators: dynamic')
        self._dynamic_validator = DynamicValidator(self._info.get('config'), self._info.get('validators'),
                                                   self._info.get('input'))

    def _validate(self):
        logging.debug('bundled validation started')

        XmlReport.add_section('static')
        self._static_validator.validate()

        # section added internally
        self._dynamic_validator.validate()

        XmlReport.export_report(self._info.get('report'), False)
