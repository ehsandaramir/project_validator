import xml.etree.cElementTree as ET
from xml.dom import minidom

from src.report.error import Error


class XmlReport:

    reports = {}
    recently_added_section: str = None

    @staticmethod
    def add_section(title: str):
        XmlReport.reports[title] = []
        XmlReport.recently_added_section = title

    @staticmethod
    def add_report(err: Error, section: str=None):
        if section:
            if XmlReport.recently_added_section:
                XmlReport.reports[section].append(err)
            else:
                XmlReport.add_section(section)
                XmlReport.reports[section].append(err)
        else:
            if XmlReport.recently_added_section:
                XmlReport.reports[XmlReport.recently_added_section].append(err)
            else:
                raise KeyError('please create a section first of pass it to function')

    @staticmethod
    def export_report(file_name: str, clear_after: bool=True):
        root = ET.Element("report", student_id='95411018')

        for section, errors in XmlReport.reports.items():
            section_element = ET.SubElement(root, 'section', title=section)

            category_mapper = {}
            for err in errors:
                if err.category not in category_mapper:
                    category_mapper[err.category] = ET.SubElement(section_element, err.category)

                error_root = ET.SubElement(
                    category_mapper[err.category],
                    'error',
                    category=err.category,
                    subcategory=err.sub_category)

                ET.SubElement(error_root, 'source').text = err.source
                ET.SubElement(error_root, 'message').text = err.message

        xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="   ")
        with open(file_name, 'w') as f:
            f.write(xml_string)

        if clear_after:
            XmlReport.clear_report()

    @staticmethod
    def clear_report():
        XmlReport.reports = {}
        XmlReport.recently_added_section = None
