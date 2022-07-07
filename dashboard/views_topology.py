from ncclient import manager
from pysnmp import hlapi
from dashboard import quick_snmp
import configparser
from .models import DeviceCapibility

import dashboard.topology.snmp.network_mapper



# # for netconf
# def getConfigNetconf(host , port , username,  password):

#     with manager.connect(host=host, port=port, username=username, password=password, hostkey_verify=False) as m:
#         intFilter = '''<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"> </interfaces>'''
#         reply = m.get_config('running', filter=('subtree', intFilter))

#         print(reply)

# for snmp
def getConfigSNMP(hosts , snmpCommunityStrings):
    content = """[DEFAULT]\nSnmpVersion = 2c\nSnmpCommunityString = [{0}]\nLogFile = dashboard/topology/snmp/NetworkMapper.log\nDebug = yes\n[DEVICES]\ndevices = [{1}]"""

    l = ', '.join(f'"{w}"' for w in hosts)
    l2 = ', '.join(f'"{w}"' for w in snmpCommunityStrings)

    content = content.format(l2 , l)


    config = open('dashboard/topology/snmp/config.ini' , "w")
    config.write(content)
    config.close()

    dashboard.topology.snmp.network_mapper.main_with_args()






def mainFunction():
    devices = DeviceCapibility.objects.all()

    snmpDevices = []
    snmpCommunityStrings = []

    netconfDevcies = []
    netconfInfo = []

    restconfDevices = []
    restconfInfo = []

    #snmpCommunityString.append("NETWORK@123")

    for device in devices:
        isSnmp = device.is_snmp
        isNetconf = device.is_netconf
        isRestconf = device.is_restconf
    
        ip = device.ip

        if isSnmp : 
            snmpDevices.append(ip)
            snmpCommunityStrings.append(device.commString)
            

        elif isNetconf | isRestconf:
            username = device.user
            password = device.pwd

            if isNetconf:
                # something related to netconf
                netconfDevcies.append(ip)
                netconfInfo.append({"username" : username , "password" : password})
                pass
            elif isRestconf:
                restconfDevices.append(ip)
                restconfInfo.append({"username": username, "password": password})
                # something related to restconf
                pass


        else: 
            print("Invalid Device")
    
    #getConfigSNMP(["192.168.2.10"], "NETWORK@123")
    getConfigSNMP(snmpDevices, snmpCommunityStrings)



 
    

