import csv
from dataclasses import asdict
from xml.dom.minidom import Document
from design_pattern.models import DroidCsvModel, AbstractBuilder


class XmlBuilder(AbstractBuilder):
    def __init__(self, csv_file: str, xml_file: str):
        # store params in class
        self.__csvFile = csv_file
        self.__xmlFile = xml_file
        self.__data = []
        self.__xmlDoc = None


    def __read_csv_file (self ):
        with open(self.__csvFile, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.__data.append( DroidCsvModel.from_dict(row) )

    def __add_entry__(self, parent , obj : DroidCsvModel ):

        for key, value in asdict(obj).items():
            xmlNode = self.__xmlDoc.createElement(key.upper())
            if value:
                xmlEntry = self.__xmlDoc.createTextNode(value)
                xmlNode.appendChild(xmlEntry)

            parent.appendChild(xmlNode)


    def build(self):
        # build steps
        # 1. read data
        self.__read_csv_file()

        # 2. convert to xml
        self.__xmlDoc = Document()
        xmlRoot = self.__xmlDoc.createElement("DroidData")
        self.__xmlDoc.appendChild(xmlRoot)

        for row in self.__data:
            xmlRow = self.__xmlDoc.createElement("row")
            xmlRoot.appendChild(xmlRow)
            self.__add_entry__(xmlRow, row)

        ## 3. finally wite file to disk
        self.__write_xml_file()

    def __write_xml_file(self):
        if self.__xmlDoc:
            with open(self.__xmlFile, "w") as f:
                self.__xmlDoc.writexml(f, addindent="\t", newl="\n", encoding="utf-8")


    ## just for unit testing
    def get_data(self):
        return self.__data