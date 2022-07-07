# from pysnmp import hlapi

# # https://www.oidview.com/ for oid
# def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
#     handler = hlapi.getCmd(
#         engine,
#         credentials,
#         hlapi.UdpTransportTarget((target, port)),
#         context,
#         *construct_object_types(oids)
#     )
#     return fetch(handler, 1)[0]


# def construct_object_types(list_of_oids):
#     object_types = []
#     for oid in list_of_oids:
#         object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
#     return object_types


# def fetch(handler, count):
#     result = []
#     for i in range(count):
#         try:
#             error_indication, error_status, error_index, var_binds = next(handler)
#             if not error_indication and not error_status:
#                 items = {}
#                 for var_bind in var_binds:
#                     items[str(var_bind[0])] = cast(var_bind[1])
#                     result.append(items)
#             else:
#                 raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
#         except StopIteration:
#             break
#     return result

# def cast(value):
#     try:
#         return int(value)
#     except (ValueError, TypeError):
#         try:
#             return float(value)
#         except (ValueError, TypeError):
#             try:
#                 return str(value)
#             except (ValueError, TypeError):
#                 pass
#     return value

# # for SNMPv2
# # hlapi.CommunityData('ICTSHORE'))

# # for SNMPv3
# # hlapi.UsmUserData('testuser', authKey='authenticationkey', privKey='encryptionkey', authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)


from datetime import datetime
from pysnmp import hlapi

# https://www.oidview.com/ for oid
def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    print(handler)
    return fetch(handler, 1)[0]


def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                    result.append(items)
            else:
                raise RuntimeError('Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result

def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value

# for SNMPv2

def runthis(host , communityString,port):
    
    l = []

    for i in range(8 , 10): 
        for j in range(15,30):
            l.append("1.3.6.1.2.1.31.1.1.1." + str(i) + "."  + str(j))

    # print(l)
    # res = get(host , l  , hlapi.CommunityData(communityString))
    res = {
    "1.3.6.1.2.1.31.1.1.1.8.15": 0,
    "1.3.6.1.2.1.31.1.1.1.8.16": 0,
    "1.3.6.1.2.1.31.1.1.1.8.17": 0,
    "1.3.6.1.2.1.31.1.1.1.8.18": 0,
    "1.3.6.1.2.1.31.1.1.1.8.19": 0,
    "1.3.6.1.2.1.31.1.1.1.8.20": 0,
    "1.3.6.1.2.1.31.1.1.1.8.21": 0,
    "1.3.6.1.2.1.31.1.1.1.8.22": 0,
    "1.3.6.1.2.1.31.1.1.1.8.23": 0,
    "1.3.6.1.2.1.31.1.1.1.8.24": 16017,
    "1.3.6.1.2.1.31.1.1.1.8.25": 0,
    "1.3.6.1.2.1.31.1.1.1.8.26": 0,
    "1.3.6.1.2.1.31.1.1.1.8.27": "",
    "1.3.6.1.2.1.31.1.1.1.8.28": "",
    "1.3.6.1.2.1.31.1.1.1.8.29": "",
    "1.3.6.1.2.1.31.1.1.1.9.15": 0,
    "1.3.6.1.2.1.31.1.1.1.9.16": 0,
    "1.3.6.1.2.1.31.1.1.1.9.17": 0,
    "1.3.6.1.2.1.31.1.1.1.9.18": 0,
    "1.3.6.1.2.1.31.1.1.1.9.19": 0,
    "1.3.6.1.2.1.31.1.1.1.9.20": 0,
    "1.3.6.1.2.1.31.1.1.1.9.21": 0,
    "1.3.6.1.2.1.31.1.1.1.9.22": 0,
    "1.3.6.1.2.1.31.1.1.1.9.23": 0,
    "1.3.6.1.2.1.31.1.1.1.9.24": 14294,
    "1.3.6.1.2.1.31.1.1.1.9.25": 0,
    "1.3.6.1.2.1.31.1.1.1.9.26": 0,
    "1.3.6.1.2.1.31.1.1.1.9.27": "",
    "1.3.6.1.2.1.31.1.1.1.9.28": "",
    "1.3.6.1.2.1.31.1.1.1.9.29": ""
    }
    return (res)
    
            


# for SNMPv3
# hlapi.UsmUserData('testuser', authKey='authenticationkey', privKey='encryptionkey', authProtocol=hlapi.usmHMACSHAAuthProtocol, privProtocol=hlapi.usmAesCfb128Protocol)

# iso.3.6.1.2.1.31.1.1.1.9.24

