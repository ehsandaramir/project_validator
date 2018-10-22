import filecmp, os
from os import path
from error import Error


class StaticChecker:

    def __init__(self, touchstone_root: str, test_root: str):
        self.touchstone = touchstone_root
        self.test = test_root

    @staticmethod
    def _eval(rep, tstone, test):
        list_files = [f for f in os.listdir(tstone) if path.isfile(path.join(tstone, f))]
        list_dirs = [f for f in os.listdir(tstone) if path.isdir(path.join(tstone, f))]

        result = filecmp.cmpfiles(tstone, test, list_files)

        for mis in result[1]:
            # rep.append('mismatch: {}'.format(path.join(test, mis)))
            rep.append(Error('static',  'mismatch', path.join(test, mis)))
        for err in result[2]:
            if path.exists(path.join(test, err)):
                rep.append(Error('static', 'error', path.join(test, err)))
            else:
                rep.append(Error('static', 'existence', path.join(test, err)))

        for di in list_dirs:
            if path.exists(path.join(test, di)):
                StaticChecker._eval(rep, path.join(tstone, di), path.join(test, di))
            else:
                rep.append(Error('static', 'existence', path.join(test, di)))

    def evaluate(self) -> list:
        report = []
        self._eval(report, self.touchstone, self.test)
        return report
