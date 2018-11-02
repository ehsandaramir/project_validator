from fpdf import FPDF
from datetime import datetime
from os import path
from solution_validator.report.error import Error


class PdfReport:

    line_top_offset = 4
    line_left_offset = 1
    line_height = 1
    col_width = [1, 2, 3, 7, 15]

    def __init__(self, errors: list, destination_path: str, **kwargs):
        """
        stores meta data and basic template until `generate()` is called
        :param destination_path: path of report, including file name
        :param kwargs:
        :keyword name
        :keyword status
        :keyword grade
        """
        self.reports = errors
        self.path = destination_path
        self.user_data = kwargs

        if kwargs['status'].lower() == 'succeeded':
            self.image_path = '../res/success.png'
        if kwargs['status'].lower() == 'failed':
            self.image_path = '../res/fail.png'

        self.pdf = FPDF('L', 'cm')

        self.pdf.set_title('Validation Report')
        self.pdf.set_font("Arial", size=12)

        self.line_holder = 0
        self.line_levels = []

        self._prepare_reports()
        self._create_new_page()
        self._write_page_head()
        self._write_all_reports()
        self._export()

    def _prepare_reports(self):
        all_path = []
        for report in self.reports:
            all_path.append(report.source)
        common_path = path.commonpath(all_path)

        arr = []
        for report in self.reports:
            current_path = report.source[len(common_path) + 1:]
            current_message = report.message
            if current_message is None:
                current_message = ''
            arr.append(
                Error(report.category, report.sub_category, current_path, current_message)
            )
        self.reports = arr

    def _create_new_page(self):
        self.pdf.add_page()

    def _write_page_head(self):
        heading = 'Student id: {},    status: {},    grade: {},    time: {}'\
            .format(self.user_data['name'], self.user_data['status'], self.user_data['grade'], datetime.utcnow())
        self.pdf.image(self.image_path, 1, 1, w=2, h=2)

        self.pdf.set_font("Arial", 'B', size=20)
        self.pdf.set_text_color(255, 255, 255)
        self.pdf.cell(2.5, 1, '', 0, 0, 'C')
        self.pdf.cell(0, 1, 'VALIDATION REPORT', 1, 1, 'C', 1)
        self.pdf.set_font("Arial", 'B', size=12)
        self.pdf.set_text_color(0, 0, 0)
        self.pdf.cell(2.5, 1, '', 0, 0, 'C')
        self.pdf.cell(0, 1, heading, 1, 1)
        self.pdf.ln(0.7)
        self.pdf.set_font("Arial", size=12)

    def _write_all_reports(self):
        self.pdf.set_font("Arial", 'B', size=12)
        self.pdf.cell(self.col_width[0], 1, '#', 1, 0, 'C')
        self.pdf.cell(self.col_width[1], 1, 'category', 1, 0, 'C')
        self.pdf.cell(self.col_width[2], 1, 'sub_category', 1, 0, 'C')
        self.pdf.cell(self.col_width[3], 1, 'source', 1, 0, 'C')
        self.pdf.cell(self.col_width[4], 1, 'message', 1, 0, 'C')
        self.pdf.ln()

        self.pdf.set_font("Arial", size=12)

        counter = 1
        for report in self.reports:
            self._write_single_report(counter, report)
            counter += 1

    def _write_single_report(self, index: int, report: Error):
        if report.message is None:
            report.message = ''
        self.pdf.cell(self.col_width[0], 1, index.__str__(), 1, 0, 'C')
        self.pdf.cell(self.col_width[1], 1, report.category, 1, 0, 'C')
        self.pdf.cell(self.col_width[2], 1, report.sub_category, 1, 0, 'C')
        self.pdf.cell(self.col_width[3], 1, report.source, 1, 0)
        self.pdf.cell(self.col_width[4], 1, report.message, 1, 0)
        self.pdf.ln()

    def _export(self):
        self.pdf.output(self.path)
