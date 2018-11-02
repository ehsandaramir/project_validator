import zipfile
import os
import logging
from src.dynamic_validator import DynamicValidator
from src.report.report_xml import XmlReport
from src.static_validator import StaticValidator


class BundledValidator:

    def __init__(self, student_id, file_name, report_file_name, result_path, zipped=True):
        logging.debug('creating bundled validator for %s', student_id)
        self._zipped = zipped
        self._target_path = '../test_data'
        self._result_path = result_path
        self._resource_path = '../res'
        self._student_id = student_id
        self._file_name = file_name
        self._report_path = os.path.join(self._result_path, report_file_name)

        logging.debug('input as zip: %s', zipped)

        if self._zipped:
            self._file_name_main = file_name.split('.')[0]
            self._extract_target()
        else:
            self._file_name_main = file_name
            self._target_path = os.path.join(self._target_path, self._file_name)

        self._init_validators()
        self._validate()

    def _extract_target(self):
        logging.debug('extracting %s...', self._file_name)

        zip_ref = zipfile.ZipFile(os.path.join(self._target_path, self._file_name), 'r')
        zip_ref.extractall(os.path.join(self._target_path, self._student_id))
        zip_ref.close()

        logging.debug('extraction done!')

        if os.path.exists(os.path.join(self._target_path, self._file_name_main)):
            dirs = os.listdir(os.path.join(self._target_path, self._file_name_main))
            if len(dirs) == 1:
                self._target_path = os.path.join(self._target_path, self._file_name_main)
        try:
            os.mkdir(self._target_path)
        except FileExistsError:
            pass

    def _init_validators(self):
        logging.debug('initializing validator: static')

        self._static_validator = StaticValidator(os.path.join(self._resource_path, 'touchstone'), self._target_path)

        logging.debug('initializing validator: dynamic')
        self._dynamic_validator = DynamicValidator(os.path.join(self._resource_path, 'config.xml'),
                                                   os.path.join(self._resource_path, 'validators.xml'),
                                                   self._target_path)

    def _validate(self):
        logging.debug('bundled validation started')

        XmlReport.add_section('static')
        self._static_validator.validate()

        # section added internally
        self._dynamic_validator.validate()

        XmlReport.export_report(self._report_path)
