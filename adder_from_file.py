from src import infoAdder
import sys
import os
from yaml import safe_load
import glob
from logger import setLogger, getLogger

if __name__ == "__main__":
    args = sys.argv

    if (len(args) < 3):
        print("Usage: python adder_from_file.py <NameKeyAndID (in Key_and_ID.yaml)> <PDFPath> ")
        sys.exit(1)

    with open(os.path.join(os.path.dirname(__file__), 'Key_and_ID.yaml'), 'r') as yml:
        lConfig = safe_load(yml)
        lFiles = []
        for lPattern in args[2:]:
            lPatternFiles = glob.glob(lPattern)
            for lFile in lPatternFiles:
                lFiles.append('file://' + os.path.abspath(lFile))

    setLogger(
        inFileLogLevel='DEBUG',
        inConsoleLogLevel='DEBUG',
        inLogName='adder_from_file'
    )
    infoAdder(
        inURLorPath=lFiles,
        inAPIKey=lConfig[args[1]]['APIKey'],
        inDatabaseID=lConfig[args[1]]['DatabaseID'],
        inKeywordsID=(lConfig[args[1]]['KeywordsID']
                      if 'KeywordsID' in lConfig[args[1]] else None),
        inGetLogger=getLogger
    )
