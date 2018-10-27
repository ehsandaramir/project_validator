import time
import zipfile
import os
from pprint import pprint

from src.dynamic_validator import DynamicValidator
from src.report.report_generator import ReportGenerator
from src.static_validator import StaticValidator


class BundledValidator:

    def __init__(self, student_id, file_name, zipped=True):
        self._zipped = zipped
        self._target_path = '../test_data'
        self._resource_path = '../res'
        self._student_id = student_id
        self._file_name = file_name
        self._report_path = os.path.join(self._target_path,
                                         'results/report_{}_{}.pdf'
                                         .format(self._student_id, time.time().__str__().split('.')[0]))
        try:
            os.mkdir(os.path.join(self._target_path, 'results'))
        except FileExistsError:
            pass

        if self._zipped:
            self._file_name_main = file_name.split('.')[0]
            self._extract_target()
        else:
            self._file_name_main = file_name
            self._target_path = os.path.join(self._target_path, self._file_name)

        self._init_validators()
        self._validate()

    def _extract_target(self):
        zipref = zipfile.ZipFile(os.path.join(self._target_path, self._file_name), 'r')
        zipref.extractall(os.path.join(self._target_path, self._student_id))
        zipref.close()

        if os.path.exists(os.path.join(self._target_path, self._file_name_main)):
            dirs = os.listdir(os.path.join(self._target_path, self._file_name_main))
            if len(dirs) == 1:
                self._target_path = os.path.join(self._target_path, self._file_name_main)
        try:
            os.mkdir(self._target_path)
        except FileExistsError:
            pass

    def _init_validators(self):
        self._static_validator = StaticValidator(os.path.join(self._resource_path, 'touchstone'), self._target_path, verbose=True, fail_only=True)

        self._dynamic_validator = DynamicValidator(os.path.join(self._resource_path, 'config.xml'),
                                                   os.path.join(self._resource_path, 'validators.xml'),
                                                   self._target_path)

    def _validate(self):
        static_report = self._static_validator.validate()
        dynamic_report = self._dynamic_validator.validate()
        self.final_report = static_report + dynamic_report

        pprint(self.final_report)

        report_generator = ReportGenerator(self.final_report,
                                           self._report_path,
                                           name=self._student_id,
                                           status='failed',
                                           grade=83.4)
        # TODO: Delete cached files
        # TODO: set archive as _backup
