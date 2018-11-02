import os
import time
from .solution_validator.bundled_validator import BundledValidator
import logging.config


if __name__ == '__main__':
    student_id = '95411018'
    file_name = '95411018/DS97981/'
    result_path = '../test_results'

    time_extension = time.time().__str__().split('.')[0]
    log_file_name = os.path.join(result_path, 'log_{}_{}.log'.format(student_id, time_extension))
    report_file_name = 'report_{}_{}.xml'.format(student_id, time_extension)

    try:
        os.mkdir(result_path)
    except FileExistsError:
        pass
    finally:
        logging.basicConfig(filename=log_file_name,
                            filemode='a',
                            format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                            datefmt='%H:%M:%S',
                            level=logging.DEBUG)

    bundled_validator = BundledValidator(student_id, file_name, report_file_name, result_path, False)
