import datetime
import configparser
from dashboard.topology.snmp.pyconfig import *


def log(string, severity=3):
    config = configparser.ConfigParser()
    config.read('dashboard/topology/snmp/config.ini')
    config.sections()
    outfile = open(config['DEFAULT']['LogFile'], "a+")
    timestamp = datetime.datetime.now().strftime("%Y %b %d-%H:%M:%S")
    outfile.write(timestamp + ": " + string + "\n")
    outfile.close()

    if config['DEFAULT']['Debug'] == "yes":
        print(timestamp + ": " + string)
