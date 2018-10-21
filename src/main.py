from pprint import pprint

from dynamic_validator import DynamicValidator
from static_checker import StaticChecker


if __name__ == '__main__':
    sc = StaticChecker('data/touchstone', 'data/95411018')
    sc_result = sc.evaluate()

    dv = DynamicValidator('config.xml', 'data/95411018')
    dv_result = dv.validate()

    print('\n\n---- RESULTS ----')
    print('static validations:')
    pprint(sc_result)
    print('\ndynamic validations:')
    pprint(dv_result)
