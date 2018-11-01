import xml.etree.cElementTree as ElementTree
from xml.dom import minidom

from src.report.report_base import BaseReport


class XmlReport(BaseReport):

    @staticmethod
    def export_report(file_name: str, clear_after: bool=True):
        root = ElementTree.Element("report", student_id='95411018')

        for section, errors in XmlReport.reports.items():
            section_element = ElementTree.SubElement(root, 'section', title=section)

            category_mapper = {}
            for err in errors:
                if err.category not in category_mapper:
                    category_mapper[err.category] = ElementTree.SubElement(section_element, err.category)

                error_root = ElementTree.SubElement(
                    category_mapper[err.category],
                    'error',
                    category=err.category,
                    subcategory=err.sub_category)

                ElementTree.SubElement(error_root, 'source').text = err.source
                ElementTree.SubElement(error_root, 'message').text = err.message

        xml_string = minidom.parseString(ElementTree.tostring(root)).toprettyxml(indent="   ")
        with open(file_name, 'w') as f:
            f.write(xml_string)

        if clear_after:
            XmlReport.clear_report()
