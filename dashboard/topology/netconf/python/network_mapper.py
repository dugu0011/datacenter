#!/bin/python
from pyhpecw7.comware import HPCOM7
from pyhpecw7.features.vlan import Vlan
from pyhpecw7.features.interface import Interface
from pyhpecw7.features.neighbor import Neighbors
from pyhpecw7.utils.xml.lib import *
import yaml
import pprint
import json
import re

#########################################################
# REGULAR EXPLRESSIONS FOR MATCHING PORT NAMES TO SPEEDS
# NOTE: This is used in visuzation later to color lines
#########################################################
LINK_SPEEDS = [("^TwentyGigE*", "20"),
               ("^FortyGig*", "40"),
               ("^Ten-GigabitEthernet*", "10"),
               ("^GigabitEthernet*", "1")]

#########################################################
# REGULAR EXPLRESSIONS FOR MATCHING DEVICES HIERARHY
# E.g. Access layer switches have "AC" in their name
# or aggregation layer devices have "AG" in their names
#########################################################
NODE_HIERARCHY = [('.+ICB.*', "2"),
                  ('^[a-zA-Z]{5}AG.*', "3"),
                  ('^[a-zA-Z]{5}AC.*', "2"),
                  ('^[a-zA-Z]{5}L2.*', "4")]

####################
# Connection method
####################


def connect(host, username, password, port):
  args = dict(host=host, username=username, password=password, port=port)
  print("Connecting " + host)
  # CREATE CONNECTION
  device = HPCOM7(**args)
  device.open()
  return device

################################
# Returns RAW python Dictionary
# with Neighbor NETCONF details
#################################


def getNeighbors(device):
  print('getNeighbors')
  neighbors = Neighbors(device)
  neigh_type = dict(default='lldp', choices=['cdp', 'lldp'])
  response = getattr(neighbors, "lldp")
  results = dict(neighbors=response)
  clean_results = list()

  for neighbor in results['neighbors']:
    if str(neighbor['neighbor']) == "None" or str(neighbor['neighbor']) == "":
      print("Removing probably bad neighbor \"" +
            str(neighbor['neighbor']) + "\"")
    else:
      clean_results.append(neighbor)

  return clean_results

###############################################
# Takes RAW Dictionary of Neighbors and returns
# simplified Dictionary of only Neighbor nodes
# for visuzation as a node (point)
#
# NOTE: Additionally this using RegEx puts layer
# hierarchy into the result dictionary
###############################################


def getNodesFromNeighborships(neighborships):
  print("getNodesFromNeighborships:")
  nodes = {'nodes': []}
  for key, value in neighborships.iteritems():
    print("Key:" + str(key) + ":")

    '''
    PATTERNS COMPILATIOn
    '''
    print("Hostname matched[key]: " + key)
    group = "1"  # for key (source hostname)
    for node_pattern in NODE_HIERARCHY:
      print("Pattern: " + node_pattern[0])
      pattern = re.compile(node_pattern[0])
      if pattern.match(key):
        print("match")
        group = node_pattern[1]
        break
    print("Final GROUP for key: " + key + " is " + group)

    candidate = {"id": key, "group": group, "protocol": "netconf"}
    if candidate not in nodes['nodes']:
      print("adding")
      nodes['nodes'].append(candidate)

    for neighbor in value:
      print("neighbor: " + str(neighbor['neighbor']) + ":")
      '''
      PATTERNS COMPILATIOn
      '''
      print("Hostname matched: " + neighbor['neighbor'])
      group = "1"
      for node_pattern in NODE_HIERARCHY:
        print("Pattern: " + node_pattern[0])
        pattern = re.compile(node_pattern[0])
        if pattern.match(neighbor['neighbor']):
          print("match")
          group = node_pattern[1]
          break
      print("Final GROUP for neighbor: " + key + " is " + group)

      candidate2 = {"id": neighbor['neighbor'], "group": group , "protocol" : "netconf"}
      if candidate2 not in nodes['nodes']:
        print("adding")
        nodes['nodes'].append(candidate2)

  return nodes

###############################################
# Takes RAW Dictionary of Neighbors and returns
# simplified Dictionary of only links between
# nodes for visuzation later (links)
#
# NOTE: Additionally this using RegEx puts speed
# into the result dictionary
###############################################


def getLinksFromNeighborships(neighborships):
  print("getLinksFromNeighborships:")

  links = {'links': []}
  for key, value in neighborships.iteritems():
    print(str(key))
    for neighbor in value:

      '''
      PATTERNS COMPILATIOn
      '''
      print("Interface matched: " + neighbor['local_intf'])
      speed = "1"  # DEFAULT
      for speed_pattern in LINK_SPEEDS:
        print("Pattern: " + speed_pattern[0])
        pattern = re.compile(speed_pattern[0])

        if pattern.match(neighbor['local_intf']):
          speed = speed_pattern[1]

      print("Final SPEED:" + speed)

      links['links'].append(
          {"source": key, "target": neighbor['neighbor'], "value": speed , "protocol" : "netconf"})

  return links

##############################################
# Filters out links from simplified Dictionary
# that are not physical
# (e.g Loopback or VLAN interfaces)
#
# NOTE: Uses the same RegEx definitions as
# speed assignment
##############################################


def filterNonPhysicalLinks(interfacesDict):

  onlyPhysicalInterfacesDict = dict()

  print("filterNonPhysicalLinks")
  for key, value in interfacesDict.iteritems():
    print("Key:" + str(key) + ":")
    onlyPhysicalInterfacesDict[key] = []

    for interface in value:

      bIsPhysical = False
      for name_pattern in LINK_SPEEDS:
        pattern = re.compile(name_pattern[0])

        if pattern.match(interface['local_intf']):
          bIsPhysical = True
          onlyPhysicalInterfacesDict[key].append({"local_intf": interface['local_intf'],
                                                  "oper_status": interface['oper_status'],
                                                  "admin_status": interface['admin_status'],
                                                  "actual_bandwith": interface['actual_bandwith'],
                                                  "description": interface['description']})
          break

      print(str(bIsPhysical) + " - local_intf:" +
            interface['local_intf'] + " is physical.")

  return onlyPhysicalInterfacesDict

##############################################
# Filters out links from simplified Dictionary
# that are not in Operational mode "UP"
##############################################


def filterNonActiveLinks(interfacesDict):

  onlyUpInterfacesDict = dict()

  print("filterNonActiveLinks")
  for key, value in interfacesDict.iteritems():
    print("Key:" + str(key) + ":")
    onlyUpInterfacesDict[key] = []

    for interface in value:
      if interface['oper_status'] == 'UP':
        onlyUpInterfacesDict[key].append({"local_intf": interface['local_intf'],
                                          "oper_status": interface['oper_status'],
                                          "admin_status": interface['admin_status'],
                                          "actual_bandwith": interface['actual_bandwith'],
                                          "description": interface['description']})
        print("local_intf:" + interface['local_intf'] + " is OPRATIONAL.")

  return onlyUpInterfacesDict

################################################
# Takes RAW neighbors dictionary and simplified
# links dictionary and cross-references them to
# find links that are there, but have no neighbor
################################################


def filterLinksWithoutNeighbor(interfacesDict, neighborsDict):

  neighborlessIntlist = dict()

  print("filterLinksWithoutNeighbor")
  for devicename, neiInterfaceDict in neighborships.iteritems():
    print("Key(device name):" + str(devicename) + ":")

    neighborlessIntlist[devicename] = []

    for interface in interfacesDict[devicename]:
      bHasNoNeighbor = True
      for neighbor_interface in neiInterfaceDict:
        print("local_intf: " + interface['local_intf']
              + " neighbor_interface['local_intf']:" + neighbor_interface['local_intf'])
        if interface['local_intf'] == neighbor_interface['local_intf']:
          # Tries to remove this interface from list of interfaces
          #interfacesDict[devicename].remove(interface)
          bHasNoNeighbor = False
          print("BREAK")
          break

      if bHasNoNeighbor:
        neighborlessIntlist[devicename].append(interface)
        print("Neighborless Interface on device: " +
              devicename + " int:" + interface['local_intf'])

  return neighborlessIntlist

###########################
# Collects all Interfaces
# using NETCONF interface
# from a Device
#
# NOTE: INcludes OperStatus
# and ActualBandwidth and
# few other parameters
###########################


def getInterfaces(device):
  print('getInterfaces')

  E = data_element_maker()
  top = E.top(
      E.Ifmgr(
          E.Interfaces(
              E.Interface(
              )
          )
      )
  )
  nc_get_reply = device.get(('subtree', top))

  intName = findall_in_data('Name', nc_get_reply.data_ele)
  ## 2 == DOWN ; 1 == UP
  intOperStatus = findall_in_data('OperStatus', nc_get_reply.data_ele)
  ## 2 == DOWN ; 1 == UP
  intAdminStatus = findall_in_data('AdminStatus', nc_get_reply.data_ele)
  IntActualBandwidth = findall_in_data(
      'ActualBandwidth', nc_get_reply.data_ele)
  IntDescription = findall_in_data('Description', nc_get_reply.data_ele)

  deviceActiveInterfacesDict = []
  for index in range(len(intName)):

    # Oper STATUS
    OperStatus = 'UNKNOWN'
    if intOperStatus[index].text == '2':
      OperStatus = 'DOWN'
    elif intOperStatus[index].text == '1':
      OperStatus = 'UP'

    # Admin STATUS
    AdminStatus = 'UNKNOWN'
    if intAdminStatus[index].text == '2':
      AdminStatus = 'DOWN'
    elif intAdminStatus[index].text == '1':
      AdminStatus = 'UP'

    deviceActiveInterfacesDict.append({"local_intf": intName[index].text,
                                       "oper_status": OperStatus,
                                       "admin_status": AdminStatus,
                                       "actual_bandwith": IntActualBandwidth[index].text,
                                       "description": IntDescription[index].text})

  return deviceActiveInterfacesDict


###########################
# MAIN ENTRY POINT TO THE
# SCRIPT IS HERE
###########################
def startingPoint(hosts, usernames, passwords, port=830):
  hostLen = len(hosts)
  if(hostLen != len(usernames) | hostLen != len(passwords)):
    print("Host.length != user.length | passwords.length")
    return

  print("Opening DEVICES.txt in local directory to read target device IP/hostnames")

  #This will be the primary result neighborships dictionary
  neighborships = dict()

  #This will be the primary result interfaces dictionary
  interfaces = dict()

  # connecting to a device
  print("Starting LLDP info collection...")


  for i in range(0 , hostLen) :
    host = hosts[i]
    username = usernames[i]
    password = passwords[i]

    device = connect(host, username, password, port)
    if device.connected:
      print("success")
    else:
      print("failed to connect to the " + host + " .. skipping")
      continue

    ###
    # Here we are connected, let collect Interfaces
    ###
    interfaces[host] = getInterfaces(device)

    ###
    # Here we are connected, let collect neighbors
    ###
    new_neighbors = getNeighbors(device)
    neighborships[host] = new_neighbors

    
    
    '''
    NOW LETS PRINT OUR ALL NEIGHBORSHIPS FOR DEBUG
    '''
    pprint.pprint(neighborships)
    with open('neighborships.json', 'w') as outfile:
      json.dump(neighborships, outfile, sort_keys=True, indent=4)
      print("JSON printed into neighborships.json")

    '''
    NOW LETS PRINT OUR ALL NEIGHBORSHIPS FOR DEBUG
    '''
    interfaces = filterNonActiveLinks(filterNonPhysicalLinks(interfaces))
    pprint.pprint(interfaces)
    with open('interfaces.json', 'w') as outfile:
      json.dump(interfaces, outfile, sort_keys=True, indent=4)
      print("JSON printed into interfaces.json")

    '''
    GET INTERFACES WITHOUT NEIGHRBOR
    '''
    print("=====================================")
    print("no_neighbor_interfaces.json DICTIONARY ")
    print("======================================")
    interfacesWithoutNeighbor = filterLinksWithoutNeighbor(
        interfaces, neighborships)
    with open('no_neighbor_interfaces.json', 'w') as outfile:
      json.dump(interfacesWithoutNeighbor, outfile, sort_keys=True, indent=4)
      print("JSON printed into no_neighbor_interfaces.json")

    '''
    NOW LETS FORMAT THE DICTIONARY TO NEEDED D3 LIbary JSON
    '''
    print("================")
    print("NODES DICTIONARY")
    print("================")
    nodes_dict = getNodesFromNeighborships(neighborships)
    pprint.pprint(nodes_dict)

    print("================")
    print("LINKS DICTIONARY")
    print("================")
    links_dict = getLinksFromNeighborships(neighborships)
    pprint.pprint(links_dict)

    print("==========================================")
    print("VISUALIZATION graph.json DICTIONARY MERGE")
    print("==========================================")
    visualization_dict = {
        'nodes': nodes_dict['nodes'], 'links': links_dict['links']}

    with open('graph.json', 'w') as outfile:
        json.dump(visualization_dict, outfile, sort_keys=True, indent=4)
        print("")
        print("JSON printed into graph.json")
