import os
import re
import shutil
import time
import argparse
import logging.config
import zipfile

from project_validator.bundled_validator import BundledValidator
from project_validator.graph.hierarchy_parser import HierarchyParser
from project_validator.report.report_xml import XmlReport
from project_validator.graph.hierarchy_node import HierarchyNode


def make_input_path(path: str, input_student_id: str) -> tuple:
    if input_student_id:
        student = input_student_id
    else:
        tokens = path.split('/')
        for token in tokens:
            if re.match(r'^[0-9]{8}$', token):
                student = token

    if os.path.splitext(path)[1] == '.zip':
        if not os.path.isfile(path):
            raise FileNotFoundError('zip file does not exist: {}'.format(path))

        if os.path.isdir(os.path.splitext(path)[0]):
            shutil.rmtree(os.path.splitext(path)[0])

        zip_ref = zipfile.ZipFile(path, 'r')
        zip_ref.extractall(os.path.splitext(path)[0])
        zip_ref.close()

        path = os.path.splitext(path)[0]

    if len(os.path.splitext(path)[1]) != 0:
        raise NotImplementedError('{} file is not supported'.format(os.path.splitext(path)[1]))

    if not os.path.isdir(path):
        raise NotADirectoryError('input path is not a directory')

    while len(os.listdir(path)) <= 1:
        if len(os.listdir(path)) == 0:
            raise NotADirectoryError('empty directory')
        else:
            path = os.path.join(path, os.listdir(path)[0])

    return student, path


def parse_arguments():
    parser = argparse.ArgumentParser(description='Solution validator for repositories')

    parser.add_argument('input_dir', metavar='Input', type=str,
                        help='directory that contains whole repo')
    parser.add_argument('--output-dir', dest='output_dir', metavar='Output', type=str,
                        help='directory that will contain report and probably logs; default is time generated')
    parser.add_argument('--config-dir', dest='config_dir', metavar='Config', type=str,
                        help='directory that contains configs and touchstone directory; default is current directory')
    parser.add_argument('--student-id', dest='student_id', metavar='ID', type=str,
                        help='Optional student id, default is input file/directory name')
    parser.add_argument('--export-logs', dest='export_logs', action='store_true',
                        help='export verbose logs to output directory')

    parsed_args = parser.parse_args()

    return parsed_args


if __name__ == '__main__':

    working_dir = os.getcwd()
    args = parse_arguments()

    student_id, input_dir = make_input_path(args.input_dir, args.student_id)

    time_extension = time.time().__str__().split('.')[0]
    result_path = args.output_dir if args.output_dir else 'results_{}_{}'.format(student_id, time_extension)
    log_file_name = os.path.join(result_path, 'log_{}_{}.log'.format(student_id, time_extension))
    report_file_name = os.path.join(result_path, 'report_{}_{}.xml'.format(student_id, time_extension))

    config_dir = os.path.join(working_dir, args.config_dir) if args.config_dir else working_dir

    config_file_name = os.path.join(config_dir, 'config.xml')
    validators_file_name = os.path.join(config_dir, 'validators.xml')
    touchstone_dir = os.path.join(config_dir, 'touchstone/')

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

    info = {
        'student_id': student_id,
        'input': input_dir,
        'config': config_file_name,
        'validators': validators_file_name,
        'touchstone': touchstone_dir,
        'log': log_file_name,
        'report': report_file_name
    }

    hp = HierarchyParser(input_dir)
    print(hp.lookup_by_name(r'^A3Tests$'))
    print('')

    # bundled = BundledValidator(info)

    if not args.export_logs:
        os.remove(log_file_name)

    print('results exported to directory {}... {} errors reported'.format(result_path, XmlReport.report_counter))
