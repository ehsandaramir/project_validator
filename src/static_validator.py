import types
import os
import difflib
from os import path

from src.report.error import Error


class StaticValidator:

    def __init__(self, touchstone_root: str, test_root: str, **kwargs):
        self.touchstone = touchstone_root
        self.test = test_root
        self._verbose = kwargs.get('verbose', True)
        self._fail_only = kwargs.get('fail_only', False)
        self._output = []

    def _eval(self, rep, touchstone, test):
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
            except FileNotFoundError as exc:
                has_error = True
                rep.append(Error('static', 'existence', path_test, 'file does not exist'))

            try:
                with open(path_touch, 'r') as touchFile:
                    content_tmp = touchFile.read()
                    content_tmp = content_tmp.splitlines(keepends=False)
                    content_touch = [line.strip() for line in content_tmp if len(line.strip()) != 0]
            except FileNotFoundError as exe:
                has_error = True
                rep.append(Error('static', 'PANIC', path_touch, '!!!please call your service provider!!!'))

            diff_result = difflib.unified_diff(content_touch, content_test, path_touch, path_test, n=0)

            output = []
            for diff in diff_result:
                output.append(diff)

            if len(output) > 0:
                has_error = True
                rep.append(Error('static', 'mismatch', path_test, 'does not match `{}`'.format(touchstone)))

            if has_error:
                print('matching {} to {}... failed'.format(path_test, path_touch))
                if self._verbose:
                    self._add_output(output)
            else:
                if not self._fail_only:
                    print('matching {} to {}... succeeded'.format(path_test, path_touch))

        for directory in list_dirs:
            if path.exists(path.join(test, directory)):
                self._eval(rep, path.join(touchstone, directory), path.join(test, directory))
            else:
                rep.append(Error('static', 'existence', path.join(test, directory)))

    def _add_output(self, content):
        if isinstance(content, list):
            self._output += content
            return
        if isinstance(content, types.GeneratorType):
            for line in content:
                self._output.append(line)
            return
        if isinstance(content, str):
            self._output.append(content)
            return
        raise TypeError('could not print such input: {}'.format(type(content)))

    def _generate_output(self):
        for line in self._output:
            print(line)

    def _print_header(self, text: str):
        length = len(text)
        print('#' * (length + 4))
        print('# ', end='')
        print(text, end='')
        print(' #')
        print('#' * (length + 4))

    def _print_footer(self):
        print('/' * 100)
        print('/' * 100)
        print('/' * 100)

    def validate(self) -> list:
        self._print_header('starting static validation')
        report = []
        self._eval(report, self.touchstone, self.test)
        self._generate_output()
        self._print_footer()
        return report
