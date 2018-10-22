from pprint import pprint
from os import path

from src.dynamic_validator import DynamicValidator
from src.report.report_generator import ReportGenerator
from src.static_validator import StaticChecker


if __name__ == '__main__':
    base_path = '../test_data'
    resource_path = '../res'
    sc = StaticChecker(path.join(resource_path, 'touchstone'), path.join(base_path, '95411018'))
    sc_result = sc.evaluate()

    dv = DynamicValidator(
        path.join(resource_path, 'config.xml'),
        path.join(resource_path, 'validators.xml'),
        path.join(base_path, '95411018'))
    dv_result = dv.validate()

    print('\n\n---- RESULTS ----')
    print('static validations:')
    pprint(sc_result)
    print('\ndynamic validations:')
    pprint(dv_result)

    reports = sc_result + dv_result
    report_generator = ReportGenerator(reports, '../report.pdf', name='95411018', status='failed', grade=83.4)
