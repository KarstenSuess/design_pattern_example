import argparse

from design_pattern.xmlformats import DroidCsvXmlBuilder

def main():
    parser = argparse.ArgumentParser(exit_on_error=False)
    parser.add_argument("-i", "--input", help="input csv file (with path)", type=str, required=True)
    parser.add_argument("-o", "--out", help="output xml file (with path)", type=str, required=True)


    try:
        args = parser.parse_args()
        xmlbuidler: DroidCsvXmlBuilder = DroidCsvXmlBuilder(args.input, args.out)
        xmlbuidler.build()
        return 0
    except Exception as e:
        print("Error:", e)
        return -1

if __name__ == '__main__':
    main()
