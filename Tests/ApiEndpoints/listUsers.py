import sys
import xml.etree.ElementTree as ET

FIELDS = [
    "username",
    "firstname",
    "lasttname",
    "major",
    "minor",
    "hall",
    "class",
    "hometown",
    "state",
    "country",
    "department",
    "building",
]

def printAdvancedSearchFile(filename):
    """Prints the data stored in an XML file."""
    doc = ET.parse(filename)
    advancedSearch = doc.getroot()
    for user in advancedSearch:
        print(user.get("type"))
        for field in FIELDS:
            value = user.findtext(field)
            if value is not None:
                print(f"  {field}: {value}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        xmlfile = sys.argv[1]
    else:
        xmlfile = input("Advanced Search User XML File: ")
    printAdvancedSearchFile(xmlfile)
