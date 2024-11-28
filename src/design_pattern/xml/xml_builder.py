import csv

from src.design_pattern.models import DroidCsvModel


class XmlBuilder:
    def __init__(self, csv_file: str, xml_file: str):
        # store params in class
        self.__csvFile = csv_file
        self.__xmlFile = xml_file
        self.__data = []
        # read data
        self.read_csv_file()
        pass

    def read_csv_file (self ):
        with open(self.__csvFile, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.__data.append( DroidCsvModel.from_dict(row) )

    def build(self):
        pass

    def write_xml_file(self):
        pass

    ## just for unit testing
    def get_data(self):
        return self.__data