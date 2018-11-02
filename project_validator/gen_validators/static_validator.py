import logging
import os
import difflib
from os import path

from ..report.error import Error
from ..report.report_xml import XmlReport


class StaticValidator:

    def __init__(self, touchstone_root: str, test_root: str):
        self.touchstone = touchstone_root
        self.test = test_root

    def _validate(self, touchstone, test):
        list_files = [file for file in os.listdir(touchstone) if path.isfile(path.join(touchstone, file))]
        list_dirs = [directory for directory in os.listdir(touchstone) if path.isdir(path.join(touchstone, directory))]

        for selected_file in list_files:
            has_error = False
            path_test = os.path.join(test, selected_file)
            path_touch = os.path.join(touchstone, selected_file)
            content_test = []
            content_touch = []

            try:
                with open(path_test, 'r') as testFile:
                    content_tmp = testFile.read()
                    content_tmp = content_tmp.splitlines(keepends=False)
                    content_test = [line.strip() for line in content_tmp if len(line.strip()) != 0]
            except FileNotFoundError:
                has_error = True
                logging.info('file does not exist %s', path_test)
                XmlReport.add_report(Error('static', 'existence', path_test, 'file does not exist'))

            try:
                with open(path_touch, 'r') as touchFile:
                    content_tmp = touchFile.read()
                    content_tmp = content_tmp.splitlines(keepends=False)
                    content_touch = [line.strip() for line in content_tmp if len(line.strip()) != 0]
            except FileNotFoundError:
                has_error = True
                logging.error('!!!please call your service provider!!!  %s', path_touch)
                XmlReport.add_report(Error('static', 'PANIC', path_touch, '!!!please call your service provider!!!'))

            diff_result = difflib.unified_diff(content_touch, content_test, path_touch, path_test, n=0)

            output = []
            for diff in diff_result:
                output.append(diff)
                logging.info(diff)

            if len(output) > 0:
                has_error = True
                logging.info('does not match %s, %s', path_test, touchstone)
                XmlReport.add_report(Error('static', 'mismatch', path_test, 'does not match `{}`'.format(touchstone)))

            if has_error:
                logging.info('matching {} to {}... failed'.format(path_test, path_touch))
            else:
                logging.info('matching {} to {}... succeeded'.format(path_test, path_touch))

        for directory in list_dirs:
            if path.exists(path.join(test, directory)):
                self._validate(path.join(touchstone, directory), path.join(test, directory))
            else:
                logging.info('directory does not exist %s', path.join(test, directory))
                XmlReport.add_report(Error('static', 'existence', path.join(test, directory)))

    def validate(self):
        logging.debug('static validation started')
        self._validate(self.touchstone, self.test)
        logging.debug('static validation finished')
