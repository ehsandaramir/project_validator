from pprint import pprint
from os import path

from src.dynamic_validator import DynamicValidator
from src.static_validator import StaticChecker


if __name__ == '__main__':
    base_path = '../test_data'
    sc = StaticChecker(path.join(base_path, 'touchstone'), path.join(base_path, '95411018'))
    sc_result = sc.evaluate()

    dv = DynamicValidator(
        path.join(base_path, 'config.xml'),
        path.join(base_path, 'validators.xml'),
        path.join(base_path, '95411018'))
    dv_result = dv.validate()

    print('\n\n---- RESULTS ----')
    print('static validations:')
    pprint(sc_result)
    print('\ndynamic validations:')
    pprint(dv_result)
