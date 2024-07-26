from src import infoAdder
import sys
from logger import setLogger, getLogger

if __name__ == "__main__":
    args = sys.argv

    setLogger(
        inFileLogLevel='INFO',
        inConsoleLogLevel='DEBUG',
        inLogName='adder_for_chrome'
    )
    infoAdder(
        inURLorPath=args[1],
        inAPIKey=args[2],
        inDatabaseID=args[3],
        inKeywordsID=(args[4] if len(args) > 4 else None),
        inGetLogger=getLogger
    )
