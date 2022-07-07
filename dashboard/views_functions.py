import plotly
import glob
import json
import os
import pandas as pd
import plotly.express as px
import numpy as np
import xmltodict
import ruamel.yaml
import pygal
from .models import DataCenterCountry, DataCenterState
from socket import *
import time
import requests
from . import views_snmp
from ncclient import manager
from pysnmp import hlapi
from .models import addDataCenter,ServerData


class CapabilityModules(object):
    def __init__(self):
        pass

    def restconf(self, router, port):
        try:
            myheaders={'content-type':'application/json-rpc'}
            l = "show run"
            print(l)          
            payload = [
                {
                    "jsonrpc": "2.0",
                    "method": "cli",
                    "params": {
                        "cmd": l,
                        "version": 1
                    },
                    "id": 1
                }
            ]
            # print(payload)             
            # response = requests.post(router["ip"] ,data=json.dumps(payload), headers=myheaders,auth=(router["user"] , router["password"])).json()
            response = {
    "jsonrpc": "2.0",
    "result": {
        "body": {
            "TABLE_intf": {
                "ROW_intf": [
                    {
                        "vrf-name-out": "default",
                        "intf-name": "Vlan1",
                        "proto-state": "up",
                        "link-state": "up",
                        "admin-state": "up",
                        "iod": 2,
                        "prefix": "192.168.0.5",
                        "ip-disabled": "FALSE"
                    },
                    {
                        "vrf-name-out": "default",
                        "intf-name": "Eth1/1",
                        "proto-state": "down",
                        "link-state": "down",
                        "admin-state": "up",
                        "iod": 6,
                        "prefix": "192.168.1.5",
                        "ip-disabled": "FALSE"
                    },
                    {
                        "vrf-name-out": "default",
                        "intf-name": "Eth1/7",
                        "proto-state": "down",
                        "link-state": "down",
                        "admin-state": "up",
                        "iod": 12,
                        "prefix": "192.168.2.7",
                        "ip-disabled": "FALSE"
                    }
                ]
            }
        }
    },
    "id": 1
    }
            # date_time = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
            return (200, response)
            # return (response.status_code, "Success!")
        except Exception as e:
            return (500, f"system error occuered! Error is {e}")
        
        
    def netconf(self, router, port):
        # https://ncclient-fredgan.readthedocs.io/_/downloads/en/sphinx_version/pdf/
        try:
            # with manager.connect(host=router["ip"], port=port, username=router["user"], password=router["password"], hostkey_verify=False) as connection:
                # if router["functionname"] == "capabilities":
                #     resp = connection.get_capabilities
                #     return (200, str(resp))
                # elif router["functionname"] == "config":
                #     resp = connection.get_config(source='running')
                #     return (200, str(resp))

                # resp = connection.get_config(source='running')
            resp = '<?xml version="1.0" encoding="UTF-8"?> <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:de3b5a79-f4f4-440e-bb8d-501249ef8aa7" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"><data><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"><version>16.9</version><boot-start-marker/><boot-end-marker/><service><timestamps><debug><datetime><msec></msec></datetime></debug><log><datetime><msec/></datetime></log></timestamps></service><platform><hardware xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-platform"><throughput><level><kbps>100000</kbps></level></throughput></hardware></platform><hostname>Router</hostname><enable><password><secret>cisco</secret></password></enable><username><name>admin</name><privilege>15</privilege><secret><encryption>5</encryption><secret>$1$DgKW$Y8.k0.FDMTAzuZqZVdEeU.</secret></secret></username><vrf><definition><name>Mgmt-intf</name><address-family><ipv4></ipv4><ipv6></ipv6></address-family></definition></vrf><ip><forward-protocol><protocol>nd</protocol></forward-protocol><tftp><source-interface><GigabitEthernet>0</GigabitEthernet></source-interface></tftp><http xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-http"><authentication><local/></authentication><server>true</server><secure-server>true</secure-server></http></ip><interface><GigabitEthernet><name>0</name><shutdown/><vrf><forwarding>Mgmt-intf</forwarding></vrf><negotiation xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet"><auto>true</auto></negotiation></GigabitEthernet><GigabitEthernet><name>0/0/0</name><ip><address><primary><address>192.168.0.8</address><mask>255.255.255.0</mask></primary></address></ip><negotiation xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet"><auto>true</auto></negotiation></GigabitEthernet><GigabitEthernet><name>0/0/1</name><ip><address><primary><address>192.168.1.10</address><mask>255.255.255.0</mask></primary></address></ip><negotiation xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet"><auto>true</auto></negotiation></GigabitEthernet></interface><control-plane></control-plane><login><on-success><log></log></on-success></login><multilink><bundle-name xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ppp">authenticated</bundle-name></multilink><redundancy><mode>none</mode></redundancy><spanning-tree><extend xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-spanning-tree"><system-id/></extend></spanning-tree><subscriber><templating/></subscriber><crypto><pki xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-crypto"><trustpoint><id>TP-self-signed-2470217082</id><enrollment><selfsigned/></enrollment><revocation-check>none</revocation-check><rsakeypair><key-label>TP-self-signed-2470217082</key-label></rsakeypair><subject-name>cn=IOS-Self-Signed-Certificate-2470217082</subject-name></trustpoint><certificate><chain><name>TP-self-signed-2470217082</name><certificate><serial>01</serial><certtype>self-signed</certtype></certificate></chain></certificate></pki></crypto><license><udi><pid>ISR4321/K9</pid><sn>FDO20371PKD</sn></udi><accept><end/><user/><agreement/></accept><boot><level><securityk9/></level></boot></license><line><aux><first>0</first><stopbits>1</stopbits></aux><console><first>0</first><stopbits>1</stopbits><transport><input><input>none</input></input></transport></console><vty><first>0</first><last>4</last><login></login><password><secret>cisco</secret></password></vty></line><diagnostic xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-diagnostics"><bootup><level>minimal</level></bootup></diagnostic></native><licensing xmlns="http://cisco.com/ns/yang/cisco-smart-license"><config><enable>false</enable><privacy><hostname>false</hostname><version>false</version></privacy><utility><utility-enable>false</utility-enable></utility></config></licensing><interfaces xmlns="http://openconfig.net/yang/interfaces"><interface><name>GigabitEthernet0</name><config><name>GigabitEthernet0</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>false</enabled></config><subinterfaces><subinterface><index>0</index><config><index>0</index><enabled>false</enabled></config><ipv6 xmlns="http://openconfig.net/yang/interfaces/ip"><config><enabled>false</enabled></config></ipv6></subinterface></subinterfaces><ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet"><config><mac-address>00:6b:f1:6f:7f:9f</mac-address><auto-negotiate>true</auto-negotiate></config></ethernet></interface><interface><name>GigabitEthernet0/0/0</name><config><name>GigabitEthernet0/0/0</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>true</enabled></config><subinterfaces><subinterface><index>0</index><config><index>0</index><enabled>true</enabled></config><ipv4 xmlns="http://openconfig.net/yang/interfaces/ip"><addresses><address><ip>192.168.0.8</ip><config><ip>192.168.0.8</ip><prefix-length>24</prefix-length></config></address></addresses></ipv4><ipv6 xmlns="http://openconfig.net/yang/interfaces/ip"><config><enabled>false</enabled></config></ipv6></subinterface></subinterfaces><ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet"><config><mac-address>00:6b:f1:6f:7f:10</mac-address><auto-negotiate>true</auto-negotiate></config></ethernet></interface><interface><name>GigabitEthernet0/0/1</name><config><name>GigabitEthernet0/0/1</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>true</enabled></config><subinterfaces><subinterface><index>0</index><config><index>0</index><enabled>true</enabled></config><ipv4 xmlns="http://openconfig.net/yang/interfaces/ip"><addresses><address><ip>192.168.1.10</ip><config><ip>192.168.1.10</ip><prefix-length>24</prefix-length></config></address></addresses></ipv4><ipv6 xmlns="http://openconfig.net/yang/interfaces/ip"><config><enabled>false</enabled></config></ipv6></subinterface></subinterfaces><ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet"><config><mac-address>00:6b:f1:6f:7f:11</mac-address><auto-negotiate>true</auto-negotiate></config></ethernet></interface></interfaces><network-instances xmlns="http://openconfig.net/yang/network-instance"><network-instance><name>Mgmt-intf</name><config><name>Mgmt-intf</name><type xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types">oc-ni-types:L3VRF</type><enabled-address-families xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</enabled-address-families><enabled-address-families xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</enabled-address-families></config><interfaces><interface><id>GigabitEthernet0</id><config><id>GigabitEthernet0</id><interface>GigabitEthernet0</interface></config></interface></interfaces><tables><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family></config></table></tables><protocols><protocol><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</identifier><name>DEFAULT</name><config><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</identifier><name>DEFAULT</name></config></protocol><protocol><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</identifier><name>DEFAULT</name><config><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</identifier><name>DEFAULT</name></config></protocol></protocols></network-instance><network-instance><name>default</name><config><name>default</name><type xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types">oc-ni-types:DEFAULT_INSTANCE</type><description>default-vrf [read-only]</description></config><tables><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family></config></table></tables><protocols><protocol><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</identifier><name>DEFAULT</name><config><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</identifier><name>DEFAULT</name></config></protocol><protocol><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</identifier><name>DEFAULT</name><config><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</identifier><name>DEFAULT</name></config></protocol></protocols></network-instance></network-instances><components xmlns="http://openconfig.net/yang/platform"><component><name>Slot0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties><subcomponents><subcomponent><name>Subslot0/0</name><config><name>Subslot0/0</name></config></subcomponent></subcomponents></component><component><name>SlotF0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component><component><name>SlotP0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component><component><name>SlotP2</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component><component><name>SlotR0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component><component><name>ISR4321/K9</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties><subcomponents><subcomponent><name>Slot0</name><config><name>Slot0</name></config></subcomponent><subcomponent><name>SlotF0</name><config><name>SlotF0</name></config></subcomponent><subcomponent><name>SlotP0</name><config><name>SlotP0</name></config></subcomponent><subcomponent><name>SlotP2</name><config><name>SlotP2</name></config></subcomponent><subcomponent><name>SlotR0</name><config><name>SlotR0</name></config></subcomponent></subcomponents></component><component><name>Subslot0/0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component></components><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"><interface><name>GigabitEthernet0</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>false</enabled><ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv4><ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv6></interface><interface><name>GigabitEthernet0/0/0</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>true</enabled><ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"><address><ip>192.168.0.8</ip><netmask>255.255.255.0</netmask></address></ipv4><ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv6></interface><interface><name>GigabitEthernet0/0/1</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>true</enabled><ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"><address><ip>192.168.1.10</ip><netmask>255.255.255.0</netmask></address></ipv4><ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv6></interface></interfaces><nacm xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-acm"><enable-nacm>true</enable-nacm><read-default>deny</read-default><write-default>deny</write-default><exec-default>deny</exec-default><enable-external-groups>true</enable-external-groups><rule-list><name>admin</name><group>PRIV15</group><rule><name>permit-all</name><module-name>*</module-name><access-operations>*</access-operations><action>permit</action></rule></rule-list></nacm><routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"><routing-instance><name>Mgmt-intf</name><interfaces><interface>GigabitEthernet0</interface></interfaces><routing-protocols><routing-protocol><type>static</type><name>1</name></routing-protocol></routing-protocols></routing-instance><routing-instance><name>default</name><description>default-vrf [read-only]</description><routing-protocols><routing-protocol><type>static</type><name>1</name></routing-protocol></routing-protocols></routing-instance></routing></data></rpc-reply>'
            return (200, json.dumps(xmltodict.parse(resp)))
        except Exception as e:
            return (500, f"system error occuered! Error is {e}")
        
    def snmpconf(self, router, port):
        try:
            # print(router["ip"],router["communitystring"])
            res = views_snmp.runthis(router["ip"],"none",port)
            return (200,res)
            # views_snmp.runthis(router["ip"],router["communitystring"])
        except Exception as e:
            return (500, f"Server Error! Error is:{e}")
    
class AssetsFormsVF():
    def __init__(self):
        pass

    def d_s_return(self):
        countries = DataCenterCountry.objects.all()
        states = DataCenterState.objects.all()
        return (countries, states)

    def hostscan(self, target, port):
        """
        Accepts IP Address
        Then check for the 830 Port
        return port status(Open or closed) and Time Taken in scanning
        """
        try:
            startTime = time.time()
            t_IP = gethostbyaddr(target)
            print(t_IP[0])
            s = socket(AF_INET, SOCK_STREAM)
            conn = s.connect_ex((t_IP[0], port))
            s.close()
            if(conn == 0):
                return ("Port is opened", time.time() - startTime)
            else:
    
                return ("Port is not opened", time.time() - startTime)
        except Exception as e:
            # print("port can't be scanned due to error:{}".format(e,) , time.time() - startTime)
            return ("port can't be scanned due to error:{}".format(e,) , time.time() - startTime)
            
def world_map():
    worldmap_chart = pygal.maps.world.World(tooltip_border_radius=10)
    worldmap_chart.title = 'Data Center In All Countries'
    context = {}
    data = DataCenterCountry.objects.all()
    for i in data:
        context[i.country_code] = int(i.capacity)
    
    graphs_values = [{
        'value': ('in',context.pop("in")),
        'label': 'This is the fifth',
        'xlink': {
            'href': 'http://127.0.0.1:8000/assets/india/',
            'target': '_parent'
        }
    }]
    
    worldmap_chart.add('World', context)
    worldmap_chart.add('India', graphs_values)
    world_map = worldmap_chart.render_data_uri()
    return world_map


#sankey_graph = sankey()
#india_map_plt = india_map()


 
def indian_map():

    this_dir = os.path.dirname(os.path.abspath('__file__'))
    geofile_url = os.path.join(this_dir, "dashboard", "states_india.geojson")
    
    indian_states_geojson = json.load(open(geofile_url)) 
        
    df = pd.DataFrame(list(addDataCenter.objects.all().values('Add_state','Capacity_in_MW','sqr_mtr','DataCenterName'))) 
    state_id_map ={}
    df["Capacity"] = pd.to_numeric(df["Capacity_in_MW"])
    df["Sqr Mtr"] = pd.to_numeric(df["sqr_mtr"])
    for feature in indian_states_geojson["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]
        
    df["id"] = df["Add_state"].apply(lambda x: state_id_map[x])
    # df["CapacityScale"] = np.log10(df["capacity"])
    print(df[:3])
    india_fig = px.choropleth(
        df,
        geojson=indian_states_geojson,
        locations="id",
        hover_name="Add_state",
        hover_data=["DataCenterName","Capacity","Sqr Mtr"],
        width=1000,
        # projection='natural earth',
        color = [
            37.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0,16.0,17.0,18.0,19.0,20.0,21.0,22.0,23.0,24.0,25.0,26.0,27.0,28.0,29.0,30.0,31.0,32.0,33.0,34.0,35.0,36.0,1.0
        ]
        
    )
    # print(str(dir(india_fig)), end="$"*100)
    
    india_fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},coloraxis_showscale=False)
    india_fig.update_geos(fitbounds="locations", visible=False)
    # india_fig.update_annotations(text="<a href='https://google.com' target='_blank'>Testing</a>")
    # india_fig.on_click(do_click)
    # india_fig.add_annotation(text="<a href='http://google.com' target='_blank' style='color:black;'>Visit Delhi Data Center1</a>", hovertext="Delhi DC1",x=0.2,y=0.2)
    # india_fig.add_annotation(text="<a href='http://google.com' target='_blank' style='color:black;'>Visit Delhi Data Center2</a>", hovertext="Delhi DC2",x=0.2,y=0.3)
    #indian_states_geojson["features"][0]["geometry"]["coordinates"][0][0] 

                   
    config = {'displayModeBar': False}
    india_map_plt = plotly.offline.plot(india_fig, show_link=False, config=config, output_type='div')        
    return india_map_plt

def do_click(trace, points, state):                                                               
    if points.point_inds:
        ind = points.point_inds[0]                                                               
        url = df.link.iloc[ind]                                                                   
        webbrowser.open_new_tab(url)                                                              
    
        #scatter                                                                        
 



#####################################################################################################
# import webbrowser                                                                                 #
# import pandas as pd                                                                               #
# import plotly.graph_objs as go                                                                    #
# df = pd.DataFrame({'x': [1, 2, 3],                                                                #
#                    'y': [1, 3, 2],                                                                #
#                    'link': ['https://google.com', 'https://bing.com', 'https://duckduckgo.com']}) #
#                                                                                                   #
# fig = go.FigureWidget(layout={'hovermode': 'closest'})                                            #
# scatter = fig.add_scatter(x=df.x, y=df.y, mode='markers', marker={'size': 20})                    #
#                                                                                                   #
# def do_click(trace, points, state):                                                               #
#     if points.point_inds:                                                                         #
#         ind = points.point_inds[0]                                                                #
#         url = df.link.iloc[ind]                                                                   #
#         webbrowser.open_new_tab(url)                                                              #
#                                                                                                   #
# scatter.on_click(do_click)                                                                        #
# fig                                                                                               #
#####################################################################################################
def saveServerInformation(u , data , func) : 


    #cap = (yaml.safe_load(capabilities))
    #cap = "ASDF"

    # if(func == "capabilities"):
    #     yaml = ruamel.yaml.YAML(typ='safe')
    #     d = yaml.load(data)
    #     data = json.dump(d)
    if(func == "config"):
        data = json.dumps(xmltodict.parse(data))
    
    
    # with open(f"/serverResponse/{time.time()} {func}","w") as f:
    #     f.write(str(data))
        
    obj = ServerData(user_id = u , server_data = data , function_name = func)
    obj.save()

    return data