
from django.shortcuts import render, HttpResponse
from django.views import View
from django.db.models import Q
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from tablib import Dataset
import psutil
import random
import tablib
import plotly
import numpy as np
import plotly.graph_objects as go
from django.http import JsonResponse
from .models import ProcessUtil, WebsiteLinks,Product, addDataCenter
from django.views.decorators.clickjacking import xframe_options_exempt
import pandas as pd
from django.db.models import Sum
import socket
import os
import time
from django.conf import settings
import urllib3
from django.contrib.auth import logout
from .resources import PersonResource
from .resources import *
from django.contrib.auth.decorators import login_required
from dashboard.models import PagePermissionForGroup
from django.contrib.auth.models import Group, Permission
from datetime import datetime, timezone
import plotly.offline as offline
from dashboard.models import RR,DC
from . import views_functions , views_topology

from django.contrib.auth.hashers import make_password, check_password

from django.contrib.auth.models import User
from .models import UserProfile, DeviceEquipement,addDataCenter, addDataCenterRow, AddDataCenterRackcabinet, AddDevice, Notif, DeviceDetails, PatchPanel,PatchPanelPort,DeviceTemplate, DeviceCapibility,CameraMonitor , AnsibleOutput, ContactUs, RaiseTicket
from django.http import JsonResponse
import requests
from requests.exceptions import ConnectionError
from ncclient import manager
from pprint import pprint
import xmltodict
from .forms import PagePermissionForGroupForm, PatchPanelForm, RaiseTicketForm
from django.contrib.auth import get_user_model 
from django.apps import apps
from django.contrib.auth import logout

import dashboard
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import json
import subprocess
import speedtest
from csv import writer


class Ansible(View):
    def get(self , request):
        data = {
            "result" : False
        }
        return render(request , "dashboard/ansible_form.html" , data)

    def post(self , request):
        ip = request.POST["ippart1"] + "." + request.POST["ippart2"] + "." + request.POST["ippart3"] + "." + request.POST["ippart4"]
        username = request.POST["username"]
        password = request.POST["password"]

        print("username" + username)
        print("password" + password)
        #function = request.POST["function"]

        base = "dashboard/static/ansible"
        # pem = base + "/ayushk.pem"
        # username = "ubuntu"
        inventory = base + "/inventory.cfg"
        module = base + "/install_nginx.yaml"

        try:
            #output = subprocess.run(["chmod" , "400" , pem])
            #print(output)
            # if output1.returncode == 0 this means that command ran successfully (we dont need this rn)

            # TODO: if you want to create a SSH connection using password instead of private key? use -k which means ansible will ask you for a password then enter the password using subprocess.PIPE

            f = open(inventory , "w")
            f.write("[webservers]\n" + ip)
            f.close()

            output = subprocess.run(["ansible-playbook", "-i", inventory, module, "-b", "-u", username, "--extra-vars" , "ansible_password=" + password], stdout=subprocess.PIPE, text=True, input="yes")
            print(output)
        except Exception as e:
            output = e

        finally:
            data = {
                "result" : output
            }

            ansi = AnsibleOutput(result=output)
            ansi.save()

            return render(request , "dashboard/ansible_form.html" , data)


def getGraphData():

    data = {
        "one" : {

        },

        "two" : {

        },

        "three" : {

        }
    }

    js = json.dumps(data, indent = 4)
    f = open("dashboard/static/network/data/graphs1.json" , "w")

    f.write(js)
    f.close()

    return js

def logoutView(request):
    logout(request)
    return redirect('/login?msg=l')

# @login_required()
class Test(View):
    login_required()
    """
    This View is made to implement any kind of tests
    """

    def get(self, request):
        return render(request, "dashboard/test.html")


    def post(self, request):
        # data = request.GET["data"]
        # print(data)
        ip_addr = request.POST["ip_address41"] + "." + request.POST["ip_address42"] + "." + request.POST["ip_address43"] + "." + request.POST["ip_address44"]
        # return HttpResponse(str(ip_addr))
        afvf = views_functions.AssetsFormsVF()
        port, time = afvf.hostscan(ip_addr)
        # return JsonResponse({
        #     "port":port,
        #     "time":time,
        # }, status=200)
        return render(request, 'dashboard/test.html',{'port':port, 'time':time})

        
        
    
class Notification(object):
    def __init__(self):
        pass
    def trigger_email(self):
        pass

    def show_result(self, **kwargs):
        context = {
            "other" : "",
            "button_text":"Contact US",
            "button_url":"/contact-us/"
        }

        for key,value in kwargs.items():
            if key == "result":
                context["result"] = value
            if key == "helping_text":
                context["helping_text"] = value
            if key == "title":
                context["title"] = value
            if key == "button_text":
                context["button_text"] = value
            if key == "button_url":
                context["button_url"] = value
            else:
                context["other"] = context["other"] + value + " ; "

        return context      


# Create Dashboard  views here

# capability.html
class GetCapability(View):
    def get(self, request):        
        return render(request, "dashboard/capability.html")

    def post(self, request):
        nf - Notification()
        try:
            alert = ""
            data = {key.strip():request.POST[key].strip() for key in request.POST}
            router = {
                "ip":data["ippart1"]+"."+data["ippart2"]+"."+data["ippart3"]+"."+data["ippart4"],
                "port":data["portnumber"],
                "user":data["username"],
                "password":data["password"],
                "devicename":data["devicename"],
                "protocol":data["protocol-list"],
                "functionname":data.get("protocol-functions",""),
                "communitystring":data.get("communitystring","")
            }
            vf_cm = views_functions.CapabilityModules() 
            
            if data["protocol-list"] == "snmp":
                open_ports=["161","162"]
                if data["portnumber"] in open_ports:
                    status, msg = vf_cm.snmpconf(router)
                    if status == 200:
                        alert = "Device Is Alive "+str(msg)
                        return render(request, "dashboard/capability.html", {'msg':alert})
                    else:
                        alert = "Device Not Alive "+str(msg)
                        return render(request, "dashboard/capability.html", {'msg':alert})
                else:
                    alert = "As per request, Wrong Port number sent"
                    return render(request, "dashboard/capability.html", {'msg':alert})
                
            elif  data["protocol-list"] == "netconf":
                open_ports=["830","831","832","833","834","835"]
                if data["portnumber"] in open_ports:
                    status, msg = vf_cm.netconf(router)                
                    if status == 200:
                        alert = str(msg)
                        return render(request, "dashboard/capability.html", {'msg':alert})
                    else:
                        alert = "Device Not Alive "+str(msg)
                        return render(request, "dashboard/capability.html", {'msg':alert})
                else:
                    alert = "As per request, Wrong Port number sent"
                    return render(request, "dashboard/capability.html", {'msg':alert})

            elif  data["protocol-list"] == "restconf":
                if data["portnumber"] =="443":
                    status, msg = vf_cm.restconf(router)
                    
                    if status == 200:
                        alert = str(msg)
                        return render(request, "dashboard/capability.html", {'msg':alert})
                    else:
                        alert = "Device Not Alive "+str(msg)
                        return render(request, "dashboard/capability.html", {'msg':alert})
                else:
                    alert = "As per request, Wrong Port number sent"
                    return render(request, "dashboard/capability.html", {'msg':alert})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })

def newPage(request):
    return render(request,'dashboard/newDevicecapibility.html')

class AddDeviceCapability(View):
    def get(self, request):
        
        return render(request, "dashboard/DeviceCapibility.html")

    def post(self, request):
        nf = Notification()
        try:
            msg=""
            snmp = []
            snmpPorts = ["161","162"]
            netconf = []
            netPorts = ["22","831","832","833","834","835"]
            restconf = []
            restPorts = ["443"]
            alert = ""
            snmpres = ""
            restres = ""
            netres = ""
            snmp_status = False
            rest_status = False
            net_status = False
            data = {key.strip():request.POST[key].strip() for key in request.POST}
            router = {
                "ip":data["ippart1"]+"."+data["ippart2"]+"."+data["ippart3"]+"."+data["ippart4"],
                'cstring':data.get("cString",""),
                "user":data["username"],
                "password":data["password"],
                "devicename":data["devicename"],
            } 
            vf_cm = views_functions.CapabilityModules() 

            #SNMP
            if router["cstring"]:
                for i in snmpPorts:
                    status, snmpres = vf_cm.snmpconf(router,i)
                    if (status==200):
                        snmp_status = True
                    else:
                        snmp_status = False
            #REST
            for i in restPorts:
                status, restres = vf_cm.restconf(router,i)
                if (status==200):
                    rest_status = True
                else:
                    rest_status = False
            #NETCONF
            for i in netPorts:
                status, netres = vf_cm.netconf(router,i)
                if (status==200):
                    net_status = True
                else:
                    net_status = False

            #RESTCONF

            device = DeviceCapibility(name = router["devicename"],ip = router["ip"],commString = router["cstring"],user = router["user"],pwd = router["password"],is_snmp = snmp_status,is_netconf = net_status,is_restconf = rest_status, snmp =snmpres , netconf =netres ,restconf =restres)
            device.save()
            msg = "New Device Added"
            return render(request, "dashboard/DeviceCapibility.html",{'msg':msg})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })

class autoDiscovery(View):
    def get(self, request):
        return render(request, "dashboard/autoDiscover.html")

    def post(self, request):
        nf = Notification()
        try:
            msg = ""
            devices = []
            data = {key.strip():request.POST[key].strip() for key in request.POST}
            router = {
                "ip":data["ippart1"]+"."+data["ippart2"]+"."+data["ippart3"]+".",
                "last":data["ippart4"],
                "enRange":data["enRange"],
            }
            ip = router["ip"]
            last = int(router["last"])
            enRange = int(router["enRange"])+1
            # print(str(ip) + str(last))
            def scan(addr):
                s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                socket.setdefaulttimeout(1)
                result = s.connect_ex((addr,443))
                if result == 0:
                    return 1
                else :
                    return 0

            def run1():
                for i in range(last,enRange):
                    addr = str(ip) + str(i)
                    if (scan(addr)):
                        if DeviceCapibility.objects.filter(ip=addr).exists():
                            devices.append({
                            'device':addr,
                            'status':'live',
                            'action':'none'
                            })
                        else:
                            devices.append({
                            'device':addr,
                            'status':'live',
                            'action':'required'
                            })
                        # print (addr , "is live")

                    else:
                        devices.append({
                            'device':addr,
                            'status':'down',
                            'action':'none'
                        })
                        # print(addr, "is down")
                        
            run1()
            print ("Scanning completed")
            return render(request, "dashboard/autoDiscover.html",{'devices':devices})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })

class ShowDeviceCapability(View):
    def get(self, request):
        device = DeviceCapibility.objects.all()
        return render(request, "dashboard/DeviceCapibilityShow.html",{'device':device})
class EditDeviceCapabilityPage(View):
    def get(self, request):
        nf = Notification()
        try:
            device = DeviceCapibility.objects.all()
            return render(request, "dashboard/DeviceCapibilityEdit.html",{'device':device})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
class EditDeviceCapability(View):
    def get(self, request,pk):
        nf = Notification()
        try:
            device = DeviceCapibility.objects.get(id=self.kwargs['pk'])
            return render(request, "dashboard/DeviceCapiEdit.html",{'device':device})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
    def post(self, request,pk):
        nf = Notification()
        try:
            msg = ""
            data = {key.strip():request.POST[key].strip() for key in request.POST}
            router = {
                "ip":data["ippart1"],
                "user":data["username"],
                "password":data["password"],
                "devicename":data["devicename"],
                "id":data["id"],
            }
            device = DeviceCapibility.objects.get(id=router["id"])
            device.name = router["devicename"]
            device.ip = router["ip"]
            device.user = router["user"]
            device.pwd = router["password"]
            device.save()
            msg = "Device Updated Successfully"
            return render(request, "dashboard/DeviceCapiEdit.html",{'device':device, 'msg':msg})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
class DelDeviceCapabilityPage(View):
    def get(self, request):
        nf = Notification()
        try:
            device = DeviceCapibility.objects.all()
            return render(request, "dashboard/DeviceCapibilityDel.html",{'device':device})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
class DelDeviceCapability(View):
    def get(self, request,pk):
        nf = Notification()
        try:
            device = DeviceCapibility.objects.get(id=self.kwargs['pk'])
            return render(request, "dashboard/DeviceCapiDel.html",{'device':device})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
    def post(self, request,pk):
        nf = Notification()
        try:
            msg = ""
            data = {key.strip():request.POST[key].strip() for key in request.POST}
            router = {
                "id":data["id"],
            }
            print(router)
            device = DeviceCapibility.objects.get(id=router["id"])
            device.delete()
            msg = "Device Deleted Successfully"
            return redirect('show-device-capability')
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
class ScheduleDeviceCapability(View):
    def get(self, request,id):
        nf = Notification()
        try:
            device = DeviceCapibility.objects.all()
            return render(request, "dashboard/DeviceCapibilityShedule.html",{'device':device})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
    def post(self, request,id):
        nf = Notification()
        try:
            msg = ""
            data = {key.strip():request.POST[key].strip() for key in request.POST}
            router = {
                "id":data["id"],
                "date":data["date"],
            }
            device = DeviceCapibility.objects.get(id=router["id"])
            device.schedule = router["date"]
            device.save()
            msg = "Schedule Deleted Successfully"
            return redirect('show-device-capability')
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })         
        
        


        
# @login_required()        
class Assets(View):
    login_required()
    def get(self, request):

        # world_map = views_functions.world_map()
        india_map_plt = views_functions.indian_map()
        return render(request,'dashboard/assets.html',
                      {
                        #   'world_map':world_map,
                          'india_map_plt':india_map_plt,
                      })
    
    def post(self, request):
        nf = Notification()
        try:
            
            return render(request, 'dashboard/assets.html')
        except Exception as e:
            message = nf.show_result(result="Error", helping_text="HINT:SYSTEM FAULT! Please Contact Admin", title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
# @login_required()
class assetsWorld(View):
    login_required()
    def get(self, request):

        world_map = views_functions.world_map()
        return render(request,'dashboard/assets_world.html',
                      {
                          'world_map':world_map,
                      })
    
    def post(self, request):
        nf = Notification()
        try:
            
            return render(request, 'dashboard/assets_world.html')
        except Exception as e:
            message = nf.show_result(result="Error", helping_text="HINT:SYSTEM FAULT! Please Contact Admin", title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
           

    
class Home(View):
    def get(self, request):
        return render(request, "dashboard/home.html")


def showRows(request):
    id = request.POST.get("id")
    rows = addDataCenterRow.objects.filter(data_center=id).values_list()
    return JsonResponse({
            "rows":list(rows),
        }, status=200)

def showRacks(request):
    datacenter = request.POST.get("device_id")
    row = request.POST.get("row_id")
    rows = AddDataCenterRackcabinet.objects.filter(datacenter=datacenter, date_center_row=row).values_list()
    return JsonResponse({
            "rows":list(rows),
        }, status=200)

def showavailableRacks(request):
    datacenter = request.POST.get("device_id")
    row = request.POST.get("row_id")
    rows = AddDataCenterRackcabinet.objects.filter(datacenter=datacenter, date_center_row=row).values_list()
    return JsonResponse({
            "rows":list(rows),
        }, status=200)

# @login_required()
class assetsForms(View):
    login_required() 
    def get(self, request):
        nf = Notification()
        try:
            india_map_plt = views_functions.indian_map()
            af_vf = views_functions.AssetsFormsVF()
            countries, states = af_vf.d_s_return()
            data_center = addDataCenter.objects.all()
            devicetemplate = DeviceTemplate.objects.all()
            #
            # return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'devicetemplate':devicetemplate})
            return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })

    def post(self, request):
        try:
            msg=""
            india_map_plt = views_functions.indian_map()
            data_center = addDataCenter.objects.all()
            af_vf = views_functions.AssetsFormsVF()
            countries, states = af_vf.d_s_return()
            devicetemplate = DeviceTemplate.objects.all()
            if request.POST.get("form_type") == 'formOne':
                data = {key:value.strip() for key, value in request.POST.items()}
                if addDataCenter.objects.filter(DataCenterName=data["data_center_name"]):
                    msg = "Device with same name already exsist, please select other name"
                    return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                else:
                    add = addDataCenter(

                        dataCenterTag = data["data_center_tag"],
                        DataCenterName = data["data_center_name"],
                        sqr_mtr = data["sqr_mtr"],
                        Add_country = data["address_country"],
                        Add_state = data["address_state"],
                        Address = data["address_text"],
                        Contact = data["contact"],
                        PersonalDet_fname = data["full_name"],
                        PersonalDet_email = data["email_contact"],
                        Capacity_in_MW = data["capacity"],

                    )
                    add.save()
                    # print(data)
                    msg = "New Data Center Added Successfully"
                    return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
            elif request.POST.get("form_type") == 'formTwo':
                data = {key:value.strip() for key, value in request.POST.items()}
                if addDataCenterRow.objects.filter(data_center=addDataCenter.objects.get(DataCenterName=data["data_center"]), RackRow=data["rack_row"]):
                    msg = "Row already exsist, please select other row"
                    return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                else:
                    add = addDataCenterRow(
                    data_center = addDataCenter.objects.get(DataCenterName=data["data_center"]),
                    RackRow = data["rack_row"],
                    Row_Label_Tag = data["row_tag"],
                    RowColor = data["row_color_form2"],
                    )
                    add.save()
                    # print(data)
                    msg = "New Data Center Row Added Successfully"
                    return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
            elif request.POST.get("form_type") == 'formThree':
                data = {key:value.strip() for key, value in request.POST.items()}
                if AddDataCenterRackcabinet.objects.filter(datacenter=addDataCenter.objects.get(id=data["datacenter"]),date_center_row = addDataCenterRow.objects.get(id=data["rack_row"]), Rack_Label_Tag=data["rack_tag"]):
                    msg = "Rack with same name already exsist, please select other rack name"
                    return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                else:
                    add = AddDataCenterRackcabinet(
                    datacenter = addDataCenter.objects.get(id=data["datacenter"]),
                    date_center_row = addDataCenterRow.objects.get(id=data["rack_row"]),
                    Rack_Label_Tag = data["rack_tag"],
                    RowColor = data["row_color_form3"],
                    Rack_Type = data["rack_type3"],
                    Rack_Type_Information = data.get("customised_rt_information","42"), 
                    Owner = data["your_role"],
                    Patch_Panels_Ethernet = data.get("ethernet","false"),
                    Patch_Panels_Fiber = data.get("fibre","false"),
                    Patch_Panels_Other = data.get("other","false"),
                    Patch = data.get("patch_panels_information",""),
                    Special_Notes = data["special_notes"],
                    )
                    add.save()
                    msg = "New Data Center Rack (Cabinet) Added Successfully"
                    # print(data)
                    return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
            elif request.POST.get("form_type") == 'formFour':
                data = {key:value.strip() for key, value in request.POST.items()}
                if (data["submit"] == "Add Device Template"):
                    row = AddDataCenterRackcabinet.objects.filter(datacenter=addDataCenter.objects.get(id=data["datacenter"]), date_center_row=addDataCenterRow.objects.get(id=data["rack_row"]), Rack_Label_Tag=AddDataCenterRackcabinet.objects.get(id=data["cabinet"]).Rack_Label_Tag)
                    total = row[0].Rack_Type_Information

                    maxlim = AddDataCenterRackcabinet.objects.get(datacenter=addDataCenter.objects.get(id=data["datacenter"]), date_center_row=addDataCenterRow.objects.get(id=data["rack_row"]),Rack_Label_Tag=AddDataCenterRackcabinet.objects.get(id=data["cabinet"]))
                    # sum = AddDevice.objects.get(datacenter=addDataCenter.objects.get(id=data["datacenter"]),date_center_row=addDataCenterRow.objects.get(id=data["rack_row"])).aggregate(Sum('device_height'))
                    # filled = sum["device_height__sum"]
                    # print(data)
                    # print(maxlim.Rack_Type_Information)
                    if AddDevice.objects.filter(datacenter= addDataCenter.objects.get(id=data["datacenter"]), date_center_row=addDataCenterRow.objects.get(id=data["rack_row"]), data_center_rack=AddDataCenterRackcabinet.objects.get(id=data["cabinet"]), Unit_Location=data["unit_location"]):
                        msg = "Unit Location already taken, please select other location"
                        return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                    elif int(data["unit_location"]) > maxlim.Rack_Type_Information:
                        msg = "Only "+str(maxlim.Rack_Type_Information)+" are there"
                        return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                    elif int(data["device_heigth"]) > total:
                        msg = "device height limit exceeds"
                        return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                    else:
                        add = DeviceTemplate(
                            datacenter = data.get("datacenter",""),
                            date_center_row = data.get("rack_row",""),
                            data_center_rack = data.get("cabinet",""),
                            device_height = data["device_heigth"],
                            Device_Asset_Tag = data["device_asset_tag"],
                            Device_Description = data["device_description"],
                            type_of_device = data["device_type"],

                            Unit_Location = data["unit_location"],
                            Device_Information = data["device_information"],

                            network_device_category = data["network_category"],
                            network_sub_category = data["network_device_type_cat"],
                            network_number_of_ports = data["network_device_type_ports"],
                            network_uplink_ports_wan = data["network_device_type_uplink"],
                            network_connection_type_fibre = data.get("network_category_fibre","false"),
                            network_connection_type_ehthernet = data.get("network_category_ethernet","false"),
                            network_connection_type_both = data.get("network_category_both","false"),

                            security_device_category = data["security_device_type_category"],
                            security_number_of_ports_lan = data["security_device_type_ports"],
                            security_network_uplink_ports_wan = data["security_device_type_uplink"],
                            security_connection_type_fibre = data.get("security_category_fibre","false"),
                            security_connection_type_ehthernet = data.get("security_category_ethernet","false"),
                            security_connection_type_both = data.get("security_category_both","false"),

                            patch_position = data["patch_category_pos"],
                            patch_category_type_inter = data["patch_category_type_inter"],
                            # patch_category_type_cross = data["patch_category_type_cross"],
                            # patch_category_type_isp = data["patch_category_type_isp"],
                            # patch_category_type_other = data["patch_category_type_other"],
                            # path_number_of_ports = data["patch_device_type"],

                            server_number_of_ports = data["server_device_type"],
                            server_type_fibre = data.get("server_category_fibre","false"),
                            server_type_ehthernet = data.get("server_category_ethernet","false"),
                            server_type_both = data.get("server_category_both","false"),

                            chassis_number_of_blades = data["number_of_blades"],
                            chassis_total_blades_slots = data["chasis_device_type_tblades"],
                            chassis_type_fibre = data.get("chasis_category_fibre","false"),
                            chassis_type_ehthernet = data.get("chasis_category_ethernet","false"),
                            chassis_type_both = data.get("chasis_category_both","false"),

                            load_number_of_ports = data["load_device_type_ports"],
                            load_uplink_ports_wan = data["load_device_type_uplink"],
                            load_type_fibre = data.get("load_category_fibre","false"),
                            load_type_ehthernet = data.get("load_category_ethernet","false"),
                            # load_type_both = data.get("load_category_both","false"),

                            storage_number_of_controllers = data["storage_device_type_control"],
                            storage_number_of_disks = data["storage_device_type_disks"],
                            storage_capicity_range = data["storage_capicity_range"],
                            storage_capicity_input = data["storage_capicity_input"],
                            storage_type_fibre = data.get("storage_category_fibre","false"),
                            storage_type_ehthernet = data.get("storage_category_ethernet","false"),
                            storage_type_both = data.get("storage_category_both","false"),


                            tapelib_number_of_magazine = data["tape_device_type_magazine"],
                            tapelib_number_io_station = data["tape_device_typ_io"],
                            tapelib_type = data["tape_type"],
                            tapelib_number_tape_capacity = data.get("tape_device_type_tape_capicity",int(0)),
                            tapelib_storage_capacity = data["tape_device_type_storage_capicity"],
                            tapelib_space_occupied = data["tape_device_type_space"],

                            pdu_category = data["pdu_category"],
                            pdu_number_of_power_ports = data["pdu_device_type"],
                            pdu_type = data["pdu_category_type"],
                            pdu_position = data["pdu_category_pos"],

                            ups_max_loads = data["ups_category_load"],
                            ups_number_of_power_ports = data["ups_device_type"],

                            IP_Address_col1 = data.get("ip_address41",int(0)),
                            IP_Address_col2 = data.get("ip_address42",int(0)),
                            IP_Address_col3 = data.get("ip_address43",int(0)),
                            IP_Address_col4 = data.get("ip_address44",int(0)),
                            Special_Notes = data["special_notes4"],

                            deviceMake = data["DeviceMake"],
                            deviceModel = data["DeviceModel"],
                            installDate = data.get("InstallDate",""),
                            expiryDate = data.get("InstallDate",""),
                            deviceOwner = data.get("DeviceOwner",""),
                            ownerDesc = data.get("DeviceOwnerothers",""),
                            deviceWatt = data.get("DeviceWatt",float(0.0)),
                            deviceSupplies = data["DevicePowerSupplies"],
                            deviceConn = data.get("DevicePower",""),
                            templatename = data.get("quickTemplate",""),                        

                            patchtag = data.get("patchtag","false"),
                            patchlist = data.get("patchlist","false"),
                            patchcross = data.get("patchcross","false"),
                            patchuplonks = data.get("patchuplonks","false"),
                            patchswitch = data.get("patchswitch","false"),
                            patchrouter = data.get("patchrouter","false"),
                            patch_color = data.get("patch_color",""),
                            patchtag1 = data.get("patchtag1","false"),
                            patchlist1 = data.get("patchlist1","false"),
                            patchcross1 = data.get("patchcross1","false"),
                            patchuplonks1 = data.get("patchuplonks1","false"),
                            patchswitch1 = data.get("patchswitch1","false"),
                            patchrouter1 = data.get("patchrouter1","false"),
                            patch_color_two = data.get("patch_color_two",""),
                            patchtag2 = data.get("patchtag2","false"),
                            patchlist2 = data.get("patchlist2","false"),
                            patchcross2 = data.get("patchcross2","false"),
                            patchuplonks2 = data.get("patchuplonks2","false"),
                            patchswitch2 = data.get("patchswitch2","false"),
                            patchrouter2 = data.get("patchrouter2","false"),
                            patch_color_three = data.get("patch_color_three",""),
                        )
                        add.save()
                        msg = "New Device Template Added Successfully"
                        return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                if (data["submit"] == "Add Device"):
                    row = AddDataCenterRackcabinet.objects.filter(datacenter=addDataCenter.objects.get(id=data["datacenter"]), date_center_row=addDataCenterRow.objects.get(id=data["rack_row"]), Rack_Label_Tag=AddDataCenterRackcabinet.objects.get(id=data["cabinet"]).Rack_Label_Tag)
                    total = row[0].Rack_Type_Information

                    maxlim = AddDataCenterRackcabinet.objects.get(datacenter=addDataCenter.objects.get(id=data["datacenter"]), date_center_row=addDataCenterRow.objects.get(id=data["rack_row"]),Rack_Label_Tag=AddDataCenterRackcabinet.objects.get(id=data["cabinet"]))
                    # sum = AddDevice.objects.get(datacenter=addDataCenter.objects.get(id=data["datacenter"]),date_center_row=addDataCenterRow.objects.get(id=data["rack_row"])).aggregate(Sum('device_height'))
                    # filled = sum["device_height__sum"]
                    # print(data)
                    # print(maxlim.Rack_Type_Information)
                    if AddDevice.objects.filter(datacenter= addDataCenter.objects.get(id=data["datacenter"]), date_center_row=addDataCenterRow.objects.get(id=data["rack_row"]), data_center_rack=AddDataCenterRackcabinet.objects.get(id=data["cabinet"]), Unit_Location=data["unit_location"]):
                        msg = "Unit Location already taken, please select other location"
                        return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                    elif int(data["unit_location"]) > maxlim.Rack_Type_Information:
                        msg = "Only "+str(maxlim.Rack_Type_Information)+" are there"
                        return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                    elif int(data["device_heigth"]) > total:
                        msg = "device height limit exceeds"
                        return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
                    else:
                        add = AddDevice(
                            datacenter = addDataCenter.objects.get(id=data["datacenter"]),
                            date_center_row = addDataCenterRow.objects.get(id=data["rack_row"]),
                            data_center_rack = AddDataCenterRackcabinet.objects.get(id=data["cabinet"]),
                            device_height = data["device_heigth"],
                            Device_Asset_Tag = data.get("device_asset_tag",""),
                            Device_Description = data.get("device_description",""),
                            type_of_device = data["device_type"],

                            Unit_Location = data["unit_location"],
                            Device_Information = data["device_information"],

                            network_device_category = data["network_category"],
                            network_sub_category = data["network_device_type_cat"],
                            network_number_of_ports = data["network_device_type_ports"],
                            network_uplink_ports_wan = data["network_device_type_uplink"],
                            network_connection_type_fibre = data.get("network_category_fibre","false"),
                            network_connection_type_ehthernet = data.get("network_category_ethernet","false"),
                            network_connection_type_both = data.get("network_category_both","false"),

                            security_device_category = data["security_device_type_category"],
                            security_number_of_ports_lan = data["security_device_type_ports"],
                            security_network_uplink_ports_wan = data["security_device_type_uplink"],
                            security_connection_type_fibre = data.get("security_category_fibre","false"),
                            security_connection_type_ehthernet = data.get("security_category_ethernet","false"),
                            security_connection_type_both = data.get("security_category_both","false"),

                            patch_position = data["patch_category_pos"],
                            patch_category_type_inter = data["patch_category_type_inter"],
                            # patch_category_type_cross = data["patch_category_type_cross"],
                            # patch_category_type_isp = data["patch_category_type_isp"],
                            # patch_category_type_other = data["patch_category_type_other"],
                            # path_number_of_ports = data["patch_device_type"],

                            server_number_of_ports = data["server_device_type"],
                            server_type_fibre = data.get("server_category_fibre","false"),
                            server_type_ehthernet = data.get("server_category_ethernet","false"),
                            server_type_both = data.get("server_category_both","false"),

                            chassis_number_of_blades = data["number_of_blades"],
                            chassis_total_blades_slots = data["chasis_device_type_tblades"],
                            chassis_type_fibre = data.get("chasis_category_fibre","false"),
                            chassis_type_ehthernet = data.get("chasis_category_ethernet","false"),
                            chassis_type_both = data.get("chasis_category_both","false"),

                            load_number_of_ports = data["load_device_type_ports"],
                            load_uplink_ports_wan = data["load_device_type_uplink"],
                            load_type_fibre = data.get("load_category_fibre","false"),
                            load_type_ehthernet = data.get("load_category_ethernet","false"),
                            # load_type_both = data.get("load_category_both","false"),

                            storage_number_of_controllers = data["storage_device_type_control"],
                            storage_number_of_disks = data["storage_device_type_disks"],
                            storage_capicity_range = data["storage_capicity_range"],
                            storage_capicity_input = data["storage_capicity_input"],
                            storage_type_fibre = data.get("storage_category_fibre","false"),
                            storage_type_ehthernet = data.get("storage_category_ethernet","false"),
                            storage_type_both = data.get("storage_category_both","false"),


                            tapelib_number_of_magazine = data["tape_device_type_magazine"],
                            tapelib_number_io_station = data["tape_device_typ_io"],
                            tapelib_type = data["tape_type"],
                            tapelib_number_tape_capacity = data.get("tape_device_type_tape_capicity",int(0)),
                            tapelib_storage_capacity = data["tape_device_type_storage_capicity"],
                            tapelib_space_occupied = data["tape_device_type_space"],

                            pdu_category = data["pdu_category"],
                            pdu_number_of_power_ports = data["pdu_device_type"],
                            pdu_type = data["pdu_category_type"],
                            pdu_position = data["pdu_category_pos"],

                            ups_max_loads = data["ups_category_load"],
                            ups_number_of_power_ports = data["ups_device_type"],

                            IP_Address_col1 = data.get("ip_address41",int(0)),
                            IP_Address_col2 = data.get("ip_address42",int(0)),
                            IP_Address_col3 = data.get("ip_address43",int(0)),
                            IP_Address_col4 = data.get("ip_address44",int(0)),
                            Special_Notes = data["special_notes4"],

                            deviceMake = data["DeviceMake"],
                            deviceModel = data["DeviceModel"],
                            installDate = data.get("InstallDate",""),
                            expiryDate = data.get("InstallDate",""),
                            deviceOwner = data.get("DeviceOwner",""),
                            ownerDesc = data.get("DeviceOwnerothers",""),
                            deviceWatt = data.get("DeviceWatt",float(0.0)),
                            deviceSupplies = data["DevicePowerSupplies"],
                            deviceConn = data.get("DevicePower",""),

                            patchtag = data.get("patchtag","false"),
                            patchlist = data.get("patchlist","false"),
                            patchcross = data.get("patchcross","false"),
                            patchuplonks = data.get("patchuplonks","false"),
                            patchswitch = data.get("patchswitch","false"),
                            patchrouter = data.get("patchrouter","false"),
                            patch_color = data.get("patch_color",""),
                            patchtag1 = data.get("patchtag1","false"),
                            patchlist1 = data.get("patchlist1","false"),
                            patchcross1 = data.get("patchcross1","false"),
                            patchuplonks1 = data.get("patchuplonks1","false"),
                            patchswitch1 = data.get("patchswitch1","false"),
                            patchrouter1 = data.get("patchrouter1","false"),
                            patch_color_two = data.get("patch_color_two",""),
                            patchtag2 = data.get("patchtag2","false"),
                            patchlist2 = data.get("patchlist2","false"),
                            patchcross2 = data.get("patchcross2","false"),
                            patchuplonks2 = data.get("patchuplonks2","false"),
                            patchswitch2 = data.get("patchswitch2","false"),
                            patchrouter2 = data.get("patchrouter2","false"),
                            patch_color_three = data.get("patch_color_three",""),
                        )
                        add.save()
                        msg = "New Device Added Successfully"
                        return render(request, "dashboard/assets_forms.html",{'countries':countries, 'states':states,'datacenter':data_center,'msg':msg,'devicetemplate':devicetemplate,'india_map_plt':india_map_plt,})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })

def getTemplateData(request):
    id = request.POST.get("id")
    device = DeviceTemplate.objects.get(templatename=id)
    # print(device.id)
    return JsonResponse(
        {
            "datacenter":device.datacenter,
            "date_center_row":device.date_center_row,
            "data_center_rack":device.data_center_rack,
            "device_height":device.device_height,
            "Device_Asset_Tag":device.Device_Asset_Tag,
            "Device_Description":device.Device_Description,
            "type_of_device":device.type_of_device,

            "Unit_Location":device.Unit_Location,
            "Device_Information":device.Device_Information,

            "network_device_category":device.network_device_category,
            "network_sub_category":device.network_sub_category,
            "network_number_of_ports":device.network_number_of_ports,
            "network_uplink_ports_wan":device.network_uplink_ports_wan,
            "network_connection_type_fibre":device.network_connection_type_fibre,
            "network_connection_type_ehthernet":device.network_connection_type_ehthernet,
            "network_connection_type_both":device.network_connection_type_both,

            "security_device_category":device.security_device_category,
            "security_number_of_ports_lan":device.security_number_of_ports_lan,
            "security_network_uplink_ports_wan":device.security_network_uplink_ports_wan,
            "security_connection_type_fibre":device.security_connection_type_fibre,
            "security_connection_type_ehthernet":device.security_connection_type_ehthernet,
            "security_connection_type_both":device.security_connection_type_both,

            "patch_position":device.patch_position,
            "patch_category_type_inter":device.patch_category_type_inter,
            # patch_category_type_cross:device.
            # patch_category_type_isp:device.
            # patch_category_type_other:device.
            # path_number_of_ports:device.

            "server_number_of_ports":device.server_number_of_ports,
            "server_type_fibre":device.server_type_fibre,
            "server_type_ehthernet":device.server_type_ehthernet,
            "server_type_both":device.server_type_both,

            "chassis_number_of_blades":device.chassis_number_of_blades,
            "chassis_total_blades_slots":device.chassis_total_blades_slots,
            "chassis_type_fibre":device.chassis_type_fibre,
            "chassis_type_ehthernet":device.chassis_type_ehthernet,
            "chassis_type_both":device.chassis_type_both,

            "load_number_of_ports":device.load_number_of_ports,
            "load_uplink_ports_wan":device.load_uplink_ports_wan,
            "load_type_fibre":device.load_type_fibre,
            "load_type_ehthernet":device.load_type_ehthernet,
            # load_type_both:device.

            "storage_number_of_controllers":device.storage_number_of_controllers,
            "storage_number_of_disks":device.storage_number_of_disks,
            "storage_capicity_range":device.storage_capicity_range,
            "storage_capicity_input":device.storage_capicity_input,
            "storage_type_fibre":device.storage_type_fibre,
            "storage_type_ehthernet":device.storage_type_ehthernet,
            "storage_type_both":device.storage_type_both,


            "tapelib_number_of_magazine":device.tapelib_number_of_magazine,
            "tapelib_number_io_station":device.tapelib_number_io_station,
            "tapelib_type":device.tapelib_type,
            "tapelib_number_tape_capacity":device.tapelib_number_tape_capacity,
            "tapelib_storage_capacity":device.tapelib_storage_capacity,
            "tapelib_space_occupied":device.tapelib_space_occupied,

            "pdu_category":device.pdu_category,
            "pdu_number_of_power_ports":device.pdu_number_of_power_ports,
            "pdu_type":device.pdu_type,
            "pdu_position":device.pdu_position,

            "ups_max_loads":device.ups_max_loads,
            "ups_number_of_power_ports":device.ups_number_of_power_ports,

            "cctv":device.cctv_url,

            "patchtag":device.patchtag,
            "patchlist":device.patchlist,
            "patchcross":device.patchcross,
            "patchuplonks":device.patchuplonks,
            "patchswitch":device.patchswitch,
            "patchrouter":device.patchrouter,
            "patch_color":device.patch_color,
            "patchtag1":device.patchtag1,
            "patchlist1":device.patchlist1,
            "patchcross1":device.patchcross1,
            "patchuplonks1":device.patchuplonks1,
            "patchswitch1":device.patchswitch1,
            "patchrouter1":device.patchrouter1,
            "patch_color_two":device.patch_color_two,
            "patchtag2":device.patchtag2,
            "patchlist2":device.patchlist2,
            "patchcross2":device.patchcross2,
            "patchuplonks2":device.patchuplonks2,
            "patchswitch2":device.patchswitch2,
            "patchrouter2":device.patchrouter2,
            "patch_color_three":device.patch_color_three,

            "IP_Address_col1":device.IP_Address_col1,
            "IP_Address_col2":device.IP_Address_col2,
            "IP_Address_col3":device.IP_Address_col3,
            "IP_Address_col4":device.IP_Address_col4,
            "Special_Notes":device.Special_Notes,

            "deviceMake":device.deviceMake,
            "deviceModel":device.deviceModel,
            "installDate":device.installDate,
            "expiryDate":device.expiryDate,
            "deviceOwner":device.deviceOwner,
            "ownerDesc":device.ownerDesc,
            "deviceWatt":device.deviceWatt,
            "deviceSupplies":device.deviceSupplies,
            "deviceConn":device.deviceConn,   
        }, status=200)

def datacenter_page(request, id):
    nf = Notification()
    try:
        # totalDevice=[]
        datacenter = addDataCenter.objects.get(id=id)
        rows = addDataCenterRow.objects.filter(data_center=datacenter)
        racks = AddDataCenterRackcabinet.objects.filter(datacenter=datacenter, is_delete=False)
        device = AddDevice.objects.filter(datacenter=datacenter)
        total=device.count()
        # for r in racks:
            # total_device=AddDevice.objects.filter(data_center_rack=r)
            # totalDevice.append(total_device.count) 

        # device = AddDevice.objects.filter(datacenter=datacenter).values_list('Unit_Location', flat=True)
        # print(device) 
        return render(request, "dashboard/dc.html", {'datacenter':datacenter, 'datacenterrows':rows, 'datacenterracks':racks, 'device':device,'total':total})
        # return HttpResponse("Open Datacenter "+str(id))
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

def delete_rack(request, id):
    nf = Notification()
    try:
        goback = request.GET.get("return")
        racks = AddDataCenterRackcabinet.objects.get(id=id)
        racks.is_delete = True
        racks.save()
        return redirect('datacenter',goback)
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

def edit_rack(request, id):
    nf = Notification()
    try:
        data_center = addDataCenter.objects.all()
        racks = AddDataCenterRackcabinet.objects.get(id=id)
        msg = ""
        if request.method == "POST":
            data = {key:value.strip() for key, value in request.POST.items()}
            # print(data)
            racks.datacenter = addDataCenter.objects.get(id=data["datacenter"])
            racks.date_center_row = addDataCenterRow.objects.get(id=data["rack_row"])
            racks.Rack_Label_Tag = data["rack_tag"]
            racks.RowColor = data["row_color_form3"]
            racks.Rack_Type = data["rack_type3"]
            racks.Rack_Type_Information = data.get("customised_rt_information","42") 
            racks.Owner = data["your_role"]
            racks.Patch_Panels_Ethernet = data.get("ethernet","false")
            racks.Patch_Panels_Fiber = data.get("fibre","false")
            racks.Patch_Panels_Other = data.get("other","false")
            racks.Patch = data.get("patch_panels_information","")
            racks.Special_Notes = data["special_notes"]
            racks.save()
            msg = "New Data Center Rack (Cabinet) Added Successfully"
        return render(request, 'dashboard/edit_rack_form.html', {'racks':racks,'datacenter':data_center,'msg':msg})
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })
    
def rack_page(request, id):
    nf = Notification()
    try:
        rack = AddDataCenterRackcabinet.objects.get(id=id)
        device = AddDevice.objects.filter(data_center_rack=rack.id)
        total_device=device
        # print(device)
        frontDevice = device.filter(pdu_position="front").order_by("-Unit_Location")
        rearDevice = device.filter(pdu_position="rear").order_by("-Unit_Location")
        # print(frontDevice)
        all_device = AddDevice.objects.all()
        details = DeviceDetails.objects.all()
        patchpanel = PatchPanel.objects.filter(rack=rack)
        patchport = PatchPanelPort.objects.all()
        # details = DeviceDetails.objects.filter(device__data_center_rack=rack.id)
        alphabets = {'50':'BX','49':'BW','48':'BV','47':'BU','46':'BT','45':'BS','44':'BR','43':'BQ','42':'BP','41':'BO','40':'BN','39':'BM','38':'BL','37':'BK','36':'BJ','35':'BI','34':'BH','33':'BG','32':'BF','31':'BE','30':'BD','29':'BC','28':'BB','27':'BA','26':'AZ','25':'AY','24':'AX','23':'AW','22':'AV','21':'AU','20':'AT','19':'AS','18':'AR','17':'AQ','16':'AP','15':'AO','14':'AN','13':'AM','12':'AL','11':'AK','10':'AJ','9':'AI','8':'AH','7':'AG','6':'AF','5':'AE','4':'AD','3':'AC','2':'AB','1':'AA'}
        # print(rack, device)
        if request.method == "GET": 
            return render(request, "dashboard/rackinfo.html", {'datacenterracks':rack, 'device':device, 'alphabets':alphabets, 'details':details,'all_device':all_device,'patchpanel':patchpanel,'patchport':patchport,'frontDevice':frontDevice,'rearDevice':rearDevice,})
        if request.method == "POST":
            # if request.POST.get("form_type") == 'formOne': 
            #     data = {key:value.strip() for key, value in request.POST.items()}
            #     print(data)
            #     add, created = DeviceDetails.objects.update_or_create(
            #         device=AddDevice.objects.get(id=data["incoming_device"]),defaults={'patchpanel_incoming':data["incoming_port"],'patchpanel_outgoing':0}
            #     )
            #     # add.save()
            #     msg = "Patch Port (Incoming) added"
            #     return render(request, 'dashboard/rackinfo.html',{
            #             'msg' : msg,'datacenterracks':rack, 'device':device, 'alphabets':alphabets, 'details':details,'all_device':all_device,
            #         })
            # if request.POST.get("form_type") == 'formOne': 
            #     data = {key:value.strip() for key, value in request.POST.items()}
            #     print(data)
            #     # add, created = DeviceDetails.objects.update_or_create(
            #     #     device=AddDevice.objects.get(id=data["incoming_device"]),defaults={'patchpanel_incoming':data["incoming_port"],'patchpanel_outgoing':0}
            #     # )
            #     add = PatchPanel(
            #         rack = rack,
            #         name = data["patchname"],
            #         incoming = data.get("incoming",False),
            #         outgoing = data.get("outgoing",False)
            #     )
            #     add.save()
            #     msg = "Patch Panel added"
            #     return render(request, 'dashboard/rackinfo.html',{
            #             'msg' : msg,'datacenterracks':rack, 'device':device, 'alphabets':alphabets, 'details':details,'all_device':all_device,'patchpanel':patchpanel,'patchport':patchport,
            #         })

            if request.POST.get("form_type") == 'formTwo': 
                data = {key:value.strip() for key, value in request.POST.items()}
                # print(data)
                # add, created = DeviceDetails.objects.update_or_create(
                #     device=AddDevice.objects.get(id=data["outgoing_device"]),defaults={'patchpanel_outgoing':data["outgoing_port"],'patchpanel_incoming':0}
                # )
                add = PatchPanelPort(
                    patchpanel = AddDevice.objects.get(id=data["patch"]),
                    device = AddDevice.objects.get(id=data["device"]),
                    port = data["port"],
                    information = "nothing",
                    in_out = data["inOut"]
                )
                add.save()
                msg = "Patch Port added"
                return render(request, 'dashboard/rackinfo.html',{
                        'msg' : msg,'datacenterracks':rack, 'device':device, 'alphabets':alphabets, 'details':details,'all_device':all_device,'patchpanel':patchpanel,'patchport':patchport,'frontDevice':frontDevice,'rearDevice':rearDevice,
                    })

            if request.POST.get("form_type") == 'formThree': 
                data = {key:value.strip() for key, value in request.POST.items()}
                value = int(data["patch"])
                # print(value)
                return render(request, 'dashboard/rackinfo.html',{
                        'datacenterracks':rack, 'device':device, 'alphabets':alphabets, 'details':details,'all_device':all_device,'patchpanel':patchpanel,'patchport':patchport,'value':value,'frontDevice':frontDevice,'rearDevice':rearDevice,
                    })
        # return HttpResponse("Open Datacenter "+str(id))
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })
        
def patchPanelForm(request):
    patch = PatchPanel.objects.all() 
    if request.method == 'POST':
        form = PatchPanelForm(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.save()
        return render(request, 'dashboard/patchpanelform.html',{'form' : form,'patch':patch})
    else:
        form = PatchPanelForm()
    return render(request, 'dashboard/patchpanelform.html',{'form' : form,'patch':patch})

def patchPanelShow(request, id):
    patch = PatchPanel.objects.get(id=id)
    return render(request, 'dashboard/patchpanel.html',{'patch':patch})
    
def patch_panel(request):
    nf = Notification()
    if request.POST.get("form_type") == 'formOne':
        try:
            data = {key:value.strip() for key, value in request.POST.items()}
            # print(data)
            add, created = DeviceDetails.objects.update_or_create(
                device=AddDevice.objects.get(id=data["incoming_device"]),defaults={'patchpanel_incoming':data["incoming_port"],'patchpanel_outgoing':0}
            )
            # add.save()
            msg = "New Device Added Successfully"
            return render(request, 'dashboard/rackinfo.html',{
                    'msg' : msg,'datacenterracks':rack, 'device':device, 'alphabets':alphabets, 'details':details,'all_device':all_device,
                })
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })
    if request.POST.get("form_type") == 'formTwo': 
        try:
            data = {key:value.strip() for key, value in request.POST.items()}
            # print(data)
            add = DeviceDetails(
                device = AddDevice.objects.get(id=data["outgoing_device"]),
                patchpanel_incoming = 0,
                patchpanel_outgoing = int(data["outgoing_port"]),
                )
            add.save()
            msg = "New Device Added Successfully"
            return render(request, 'dashboard/rackinfo.html',{
                    'msg' : msg,
                })
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

def device_page(request, id):
    nf = Notification()
    try:
        device = AddDevice.objects.get(id=id)
        return render(request, "dashboard/deviceinfo.html", {'device':device})

        # return HttpResponse("Open Datacenter "+str(id))
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })
#POWER ON or OFF
def change_device_status_right(request):
    id = request.POST.get("id")
    device = AddDevice.objects.get(id=id)
    if device.power_right:
        device.power_right=False
        device.save()
        # return redirect('/show/user', {'allusers': User.objects.all()})
        return JsonResponse({"msg":"Right Device Off",}, status=200)
    else:
        device.power_right=True
        device.save()
        return JsonResponse({"msg":"Right Device On",}, status=200)
def change_device_status_left(request):
    id = request.POST.get("id")
    device = AddDevice.objects.get(id=id)
    if device.power_left:
        device.power_left=False
        device.save()
        # return redirect('/show/user', {'allusers': User.objects.all()})
        return JsonResponse({"msg":"Left Device Off",}, status=200)
    else:
        device.power_left=True
        device.save()
        return JsonResponse({"msg":"Left Device On",}, status=200)

def send_device_via_mail(request):
    nf = Notification()
    try:
        if request.method == "POST":
            id = request.POST.get("id")
            device = AddDevice.objects.get(id=id)
            subject = str(device.id) + " Information"
            html_message = render_to_string('email/deviceinfo.html', {'device': device})
            plain_message = strip_tags(html_message)
            email_from = settings.EMAIL_HOST_USER
            email_to = [email_from,]
            send_mail(subject=subject,message=plain_message, html_message=html_message, from_email=email_from, recipient_list=email_to)
            return JsonResponse({"msg":"Mail Sent",}, status=200)

            # return HttpResponse("Open Datacenter "+str(id))
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

class ValidateIP(View):
    def post(self, request):
        # data = request.GET["data"]
        # print(data)
        # return JsonResponse({"port1":request.POST.get("ip_address41"),})
        ip_addr = request.POST.get("ip_address41") + "." + request.POST.get("ip_address42") + "." + request.POST.get("ip_address43") + "." + request.POST.get("ip_address44")
        ip_port = request.POST.get("ip_port")
        # print("PORT:", ip_port)
        afvf = views_functions.AssetsFormsVF()
        port, time = afvf.hostscan(ip_addr, int(ip_port))
        return JsonResponse({
            "port":port,
            "time":time,
        }, status=200)

    # def get(self, request):
        # ip_addr = request.POST["ip_address41"] + "." + request.POST["ip_address42"] + "." + request.POST["ip_address43"] + "." + request.POST["ip_address44"]
        # return HttpResponse(str(ip_addr))
        # afvf = views_functions.AssetsFormsVF()
        # port, time = afvf.hostscan(ip_addr)
        # return JsonResponse({
        #     "port":port,
        #     "time":time,
        # }, status=200)

    
class Login(View):
    def get(self, request):
        msg = request.GET.get('msg','')
        return render(request, "dashboard/login.html",{'msg':msg})

    def post(self, request):
        try:
            nf = Notification()
            data = {key:value.strip() for key, value in request.POST.items() if (key != "csrfmiddlewaretoken")}
            user_fields = User.objects.filter(email=data['yourEmail'])
            # print(data['yourEmail'], data['password'])
            if len(user_fields) == 1:
                user = authenticate(request, username=User.objects.get(email=data['yourEmail']).username, password=data['password'])
                # print(user)
        
                if user is not None:
                    login(request, user)
                    # request.session['uid'] = email=data['yourEmail']
                    message = nf.show_result(result="Success", helping_text="You are now logged in.", title="Logged In", button_text="Visit Last Page", button_url="/") 
                    # apart from these add any show_results you want in any other variable names
                    return render(request, 'dashboard/message_page.html',{
                        'message' : message,
                    })
                else:
                    message = nf.show_result(result="Can't Login", helping_text="HINT::Please check the email id you entered and password matches!", title="Login Failure ", button_text="Visit Last Page", button_url="/")
                
                    # apart from these add any show_results you want in any other variable names
                    return render(request, 'dashboard/message_page.html',{
                        'message' : message,
                    })
                
            else:
                message = nf.show_result(result="Can't Login", helping_text="HINT:No Such User found!", title="Login Failure ", button_text="Visit Last Page", button_url="{% url 'home_page' %}")
                
                # apart from these add any show_results you want in any other variable names
                return render(request, 'dashboard/message_page.html',{
                    'message' : message,
                })
        except Exception as e:
                message = nf.show_result(result="Error", helping_text=str(e), title="Login Failure ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                # HINT:SYSTEM FAULT! Please Try login after hard refreshing the page.
                # apart from these add any show_results you want in any other variable names
                return render(request, 'dashboard/message_page.html',{
                    'message' : message,
                })
    
class ResetPassword(View):
    def get(self, request):
        return render(request, 'dashboard/reset_password.html')

    def post(self, request):
        nf = Notification()
        try:
            data = {key:value.strip() for key, value in request.POST.items() if key != "csrfmiddlewaretoken" }
        
            if data["yourEmail"] == "" and "@" not in data["yourEmail"] and "." not in data["yourEmail"] and data["password"] == "" and data["masterpassword"] == "":
                message = nf.show_result(result="Can't Reset Password", helping_text="HINT::Please provide all the details asked in the Password Reset form!! ", title="User Password Reset Failure ", button_text="Visit Last Page", button_url="/")
                
                # apart from these add any show_results you want in any other variable names
                return render(request, 'dashboard/message_page.html',{
                    'message' : message,
                })

            
            if User.objects.filter(email=data["yourEmail"]).count():
                user = User.objects.get(email=data["yourEmail"])
                if UserProfile.objects.filter(user=user).count():
                    curr_mp = UserProfile.objects.get(user=user).master_password
                    if (check_password(data["masterpassword"], curr_mp)):
                        user.password = data['password']
                        user.save()               
                        message = nf.show_result(result="Password Successfully Changed", helping_text="HINT::Thank You for registering with us. Now, wait untill your account is approved and activated by the Admin!! ", title="Password Changed", button_text="Visit Last Page", button_url="/")
                        # apart from these add any show_results you want in any other variable names
                        return render(request, 'dashboard/message_page.html',{
                            'message' : message,
                        })
                    
                    else:
                        message = nf.show_result(result="Can't Reset Password", helping_text="HINT::Master Password don't match", title="Password Reset Failure ", button_text="Visit Last Page", button_url="/")
                        
                        # apart from these add any show_results you want in any other variable names
                        return render(request, 'dashboard/message_page.html',{
                            'message' : message,
                        })

                else:
                    message = nf.show_result(result="Can't Reset Password", helping_text="HINT::User Exists but I cannot find your profile!!", title="Password Reset Failure ", button_text="Visit Last Page", button_url="/")
                    
                    # apart from these add any show_results you want in any other variable names
                    return render(request, 'dashboard/message_page.html',{
                        'message' : message,
                    })
            else:
                message = nf.show_result(result="Can't Reset Password", helping_text="HINT::Email Id does not exist", title="Password Reset Failure ", button_text="Visit Last Page", button_url="/")
                
                # apart from these add any show_results you want in any other variable names
                return render(request, 'dashboard/message_page.html',{
                    'message' : message,
                })
                
        except Exception as err:
            message = nf.show_result(result="Can't Change Password", helping_text="HINT::Server error occured!! Error: {}".format(err), title="Password Reset Failure ", button_text="Visit Last Page", button_url="/")
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })

@login_required()
def showUser(request):
    nf = Notification()
    try:
        all_users= User.objects.all()
        context= {'allusers': all_users}
        return render(request, 'dashboard/show_user.html', context)
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

def changeStatus(request, id):
    # user = User.objects.filter(id=id).update(is_active=True)
    try:
        user = User.objects.get(id=id)
        if user.is_active:
            user.is_active=False
            user.save()
            return redirect('/show/user', {'allusers': User.objects.all()})
        else:
            user.is_active=True
            user.save()
            return redirect('/show/user', {'allusers': User.objects.all()})
        # return render(request, 'dashboard/show_user.html')
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })




# @login_required()
class ProfileUpdate(View):
    login_required()
    def get(self, request):
        return render(request, 'dashboard/profile-update.html')

    def post(self, request):
        try:
            nf = Notification()
            data = {key:value.strip() for key, value in request.POST.items()}
            img = request.FILES.get('input-img')
            User.objects.filter(username=request.user.username).update(first_name = data["input-f_name"], last_name = data["input-l_name"])
            user_info = UserProfile.objects.get(user=request.user)
            user_info.bio = data["input-bio"]
            if img:
                user_info.pic = img
            user_info.save()

            message = nf.show_result(result="Profile Updated!!!", helping_text="HINT::Please regularly update your information! ", title="Profile Updated Successfully", button_text="Visit Last Page", button_url="/")
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })

            
        except Exception as err:
            message = nf.show_result(result="Can't Update Profile", helping_text="HINT::SERVER ERROR! Error:{} ".format(err), title="Profile Update Failure ", button_text="Visit Last Page", button_url="/")
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })



class Registration(View):
    def get(self, request):
        return render(request, 'dashboard/registration.html')
    
    def post(self, request):
        nf = Notification()
        try:
            data = {key:value.strip() for key, value in request.POST.items() if key != "csrfmiddlewaretoken" }
        
            if data["username"] == "" and data["yourEmail"] == "" and "@" not in data["yourEmail"] and "." not in data["yourEmail"] and data["password"] == "":
                message = nf.show_result(result="Can't Register", helping_text="HINT::Please provide all the details asked in the registrations form!! ", title="User Registration Failure ", button_text="Visit Last Page", button_url="/")
                
                # apart from these add any show_results you want in any other variable names
                return render(request, 'dashboard/message_page.html',{
                    'message' : message,
                })

            
            if User.objects.filter(Q(email=data["yourEmail"]) | Q(username=data["username"])).count():
                message = nf.show_result(result="Can't Register", helping_text="HINT::Email Id and Username provided are already registered with us!! If you can't login then please contact the admin(Your account may have not been activated yet)", title="User Registration Failure ", button_text="Visit Last Page", button_url="/")
                
                # apart from these add any show_results you want in any other variable names
                return render(request, 'dashboard/message_page.html',{
                    'message' : message,
                })
            
            else:
            
                user = User()
                user.username = data['username']
                user.email = data['yourEmail']
                # user.password = data['password']
                user.set_password(data['password'])
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.is_active = False
                
                if data['role'] == 'staff':
                    user.is_staff = True
                    user.is_superuser = False
                else:
                    user.is_staff = False
                    user.is_superuser = True
                    

                user.save()

                profile = UserProfile()
                profile.user = user
                profile.master_password = data['master_password']
                profile.save()
            
                message = nf.show_result(result="Registration Successfull", helping_text="HINT::Thank You for registering with us. Now, wait untill your account is approved and activated by the Admin!! ", title="User Registered", button_text="Visit Last Page", button_url="/")
                
                # apart from these add any show_results you want in any other variable names
                return render(request, 'dashboard/message_page.html',{
                    'message' : message,
                })
                
        except Exception as err:
            message = nf.show_result(result="Can't Register", helping_text="HINT::Server error occured!! Error: {}".format(err), title="User Registration Failure ", button_text="Visit Last Page", button_url="/")
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })


def importEx(request):
    app_models = [model.__name__ for model in apps.get_models()][:-5]
    msg = ""
    if request.method == 'POST':
        nf = Notification()
        try:
            file_format = request.POST['file-format']
            modelName = request.POST['modelName']
            if modelName == 'AnsibleOutput':
                resource = AnsibleOutputResource()
            elif modelName == 'Product':
                resource = ProductResource()
            elif modelName == 'CameraMonitor':
                resource = CameraMonitorResource()
            elif modelName == 'WebsiteLinks':
                resource = WebsiteLinksResource()
            elif modelName == 'DC':
                resource = DCResource()
            elif modelName == 'DataCenterCountry':
                resource = DataCenterCountryResource()
            elif modelName == 'DataCenterState':
                resource = DataCenterStateResource()
            elif modelName == 'DeviceEquipement':
                resource = DeviceEquipementResource()
            elif modelName == 'UserProfile':
                resource = UserProfileResource()
            elif modelName == 'Person':
                resource = PersonResource()
            elif modelName == 'Post':
                resource = PostResource()
            elif modelName == 'Employee':
                resource = EmployeeResource()
            elif modelName == 'PagePermissionForGroup':
                resource = PagePermissionForGroupResource()
            elif modelName == 'addDataCenter':
                resource = addDataCenterResource()
            elif modelName == 'addDataCenterRow':
                resource = addDataCenterRowResource()
            elif modelName == 'AddDataCenterRackcabinet':
                resource = AddDataCenterRackcabinetResource()
            elif modelName == 'AddDevice':
                resource = AddDeviceResource()
            elif modelName == 'DeviceTemplate':
                resource = DeviceTemplateResource()
            elif modelName == 'DeviceDetails':
                resource = DeviceDetailsResource()
            elif modelName == 'RR':
                resource = RRResource()
            elif modelName == 'Notif':
                resource = NotifResource()
            elif modelName == 'PatchPanel':
                resource = PatchPanelResource()
            elif modelName == 'PatchPanelPort':
                resource = PatchPanelPortResource()
            elif modelName == 'Uptime':
                resource = UptimeResource()
            elif modelName == 'ProcessUtil':
                resource = ProcessUtilResource()
            elif modelName == 'Browser':
                resource = BrowserResource()
            elif modelName == 'Series':
                resource = SeriesResource()
            elif modelName == 'Test1':
                resource = Test1Resource()
            elif modelName == 'ServerData':
                resource = ServerDataResource()
            elif modelName == 'DeviceCapibility':
                resource = DeviceCapibilityResource()

            elif modelName == 'LogEntry':
                resource = LogEntryResource()
            elif modelName == 'ContentType':
                resource = ContentTypeResource()
            elif modelName == 'User':
                resource = UserResource()
            elif modelName == 'Permission':
                resource = PermissionResource()
            elif modelName == 'Group':
                resource = GroupResource()
            elif modelName == 'Session':
                resource = SessionResource()
            else:
                pass
            dataset = Dataset()
            data = request.FILES['importData']

            if file_format == 'CSV':
                imported_data = dataset.load(data.read().decode('utf-8'),format='csv')
                res = resource.import_data(dataset, dry_run=True, raise_errors=True)                                                                 
            elif file_format == 'JSON':
                imported_data = dataset.load(data.read().decode('utf-8'),format='json')
                # Testing data import
                res = resource.import_data(dataset, dry_run=True, raise_errors=True) 

            if not res.has_errors():
                # Import now
                resource.import_data(dataset, dry_run=False)
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

    return render(request, 'dashboard/import.html',{'AllModels':app_models, 'msg':msg})



def exportData(request):
    app_models = [model.__name__ for model in apps.get_models()][:-5]
    if request.method == 'POST':
        nf = Notification()
        try:
            # Get selected option from form
            modelName = request.POST['modelName']
            file_format = request.POST['file-format']
            if modelName == 'AnsibleOutput':
                resource = AnsibleOutputResource()
            elif modelName == 'Product':
                resource = ProductResource()
            elif modelName == 'CameraMonitor':
                resource = CameraMonitorResource()
            elif modelName == 'WebsiteLinks':
                resource = WebsiteLinksResource()
            elif modelName == 'DC':
                resource = DCResource()
            elif modelName == 'DataCenterCountry':
                resource = DataCenterCountryResource()
            elif modelName == 'DataCenterState':
                resource = DataCenterStateResource()
            elif modelName == 'DeviceEquipement':
                resource = DeviceEquipementResource()
            elif modelName == 'UserProfile':
                resource = UserProfileResource()
            elif modelName == 'Person':
                resource = PersonResource()
            elif modelName == 'Post':
                resource = PostResource()
            elif modelName == 'Employee':
                resource = EmployeeResource()
            elif modelName == 'PagePermissionForGroup':
                resource = PagePermissionForGroupResource()
            elif modelName == 'addDataCenter':
                resource = addDataCenterResource()
            elif modelName == 'addDataCenterRow':
                resource = addDataCenterRowResource()
            elif modelName == 'AddDataCenterRackcabinet':
                resource = AddDataCenterRackcabinetResource()
            elif modelName == 'AddDevice':
                resource = AddDeviceResource()
            elif modelName == 'DeviceTemplate':
                resource = DeviceTemplateResource()
            elif modelName == 'DeviceDetails':
                resource = DeviceDetailsResource()
            elif modelName == 'RR':
                resource = RRResource()
            elif modelName == 'Notif':
                resource = NotifResource()
            elif modelName == 'PatchPanel':
                resource = PatchPanelResource()
            elif modelName == 'PatchPanelPort':
                resource = PatchPanelPortResource()
            elif modelName == 'Uptime':
                resource = UptimeResource()
            elif modelName == 'ProcessUtil':
                resource = ProcessUtilResource()
            elif modelName == 'Browser':
                resource = BrowserResource()
            elif modelName == 'Series':
                resource = SeriesResource()
            elif modelName == 'Test1':
                resource = Test1Resource()
            elif modelName == 'ServerData':
                resource = ServerDataResource()
            elif modelName == 'DeviceCapibility':
                resource = DeviceCapibilityResource()

            elif modelName == 'LogEntry':
                resource = LogEntryResource()
            elif modelName == 'ContentType':
                resource = ContentTypeResource()
            elif modelName == 'User':
                resource = UserResource()
            elif modelName == 'Permission':
                resource = PermissionResource()
            elif modelName == 'Group':
                resource = GroupResource()
            elif modelName == 'Session':
                resource = SessionResource()
            else:
                pass
            dataset = resource.export()
            if file_format == 'CSV':
                response = HttpResponse(dataset.csv, content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename="'+modelName+'.csv"'
                return response        
            elif file_format == 'JSON':
                response = HttpResponse(dataset.json, content_type='application/json')
                response['Content-Disposition'] = 'attachment; filename="'+modelName+'.json"'
                return response
            elif file_format == 'XLS (Excel)':
                response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = 'attachment; filename="'+modelName+'.xls"'
                return response   
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })
    else:
        pass# Returns a "list" of all models created
        # print(app_models)

    return render(request, 'dashboard/export.html',{'AllModels':app_models})


# class dataBrowser(View):
#     def get (self,request):
#         return render(request,'dashboard/db.html')


# @login_required()
class GP(View):
    login_required()
    def get(self,request):
        nf = Notification()
        try:
            user=User.objects.get(username=request.user)
            all_perm=user.get_all_permissions()
            perm_count=len(all_perm) 
            all_group=Group.objects.all()
            # all_page=PagePermissionForGroup.objects.all()
            return render(request,'dashboard/groups.html',{"all_perm":all_perm,"perm_count":perm_count,"all_group":all_group})
                # return HttpResponse("this ")
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

    def post(self, request):
        nf = Notification()
        try:
            user=User.objects.get(username=request.user)
            all_perm=user.get_all_permissions()
            perm_count=len(all_perm)
            all_group=Group.objects.all()
            # all_page=PagePermissionForGroup.objects.all()

            msg = ""

            data = {key:request.POST[key].strip() for key in request.POST if not key == "csrfmiddlewaretoken"}
            print(data)
            p = request.POST.getlist('permission')
            # page_data={key:request.POST[key].strip() for key in request.POST if not key =="csrfmiddlewaretoken"}
                
            if "creategroup" in data:
                if Group.objects.filter(name=data['creategroup']).count():
                    # return HttpResponse("group already taken please write another name")
                    return render(request,'dashboard/groups.html',{"all_perm":all_perm,"perm_count":perm_count,"all_group":all_group, 'msg':'group already taken please write another name'})
                    
                else:
                    groupname, created=Group.objects.get_or_create(name=data['creategroup'])
                    # return HttpResponse("group created successfully")
                    return render(request,'dashboard/groups.html',{"all_perm":all_perm,"perm_count":perm_count,"all_group":all_group, 'msg':'group created successfully'})
                
            if "groupname" in data:
                
                group_django = Group.objects.get(name=data['groupname'])
                perm_set = Permission.objects.values("codename","id")
                perm_ids = []

                for i in perm_set:
                    for perm in p:
                        if perm.split(".")[1] in i["codename"]:
                            perm_ids.append(i["id"])
                    
                group_django.permissions.set(perm_ids)
                # page_group = PagePermissionForGroup.objects.filter(name_of_page=data['pagename'])

                # updated = page_group.update(read_perm=data.get("read_perm",False),
                # write_perm=data.get("write_perm",False),delete_perm=data.get("delete_perm",False),
                # update_perm=data.get("update_perm",False),patch_perm=data.get("patch_perm",False),
                # all_perm=data.get("all_perm",False))

                # if updated:
                #     # return HttpResponse("Page Permissions are also set")
                #     return render(request,'dashboard/groups.html',{"all_perm":all_perm,"perm_count":perm_count,"all_group":all_group, 'msg':'Page Permissions are also set'})
                # # return HttpResponse("Only Models Permissions Set")
                return render(request,'dashboard/groups.html',{"all_perm":all_perm,"perm_count":perm_count,"all_group":all_group,'msg':'Permissions Set'})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })


def getUserPermission(request):
    all_group=Group.objects.all()
    if request.method == 'POST':
        nf = Notification()
        try:
            user_name = request.POST.get('user')
            a=Group.objects.get(name=user_name)
            a_all=a.permissions.all()
            return render(request, 'dashboard/test_badal.html', context={"a_all":a_all,"all_group":all_group})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })
    return render(request, 'dashboard/test_badal.html', context={'all_group':all_group})

def assignGroup(request):
    nf = Notification()
    if request.user.is_superuser:
        msg=""
        all_group=Group.objects.all()
        all_user=User.objects.all()
        if request.method == 'POST':
            group = request.POST.get('group')
            user = request.POST.get('user')
            get_group = Group.objects.get(name=group)
            get_group.user_set.add(user)
            msg = "successfully added"
        return render(request, 'dashboard/test_badal_p2.html', context={'all_group':all_group, 'all_user':all_user,'msg':msg})
    else:
        message = nf.show_result(result="You are not authorize to see this page", title="Failure ", button_text="Visit Last Page", button_url="/")
                
            # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })

def fun1(request):
    form = PagePermissionForGroupForm()
    msg=""
    if request.method == "POST":
        new_form = PagePermissionForGroupForm(request.POST)
        if new_form.is_valid():
            new_form.save()
            msg = "Successs"
    return render(request,'dashboard/test_badal_p3.html', context={'form':form, 'msg':msg})



def temp(request):
    return render(request, "dashboard/tempview.html")

def top(request):
    return render(request, "dashboard/topview.html")




@login_required()
def setting(request):
    return render(request,"dashboard/setting.html")


def rackInformation(request,id=id):
    if request.user.is_authenticated:
        user = User.objects.filter(email=request.user.email)
        for data in user:
            html_string = "<table><tr><td id=td1>1</td></tr><tr></tr></table>"
            import lxml.html as LH
            root = LH.fromstring(html_string)
            for el in root.iter('td1'):
                el.attrib['rowspan'] = '2'

            # print(LH.tostring(root, pretty_print=True))

            device_count = DeviceEquipement.objects.count()
            device_pack = DeviceEquipement.objects.all()
            all_devices_list = []

            device_a = device_pack[0]
            device_b = device_pack[1]
            device_c = device_pack[3]
            device_d = device_pack[4]
            device_e = device_pack[5]

            # print(device_count)

            # df = pd.DataFrame(data=[[1, 2], [3, 4]])
            # df_html = df.to_html()

            context = {
                'device_count': device_count, 'device_pack': device_pack, 'device_a': device_a, 'device_b': device_b,
                'device_c': device_c, 'device_d': device_d, 'device_e': device_e,"udata": data, "date": datetime.now,
            }
            return render(request, 'dashboard/rack_information.html', context)
    else:
        return redirect('home_user')

def dc2(request):
    if request.user.is_authenticated:
        device_count = DeviceEquipement.objects.count()
        # device_name = DeviceEquipement.objects.all()
        data_centers_count = DC.objects.count()
        user = User.objects.filter(email=request.user.email)
        for data in user:
            
            import plotly.express as px
            df = px.data.tips()
            pie_fig = px.pie(df, values='tip', names='day', color_discrete_sequence=px.colors.sequential.RdBu,
                                width=300,
                                height=300, )
            config = {'displayModeBar': False}
            pie_fig_plot = plotly.offline.plot(pie_fig, output_type='div', config=config)


            device_pack = DeviceEquipement.objects.all()

            rack_assest_all = RR.objects.all().filter(RackRow='A')
            device_list = []

            device_a = device_pack[0]
            device_b = device_pack[1]
            device_c = device_pack[3]
            device_d = device_pack[4]
            device_e = device_pack[5]

            # print(device_e)

            context = {
                'device_count': device_count,'data_centers_count':data_centers_count, 'device_name': device_pack, 'device_a': device_a, 'device_b': device_b,
                'device_c': device_c, 'device_d': device_d, 'device_e': device_e,"udata": data, "date": datetime.now,
            }

            return render(request, 'dashboard/datacenter2.html', context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')
def dc3(request):
    if request.user.is_authenticated:
        device_count = DeviceEquipement.objects.count()
        # device_name = DeviceEquipement.objects.all()
        data_centers_count = DC.objects.count()
        user = User.objects.filter(email=request.user.email)
        for data in user:
            
            import plotly.express as px
            df = px.data.tips()
            pie_fig = px.pie(df, values='tip', names='day', color_discrete_sequence=px.colors.sequential.RdBu,
                                width=300,
                                height=300, )
            config = {'displayModeBar': False}
            pie_fig_plot = plotly.offline.plot(pie_fig, output_type='div', config=config)


            device_pack = DeviceEquipement.objects.all()

            rack_assest_all = RR.objects.all().filter(RackRow='A')
            device_list = []

            device_a = device_pack[0]
            device_b = device_pack[1]
            device_c = device_pack[3]
            device_d = device_pack[4]
            device_e = device_pack[5]

            # print(device_e)

            context = {
                'device_count': device_count,'data_centers_count':data_centers_count, 'device_name': device_pack, 'device_a': device_a, 'device_b': device_b,
                'device_c': device_c, 'device_d': device_d, 'device_e': device_e,"udata": data, "date": datetime.now,
            }

            return render(request, 'dashboard/datacenter3.html', context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')
def dc4(request):
    if request.user.is_authenticated:
        device_count = DeviceEquipement.objects.count()
        # device_name = DeviceEquipement.objects.all()
        data_centers_count = DC.objects.count()
        user = User.objects.filter(email=request.user.email)
        for data in user:
            
            import plotly.express as px
            df = px.data.tips()
            pie_fig = px.pie(df, values='tip', names='day', color_discrete_sequence=px.colors.sequential.RdBu,
                                width=300,
                                height=300, )
            config = {'displayModeBar': False}
            pie_fig_plot = plotly.offline.plot(pie_fig, output_type='div', config=config)


            device_pack = DeviceEquipement.objects.all()

            rack_assest_all = RR.objects.all().filter(RackRow='A')
            device_list = []

            device_a = device_pack[0]
            device_b = device_pack[1]
            device_c = device_pack[3]
            device_d = device_pack[4]
            device_e = device_pack[5]

            # print(device_e)

            context = {
                'device_count': device_count,'data_centers_count':data_centers_count, 'device_name': device_pack, 'device_a': device_a, 'device_b': device_b,
                'device_c': device_c, 'device_d': device_d, 'device_e': device_e,"udata": data, "date": datetime.now,
            }

            return render(request, 'dashboard/datacenter4.html', context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')
def dc5(request):
    if request.user.is_authenticated:
        device_count = DeviceEquipement.objects.count()
        # device_name = DeviceEquipement.objects.all()
        data_centers_count = DC.objects.count()
        user = User.objects.filter(email=request.user.email)
        for data in user:
            
            import plotly.express as px
            df = px.data.tips()
            pie_fig = px.pie(df, values='tip', names='day', color_discrete_sequence=px.colors.sequential.RdBu,
                                width=300,
                                height=300, )
            config = {'displayModeBar': False}
            pie_fig_plot = plotly.offline.plot(pie_fig, output_type='div', config=config)


            device_pack = DeviceEquipement.objects.all()

            rack_assest_all = RR.objects.all().filter(RackRow='A')
            device_list = []

            device_a = device_pack[0]
            device_b = device_pack[1]
            device_c = device_pack[3]
            device_d = device_pack[4]
            device_e = device_pack[5]

            # print(device_e)

            context = {
                'device_count': device_count,'data_centers_count':data_centers_count, 'device_name': device_pack, 'device_a': device_a, 'device_b': device_b,
                'device_c': device_c, 'device_d': device_d, 'device_e': device_e,"udata": data, "date": datetime.now,
            }

            return render(request, 'dashboard/datacenter5.html', context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')

@login_required()
def newDataCenter(request):
    if request.user.is_authenticated:
        device_count = DeviceEquipement.objects.count()
        # device_name = DeviceEquipement.objects.all()
        data_centers_count = DC.objects.count()
        user = User.objects.filter(email=request.user.email)
        for data in user:
            
            import plotly.express as px
            df = px.data.tips()
            pie_fig = px.pie(df, values='tip', names='day', color_discrete_sequence=px.colors.sequential.RdBu,
                                width=300,
                                height=300, )
            config = {'displayModeBar': False}
            pie_fig_plot = plotly.offline.plot(pie_fig, output_type='div', config=config)


            device_pack = DeviceEquipement.objects.all()

            rack_assest_all = RR.objects.all().filter(RackRow='A')
            device_list = []

            device_a = device_pack[0]
            device_b = device_pack[1]
            device_c = device_pack[3]
            device_d = device_pack[4]
            device_e = device_pack[5]

            # print(device_e)

            context = {
                'device_count': device_count,'data_centers_count':data_centers_count, 'device_name': device_pack, 'device_a': device_a, 'device_b': device_b,
                'device_c': device_c, 'device_d': device_d, 'device_e': device_e,"udata": data, "date": datetime.now,
            }

            return render(request, 'dashboard/data_center.html', context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')

    else:
        return redirect('login_page')
@login_required()
def all_notifications(request):
    data = Notif.objects.filter(user=request.user, is_delete=False).order_by("-date")
    return render(request, 'dashboard/notifications.html', {'data':data})

@login_required()
def notification_update(request,id):
    id = Notif.objects.get(id=id)
    id.is_read=True
    id.save()
    return redirect('home_page')
    # if request.method == 'GET':
    #     id = request.GET['id']
    #     n = Notif.objects.get(id=id)
    #     n.is_read = True
    #     n.save()
    #     return redirect('home_page')
        # all_notifications = Notif.objects.filter(user=request.user, is_delete=False).order_by("-date").values()[:3]
        # count = Notif.objects.filter(user=request.user, is_delete=False, is_read=False).count()
        # return JsonResponse({'notifications':list(all_notifications), 'count':count})
        # return HttpResponse("Marked as read")

@login_required()
def notification_delete(request,id):
    id = Notif.objects.get(id=id)
    id.is_delete=True
    id.save()
    return redirect('home_page')
    # if request.method == 'GET':
    #     id = request.GET['id']
    #     n = Notif.objects.get(id=id)
    #     n.is_delete = True
    #     n.save()
    #     return redirect('home_page')
        # all_notifications = Notif.objects.filter(user=request.user, is_delete=False).order_by("-date").values()[:3]
        # count = Notif.objects.filter(user=request.user, is_delete=False, is_read=False).count()
        # return JsonResponse({'notifications':list(all_notifications), 'count':count})


######### menu functionality ############    
@login_required()
def reports(request):
    if request.user.is_authenticated:
        user = User.objects.filter(email=request.user.email)
        for data in user:

            context={"udata": data, "date": datetime.now}

            return render(request, 'dashboard/reports.html',context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')

    else:
        return redirect('/')



@login_required()
def genearte_raw_data_report(request,id=id):
    if request.user.is_authenticated:
        user = User.objects.filter(email=request.user.email)
        for data in user:
            import csv
            from fpdf import FPDF
            df = pd.read_csv('dashboard/extraFiles/sample_data.csv',
                                header=None, skiprows=3)
            result = df.to_html(classes='table table-striped')

            with open('dashboard/extraFiles/sample_data.csv', newline='') as f:
                reader = csv.reader(f)

                pdf = FPDF()
                pdf.add_page()
                page_width = pdf.w - 2 * pdf.l_margin

                pdf.set_font('Times', 'B', 14.0)
                pdf.cell(page_width, 0.0, 'Sample Data', align='C')
                pdf.ln(10)

                pdf.set_font('Courier', '', 12)

                col_width = page_width / 4

                pdf.ln(1)

                th = pdf.font_size

                for row in reader:
                    # print(len(row))
                    pdf.cell(col_width, th, str(row[0]), border=1)
                    pdf.cell(col_width, th, row[1], border=1)
                    pdf.cell(col_width, th, row[2], border=1)

                    pdf.ln(th)

                pdf.ln(10)

                pdf.set_font('Times', '', 10.0)
                pdf.cell(page_width, 0.0, '- end of report -', align='C')

                pdf.output(name='dashboard/extraFiles/sample.pdf')
                report = pdf.output(dest='S').encode('latin-1')
                response  = HttpResponse(report,content_type='application/pdf')
                response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
                return  response



                return render(request,'dashboard/reports.html')
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')

    else:
        return redirect('/')

@login_required()
def rack_report(request):
    from django.template.loader import get_template
    from weasyprint import HTML
    from django.http import HttpResponse

    html_template = get_template('dashboard/check.html').render()
    pdf_file = HTML(string=html_template).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response
    return render(request,'dashboard/reports.html')


@login_required()
def plotly_graph(request):
    if request.user.is_authenticated:
        # print(request.user)
        user = User.objects.filter(email=request.user.email)
        for data in user:
            new_graphs = check_graphs()
            scatter_graph = type4graph()
            network_line_graph = line1()
            sankey_graph = sankey()
            sunburst_graph = sunburst()
            india_map_plt = india_map()

            context = {"udata": data,'india_map_plt':india_map_plt, "date": datetime.now,'new_graph': new_graphs, 'scatter_graph': scatter_graph, 'network_line_graph':network_line_graph, 'sankey_graph': sankey_graph,
                       'sunburst': sunburst_graph}
            return render(request, 'dashboard/graph.html', context)
    else:
        # print('not open')
        return redirect('/')


def visualization():
    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    df = pd.read_csv('/home/akus/Documents/2016.csv')
    sns.set(style="darkgrid")

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    x = df['Happiness Score']
    y = df['Economy (GDP per Capita)']
    z = df['Health (Life Expectancy)']

    ax.set_xlabel("Happiness")
    ax.set_ylabel("Economy")
    ax.set_zlabel("Health")

    ax.scatter(x, y, z)

    config = {'displayModeBar': False}

    three_d_plt_div = plotly.offline.plot(ax, output_type='div', config=config)

    return three_d_plt_div


@login_required()
def network_graph(request,id=id):
    if request.user.is_authenticated:
        user = User.objects.filter(email=request.user.email)
        device_count = DeviceEquipement.objects.count()
        # device_name = DeviceEquipement.objects.all()
        data_centers_count = DC.objects.count()
        for data in user:
            new_bluw_network = new_network()
            label_network = network_label()
            new_graphs = check_graphs()

            context = {
                'network_graph': new_bluw_network, 'device_count':device_count,'data_centers_count':data_centers_count,"udata": data, "date": datetime.now,'label_network': label_network, 'new_graphs':new_graphs,
            }

            return render(request, 'dashboard/network_monitoring.html', context)

    else:
        return redirect('/')


def new_network():
    import plotly.graph_objects as go
    import networkx as nx
    import re
    from dashboard.process import get_empty_appearances
    from dashboard.process import get_coappear

    
    f = open(os.path.join(settings.BASE_DIR, 'dashboard', 'midsummer.txt'),"r")
    whole_text = f.read()

    scenes = whole_text.split('SCENE ')
    # print(len(scenes))
    characters = re.findall('[A-Z]+[,;]', scenes[0])
    characters = [name.strip(',').strip(';').title() for name in characters]

    characters.remove('Goodfellow')  # Puck = Goodfellow
    characters.append('Fairies')
    characters.append('Attendants')
    # print(characters)

    # from process import get_empty_appearances

    appearances = get_empty_appearances(characters)
    # print(appearances)

    # print(scenes[0])
    # print(scenes[9])
    # print(scenes[9].split('***')[0])

    scenes[9] = scenes[9].split('***')[0]
    # print(scenes[9])

    internal_cast = {'Pyramus': 'Bottom',
                     'Thisbe': 'Flute',
                     'Wall': 'Snout',
                     'Moonshine': 'Starveling',
                     'Lion': 'Snug',
                     'Prologue': 'Quince'}
    # from multiprocessing import Process
    # from process import get_coappear

    appearances_Ii = get_coappear(scenes[1], 'I', internal_cast, appearances)
    appearances_Iii = get_coappear(scenes[2], 'I', internal_cast, appearances_Ii)

    appearances_IIi = get_coappear(scenes[3], 'II', internal_cast, appearances_Iii)
    appearances_IIii = get_coappear(scenes[4], 'II', internal_cast, appearances_IIi)

    appearances_IIIi = get_coappear(scenes[5], 'III', internal_cast, appearances_IIii)
    appearances_IIIii = get_coappear(scenes[6], 'III', internal_cast, appearances_IIIi)

    appearances_IVi = get_coappear(scenes[7], 'IV', internal_cast, appearances_IIIii)
    appearances_IVii = get_coappear(scenes[8], 'IV', internal_cast, appearances_IVi)

    all_appearances = get_coappear(scenes[9], 'V', internal_cast, appearances_IVii)

    appearance_counts = get_empty_appearances(characters, True)
    scene_counts = {}
    # print(scene_counts)

    # For each character that appears, get how many scenes the character appears in and
    # how many times each pair of characters appears together
    for character in all_appearances:
        scene_counts[character] = []
        for co_char in all_appearances[character]:
            appearance_counts[character][co_char] = len(all_appearances[character][co_char])
            scene_counts[character].extend(all_appearances[character][co_char])

        scene_counts[character] = len(set(scene_counts[character]))

    # print(appearance_counts)
    # print(scene_counts)

    midsummer = nx.Graph()
    # Add node for each character
    for char in scene_counts.keys():
        if scene_counts[char] > 0:
            midsummer.add_node(char, size=scene_counts[char])

    # print(midsummer.nodes)
    # For each co-appearance between two characters, add an edge
    for char in appearance_counts.keys():
        for co_char in appearance_counts[char].keys():

            # Only add edge if the count is positive
            if appearance_counts[char][co_char] > 0:
                midsummer.add_edge(char, co_char, weight=appearance_counts[char][co_char])
    # print(midsummer.edges())

    # Get positions for the nodes in G
    pos_ = nx.spring_layout(midsummer)
    # print(pos_)
    # print(midsummer.edges()[('Theseus', 'Hippolyta')])
    f.close()

    def make_edge(x, y, text, width):
        '''Creates a scatter trace for the edge between x's and y's with given width

        Parameters
        ----------
        x    : a tuple of the endpoints' x-coordinates in the form, tuple([x0, x1, None])

        y    : a tuple of the endpoints' y-coordinates in the form, tuple([y0, y1, None])

        width: the width of the line

        Returns
        -------
        An edge trace that goes between x0 and x1 with specified width.
        '''
        return go.Scatter(x=x,
                          y=y,
                          line=dict(width=width,
                                    color='cornflowerblue'),
                          hoverinfo='text',
                          text=([text]),
                          mode='lines')

    # For each edge, make an edge_trace, append to list
    edge_trace = []
    for edge in midsummer.edges():

        if midsummer.edges()[edge]['weight'] > 0:
            char_1 = edge[0]
            char_2 = edge[1]

            x0, y0 = pos_[char_1]
            x1, y1 = pos_[char_2]

            text = char_1 + '--' + char_2 + ': ' + str(midsummer.edges()[edge]['weight'])

            trace = make_edge([x0, x1, None], [y0, y1, None], text,
                              0.3 * midsummer.edges()[edge]['weight'] ** 1.75)

            edge_trace.append(trace)

    # Make a node trace
    node_trace = go.Scatter(x=[],
                            y=[],
                            text=[],
                            textposition="top center",
                            textfont_size=10,
                            mode='markers+text',
                            hoverinfo='none',
                            marker=dict(color=[],
                                        size=[],
                                        line=None))
    # For each node in midsummer, get the position and size and add to the node_trace
    for node in midsummer.nodes():
        x, y = pos_[node]
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
        node_trace['marker']['color'] += tuple(['cornflowerblue'])
        node_trace['marker']['size'] += tuple([5 * midsummer.nodes()[node]['size']])
        node_trace['text'] += tuple(['<b>' + node + '</b>'])

    layout = go.Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )

    fig = go.Figure(layout=layout)

    for trace in edge_trace:
        fig.add_trace(trace)

    network_fig = fig.add_trace(node_trace)

    network_fig.update_layout(showlegend=False)

    network_fig.update_xaxes(showticklabels=False)

    network_fig.update_yaxes(showticklabels=False)

    config = {'displayModeBar': False}
    network_plt_div = plotly.offline.plot(network_fig, output_type='div', config=config)
    return network_plt_div



def network_label():
    import plotly.graph_objects as go

    import networkx as nx

    G = nx.random_geometric_graph(100, 0.125)

    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            # 'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            # 'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            # 'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line_width=2))

    node_adjacencies = []
    node_text = []
    for node, adjacencies in enumerate(G.adjacency()):
        node_adjacencies.append(len(adjacencies[1]))
        node_text.append('# of connections: ' + str(len(adjacencies[1])))

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    label_network_fig = go.Figure(data=[edge_trace, node_trace],
                                  layout=go.Layout(

                                      titlefont_size=16,
                                      showlegend=False,
                                      hovermode='closest',
                                      margin=dict(b=20, l=5, r=5, t=40),
                                      annotations=[dict(
                                          showarrow=False,
                                          xref="paper", yref="paper",
                                          x=0.005, y=-0.002)],
                                      xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                                      yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                                  )

    config = {'displayModeBar': False}
    label_network_plt_div = plotly.offline.plot(label_network_fig, output_type='div', config=config)
    return label_network_plt_div

def check_graphs():
    t = np.linspace(0, 10, 100)

    check_fig = go.Figure()

    check_fig.add_trace(go.Scatter(
        x=t, y=np.sin(t),
        name='Input',
        mode='markers',
        marker_color='rgba(152, 0, 0, .8)'
    ))

    check_fig.add_trace(go.Scatter(
        x=t, y=np.cos(t),
        name='output',
        mode='markers',
        marker_color='rgba(255, 182, 193, .9)'
    ))

    # Set options common to all traces with fig.update_traces
    check_fig.update_traces(mode='markers', marker_line_width=2, marker_size=10)
    check_fig.update_layout(title='Styled Scatter',
                            yaxis_zeroline=False, xaxis_zeroline=False)

    config = {'displayModeBar': False}

    new_plt_div = plotly.offline.plot(check_fig, output_type='div', config=config)

    return new_plt_div


# def visualization():
#     import matplotlib.pyplot as plt
#     import pandas as pd
#     import seaborn as sns

#     df = pd.read_csv('/home/akus/Documents/2016.csv')
#     sns.set(style="darkgrid")

#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')

#     x = df['Happiness Score']
#     y = df['Economy (GDP per Capita)']
#     z = df['Health (Life Expectancy)']

#     ax.set_xlabel("Happiness")
#     ax.set_ylabel("Economy")
#     ax.set_zlabel("Health")

#     ax.scatter(x, y, z)

#     config = {'displayModeBar': False}

#     three_d_plt_div = plotly.offline.plot(ax, output_type='div', config=config)

#     return three_d_plt_div


# def plotly_graph(request):
#     if request.session.has_key('uid'):
#         user = User.objects.filter(email=request.session['uid'])
#         for data in user:
#             new_graphs = check_graphs()
#             scatter_graph = type4graph()
#             network_line_graph = line1()
#             sankey_graph = sankey()
#             sunburst_graph = sunburst()
#             india_map_plt = india_map()

#             context = {"udata": data,'india_map_plt':india_map_plt, "date": datetime.now,'new_graph': new_graphs, 'scatter_graph': scatter_graph, 'network_line_graph':network_line_graph, 'sankey_graph': sankey_graph,
#                        'sunburst': sunburst_graph}
#             return render(request, 'dashboard/graph.html', context)
#     else:
#         return redirect('/')


def type4graph():
    import plotly.express as px
    df = px.data.iris()
    scatter_fig1 = px.scatter(df, x="sepal_width", y="sepal_length", color="species",
                              size='petal_length', hover_data=['petal_width'])

    config = {'displayModeBar': False}
    scatter_plt1 = plotly.offline.plot(scatter_fig1, output_type='div', config=config)

    return scatter_plt1


def line1():
    import plotly
    import cufflinks as cf
    import pandas as pd

    # setup
    layout1 = cf.Layout(
        height=400,
        width=400
    )
    cf.go_offline()
    df = pd.read_csv("https://raw.githubusercontent.com/akusits/akus_monitoring_graphs_data/master/file(1).csv")

    network_line_plot = df.iplot(asFigure=True, kind='line', layout=layout1)

    config = {'displayModeBar': False}
    line1 = plotly.offline.plot(network_line_plot, output_type='div', config=config)
    return line1

def sankey():
    import plotly.graph_objects as go
    import urllib, json

    url = 'https://raw.githubusercontent.com/plotly/plotly.js/master/test/image/mocks/sankey_energy.json'
    response = urllib.request.urlopen(url)
    data = json.loads(response.read())

    # override gray link colors with 'source' colors
    opacity = 0.4
    # change 'magenta' to its 'rgba' value to add opacity
    data['data'][0]['node']['color'] = ['rgba(255,0,255, 0.8)' if color == "magenta" else color for color in
                                        data['data'][0]['node']['color']]
    data['data'][0]['link']['color'] = [data['data'][0]['node']['color'][src].replace("0.8", str(opacity))
                                        for src in data['data'][0]['link']['source']]

    fig5 = go.Figure(data=[go.Sankey(
        valueformat=".0f",
        valuesuffix="TWh",
        # Define nodes
        node=dict(
            pad=15,
            thickness=15,
            line=dict(color="black", width=0.5),
            label=data['data'][0]['node']['label'],
            color=data['data'][0]['node']['color']
        ),
        # Add links
        link=dict(
            source=data['data'][0]['link']['source'],
            target=data['data'][0]['link']['target'],
            value=data['data'][0]['link']['value'],
            label=data['data'][0]['link']['label'],
            color=data['data'][0]['link']['color']
        ))])

    config = {'displayModeBar': False}
    sankey1 = plotly.offline.plot(fig5, output_type='div', config=config)

    return sankey1    


def sunburst():
    import plotly.express as px
    df = px.data.tips()
    sunburst_fig = px.sunburst(df, path=['sex', 'day', 'time'], values='total_bill', color='day')

    config = {'displayModeBar': False}
    sunburst_plt_div = plotly.offline.plot(sunburst_fig, output_type='div', config=config)
    return sunburst_plt_div

def india_map():
    import pandas as pd
    import plotly.express as px

    df = pd.read_csv(
        "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")

    india_fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',

        color_continuous_scale='Reds'
    )

    india_fig.update_geos(fitbounds="locations", visible=False)
    config = {'displayModeBar': False}


    india_map_plt = offline.plot(india_fig, show_link=False, config=config, output_type='div')

    # hexbin_plt = plotly.offline.plot(fig, output_type='div')

    return india_map_plt

def home_network(request,id=id):
    if request.user.is_authenticated:
        user = User.objects.filter(email=request.user.email)
        for data in user:

            network_line_graph = line1()
            gauge = testgauge1()
            # needlegauge = needle_gauge()
            heatmap = check_heatmap()
            context = {'gauge': gauge, "udata": data, "date": datetime.now,'network_line_graph': network_line_graph, 'heatmap': heatmap,

                        }
            return render(request, 'dashboard/home_network.html', context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')
    else:
        return redirect('/')


def testgauge1():
    import pygal
    gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.70, width=200, height=200,
                             show_legend=False)

    gauge.add('', [{'value': 630, 'max_value': 1000, 'color': 'lime', }])
    some_name = gauge.render_data_uri()
    return some_name

def check_heatmap():
    import plotly.graph_objects as go
    import datetime
    import numpy as np
    np.random.seed(1)

    programmers = ['Alex', 'Nicole', 'Sara', 'Etienne', 'Chelsea', 'Jody', 'Marianne']

    base = datetime.datetime.today()
    dates = base - np.arange(180) * datetime.timedelta(days=1)
    z = np.random.poisson(size=(len(programmers), len(dates)))

    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=dates,
        y=programmers,
        colorscale='Viridis'))

    heatmap_fig = fig.update_layout(
        title='GitHub commits per day',
        xaxis_nticks=36)

    config = {'displayModeBar': False}
    gauge_plt = plotly.offline.plot(heatmap_fig, output_type='div', config=config)

    return gauge_plt




def apm_monitoring(request):
    if request.user.is_authenticated:
        user = User.objects.filter(email=request.user.email)
        for data in user:
            
            import networkx as nx
            import matplotlib.pyplot as plt
            import io

            device_count = DeviceEquipement.objects.count()
            # device_name = DeviceEquipement.objects.all()
            data_centers_count = DC.objects.count()

            G = nx.DiGraph()

            G.add_edges_from([('A', 'B'), ('C', 'D'), ('G', 'D')], weight=1)
            G.add_edges_from([('D', 'A'), ('D', 'E'), ('B', 'D'), ('D', 'E')], weight=2)
            G.add_edges_from([('B', 'C'), ('E', 'F')], weight=3)
            G.add_edges_from([('C', 'F')], weight=4)

            val_map = {'A': 1.0,
                        'D': 0.5714285714285714,
                        'H': 0.0}

            values = [val_map.get(node, 0.45) for node in G.nodes()]
            edge_labels = dict([((u, v,), d['weight'])
                                for u, v, d in G.edges(data=True)])
            red_edges = [('C', 'D'), ('D', 'A')]
            edge_colors = ['black' if not edge in red_edges else 'red' for edge in G.edges()]

            pos = nx.spring_layout(G)
            nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
            nx.draw(G, pos, node_color=values, node_size=1500, edge_color=edge_colors, edge_cmap=plt.cm.Reds)
            buf = io.BytesIO()
            plt.savefig(buf, format='svg', bbox_inches='tight')
            image_bytes = buf.getvalue().decode('utf-8')
            buf.close()
            plt.close()
            context = {

                'my_chart': image_bytes,"udata": data, "date": datetime.now,'device_count':device_count,
                'data_centers_count':data_centers_count,
            }

            return render(request, 'dashboard/apm.html', context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')
    else:
        return redirect('/')


def database_monitoring(request,id=id):
    if request.user.is_authenticated:
        user = User.objects.filter(email=request.user.email)
        device_count = DeviceEquipement.objects.count()
        # device_name = DeviceEquipement.objects.all()
        data_centers_count = DC.objects.count()
        for data in user:

            piechart = pie_chart2()
            barchart = bar_plot4()
            barchart1 = bar_chart1()
            barchart2 = bar_chart()
            # heartchart= heart_beat()

            context = {"udata": data, 'device_count':device_count,'data_centers_count':data_centers_count,"date": datetime.now,'piechart': piechart, 'barchart': barchart, 'barchart1': barchart1, 'barchart2': barchart2}
            return render(request, 'dashboard/database_monitoring.html', context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')
    else:
        return redirect('/')

def pie_chart2():
    import pygal
    pie_chart = pygal.Pie(show_legend=False,
                          style=pygal.style.styles['default'](value_font_size=60))
    pie_chart.add('IE', [5.7, 10.2, 2.6, 1])
    pie_chart.add('Firefox', [.6, 16.8, 7.4, 2.2, 1.2, 1, 1, 1.1, 4.3, 1])
    pie_chart.add('Chrome', [.3, .9, 17.1, 15.3, .6, .5, 1.6])
    pie_chart.add('Safari', [4.4, .1])
    pie_chart.add('Opera', [.1, 1.6, .1, .5])
    pie2 = pie_chart.render_data_uri()
    return pie2

def bar_plot4():
    import plotly.graph_objects as go

    x = ['b', 'a', 'c', 'd']
    fig = go.Figure(go.Bar(x=x, y=[2, 5, 1, 9], name='Montreal'))
    fig.add_trace(go.Bar(x=x, y=[1, 4, 9, 16], name='Ottawa'))
    fig.add_trace(go.Bar(x=x, y=[6, 8, 4.5, 8], name='Toronto'))

    fig.update_layout(barmode='stack', xaxis={'categoryorder': 'category ascending'})

    config = {'displayModeBar': False}
    bar_chart = plotly.offline.plot(fig, output_type='div', config=config)

    return bar_chart


def bar_chart1():
    import plotly.express as px
    data_canada = px.data.gapminder().query("country == 'Canada'")
    fig = px.bar(data_canada, x='year', y='pop')

    config = {'displayModeBar': False}
    bar_chart1 = plotly.offline.plot(fig, output_type='div', config=config)

    return bar_chart1


def bar_chart():
    import pygal
    line_chart = pygal.Bar(show_legend=False,
                           style=pygal.style.styles['default'](value_font_size=60))
    line_chart.title = 'Browser usage evolution (in %)'
    line_chart.x_labels = map(str, range(2002, 2013))
    line_chart.add('Firefox', [None, None, 0, 16.6, 25, 31, 36.4, 45.5, 46.3, 42.8, 37.1])
    line_chart.add('Chrome', [None, None, None, None, None, None, 0, 3.9, 10.8, 23.8, 35.3])
    line_chart.add('IE', [85.8, 84.6, 84.7, 74.5, 66, 58.6, 54.7, 44.8, 36.2, 26.6, 20.1])
    line_chart.add('Others', [14.2, 15.4, 15.3, 8.9, 9, 10.4, 8.9, 5.8, 6.7, 6.8, 7.5])
    bar = line_chart.render_data_uri()
    return bar


def storage(request,id=id):
    device_count = DeviceEquipement.objects.count()
    # device_name = DeviceEquipement.objects.all()
    data_centers_count = DC.objects.count()
    if request.user.is_authenticated:
        user = User.objects.filter(email=request.user.email)
        for data in user:
           
            piechart = pie_chart2()
            context={
                "udata": data, "date": datetime.now,'piechart':piechart,'device_count':device_count,'data_centers_count':data_centers_count,
            }
            return render(request, 'dashboard/storage.html',context)
        else:
            return HttpResponse('Sorry , You do not have access rights to this page. Kindly login as admin .')
    else:
        return redirect('/')

def delete_web_monitor(request, id):
    nf = Notification()
    try:
        website = WebsiteLinks.objects.get(id=id)
        website.delete()
        msg = "Deleted Successfully"
        return redirect('hexbin_graph')
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })
def delete_cctv(request, id):
    nf = Notification()
    try:
        cctv = Product.objects.get(id=id)
        cctv.delete()
        msg = "Deleted Successfully"
        return redirect('cctv')
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })
def delete_camera(request, id):
    nf = Notification()
    try:
        camera = CameraMonitor.objects.get(id=id)
        camera.delete()
        msg = "Deleted Successfully"
        return redirect('cctv')
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })
def hexbin_graph(request):
    if request.user.is_authenticated:
        nf = Notification()
        websites_pack = WebsiteLinks.objects.all()
        totalWebsite = websites_pack.count()
        if request.method == 'POST':
            try:
                data = []
                total = 0
                down = 0
                if request.POST.get('website_name'):
                    website = request.POST.get('protocol')+request.POST.get('website_name')
                    if WebsiteLinks.objects.filter(website_name=website):
                        return redirect("/web/monitoring?msg=error")
                    websites = WebsiteLinks()
                    websites.website_name = website
                    websites.save() 
                    state = False
                    for url in websites_pack:
                        startTime = time.time()
                        try:
                            r = requests.get(url.website_name).status_code
                        except ConnectionError as err:
                            r = 0
                        except requests.exceptions.RequestException as err:
                            r = 0
                        if r == 200:
                            state = True
                            total = total + 1
                        else:
                            state=False
                            down = down + 1
                        data.append({
                            'id':url.id,
                            'website':url.website_name,
                            'status':state,
                            'time': round((time.time() - startTime),2)
                        })
                    context = {
                        'website_pack': data, 'total':total, 'down':down,'totalWebsite':totalWebsite
                            }
                    return render(request, 'dashboard/heatmap.html',context)
            except Exception as e:
                message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
                return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
        else:
            msg = request.GET.get('msg','')
            data = []
            total = 0
            down = 0
            for url in websites_pack:
                state = False
                startTime = time.time()
                try:
                    r = requests.get(url.website_name).status_code
                except ConnectionError as err:
                    r = 0
                except requests.exceptions.RequestException as err:
                    r = 0
                if r == 200:
                    state = True
                    total = total + 1
                else:
                    state=False
                    down = down + 1
                data.append({
                    'id':url.id,
                    'website':url.website_name,
                    'status':state,
                    'time': round((time.time() - startTime),2)
                })
            context = {
                'website_pack': data, 'total':total, 'down':down,'totalWebsite':totalWebsite
            }
            return render(request, 'dashboard/heatmap.html', context)
    else: 
        return redirect('/')



def cctv(request):
    if request.user.is_authenticated:    
        camera_links = CameraMonitor.objects.all()
        cctv_links = Product.objects.all()
        nf = Notification()
        if request.method == 'POST':
            if request.POST.get("form_type") == 'formTwo':
                try:
                    if request.POST.get('name'):
                        cctv_websites = Product()
                        cctv_websites.name = request.POST.get('name')
                        cctv_websites.save()
                        cameraTotal = 0
                        cameraDown = 0
                        cctvTotal = 0
                        cctvDown = 0
                        cameraObject = CameraMonitor.objects.all()
                        for url in cameraObject:
                            try:
                                r = requests.get(url.url).status_code
                            except ConnectionError as err:
                                r = 0
                            except requests.exceptions.RequestException as err:
                                r = 0
                            if r == 200:
                                cameraTotal = cameraTotal + 1
                            else:
                                cameraDown = cameraDown + 1
                        cctvObject = Product.objects.all()
                        for url in cctvObject:
                            try:
                                r = requests.get(url.name).status_code
                            except ConnectionError as err:
                                r = 0
                            except requests.exceptions.RequestException as err:
                                r = 0
                            if r == 200:
                                cctvTotal = cctvTotal + 1
                            else:
                                cctvDown = cctvDown + 1
                        context = {'cctv_links': cctv_links,'camera_links':camera_links,'cameraTotal':cameraTotal,'cctvTotal':cctvTotal,'cameraDown':cameraDown,'cctvDown':cctvDown}
                        return render(request, 'dashboard/cctv.html', context)
                except Exception as e:
                    message = nf.show_result(result="Error", helping_text="HINT:SYSTEM FAULT! Please Contact Admin", title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
                    return render(request, 'dashboard/message_page.html',{
                        'message' : message,
                    })
            if request.POST.get("form_type") == 'formOne':
                try:
                    if request.POST.get('name'):
                        cctv_websites = CameraMonitor()
                        cctv_websites.url = request.POST.get('name')
                        cctv_websites.save()
                        cameraTotal = 0
                        cameraDown = 0
                        cctvTotal = 0
                        cctvDown = 0
                        cameraObject = CameraMonitor.objects.all()
                        for url in cameraObject:
                            try:
                                r = requests.get(url.url).status_code
                            except ConnectionError as err:
                                r = 0
                            except requests.exceptions.RequestException as err:
                                r = 0
                            if r == 200:
                                cameraTotal = cameraTotal + 1
                            else:
                                cameraDown = cameraDown + 1
                        cctvObject = Product.objects.all()
                        for url in cctvObject:
                            try:
                                r = requests.get(url.name).status_code
                            except ConnectionError as err:
                                r = 0
                            except requests.exceptions.RequestException as err:
                                r = 0
                            if r == 200:
                                cctvTotal = cctvTotal + 1
                            else:
                                cctvDown = cctvDown + 1
                        context = {'cctv_links': cctv_links,'camera_links':camera_links,'cameraTotal':cameraTotal,'cctvTotal':cctvTotal,'cameraDown':cameraDown,'cctvDown':cctvDown}
                        return render(request, 'dashboard/cctv.html', context)
                except Exception as e:
                    message = nf.show_result(result="Error", helping_text="HINT:SYSTEM FAULT! Please Contact Admin", title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
                    return render(request, 'dashboard/message_page.html',{
                        'message' : message,
                     })
        else:
            cameraTotal = 0
            cameraDown = 0
            cctvTotal = 0
            cctvDown = 0
            cameraObject = CameraMonitor.objects.all()
            for url in cameraObject:
                try:
                    r = requests.get(url.url).status_code
                except ConnectionError as err:
                    r = 0
                except requests.exceptions.RequestException as err:
                    r = 0
                if r == 200:
                    cameraTotal = cameraTotal + 1
                else:
                    cameraDown = cameraDown + 1
            cctvObject = Product.objects.all()
            for url in cctvObject:
                try:
                    r = requests.get(url.name).status_code
                except ConnectionError as err:
                    r = 0
                except requests.exceptions.RequestException as err:
                    r = 0
                if r == 200:
                    cctvTotal = cctvTotal + 1
                else:
                    cctvDown = cctvDown + 1
            context = {'cctv_links': cctv_links,'camera_links':camera_links,'cameraTotal':cameraTotal,     'cctvTotal':cctvTotal,'cameraDown':cameraDown,'cctvDown':cctvDown}
            return render(request, 'dashboard/cctv.html', context)
    else:
        return redirect('/')



def apmReport(request):
    return render(request,'dashboard/apm_report.html')



def mail(request):
    return render(request,'dashboard/mail.html')



def aboutUs(request):
    return render(request,'dashboard/aboutUs.html') 


def dataReview(request):
    return render(request,'dashboard/dataReview.html') 


def dataCheck(request):
    return render(request,'dashboard/dataCheck.html') 

@login_required
def contactUs(request):
    nf = Notification()
    try:
        user = User.objects.get(username=request.user)
        msg = ""
        # print(user)
        if request.method == "POST":
            data = {key:request.POST[key].strip() for key in request.POST if not key == "csrfmiddlewaretoken"}
            contact = ContactUs(fname = data["firstname"], lname=data["lastname"], email=data.get("email",""), msg=data["subject"])
            contact.save()
            msg = "Thank you for contacting us"
        
        return render(request,'dashboard/contactUs.html',{'user':user,'msg':msg}) 
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

@login_required
def raiseTicket(request):
    nf = Notification()
    try:
        user = User.objects.get(username=request.user)
        msg = ""
        myTicket = RaiseTicket.objects.filter(user=user)
        # print(user)
        if request.method == "POST":
            ticket = RaiseTicketForm(request.POST, request.FILES)
            if ticket.is_valid():
                instance = ticket.save(commit=False)
                instance.user = request.user
                instance.save()
                msg = "Thank you for raising a ticket"
        else:
            ticket = RaiseTicketForm()
        return render(request,'dashboard/raiseTicket.html',{'user':user,'msg':msg, 'ticket':ticket,'myTicket':myTicket}) 
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

@login_required
def viewRaiseTicket(request, id):
    nf = Notification()
    try:
        msg = ""
        ticket = RaiseTicket.objects.get(id=id)
        if request.method == "POST":
            data = {key:request.POST[key].strip() for key in request.POST if not key == "csrfmiddlewaretoken"}
            print(data)
            ticket = RaiseTicket.objects.get(id=id)
            ticket.admin_response = data.get("admin_response","")
            if data["aprove"] == 'aproved':
                ticket.is_aprove = True
            else:
                ticket.is_aprove = False
            ticket.accepted = True
            ticket.updated = datetime.now()
            ticket.save()
        else:
            pass
        return render(request,'dashboard/viewRaiseTicket.html',{'ticket':ticket}) 
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

class netconfTopology(View):
    def get(self, request):
        return render(request, "dashboard/netconfTopology.html")

class topology(View):
    def get(self, request):
        #views_topology.mainFunction()
        # base = "dashboard/static/"
        
        # base = "dashboard/static/"
        # f = open(base + "snmp/graph.json")
        
        # data = json.load(f)
        # data["nodes"].insert(0 , {"group" : "0" , "id" : "parent" , "image" : "akus.png" , "protocol" : False})
        # data["links"].insert(0 , {"source": "parent", "target": "", "value": "40"})
        # f.close()
        
        # f = open(base + "snmp/graph.json" , "w")
        # f.write(json.dumps(data))
        # f.close()

        return render(request, "dashboard/topology.html")


def table(request):
    return render(request,"dashboard/table.html")

def myPath(request,id, value):
    nf = Notification()
    try:
        d = DeviceCapibility.objects.get(id=id)
        value = value
        if value=='snmp':
            context = {'device':d.snmp}
        if value=='rest':
            context = {'device':d.restconf}
        if value=='net':
            context = {'device':d.netconf}
        # print(device)
        return render(request , "dashboard/displayServerInformation.html",context)
    except Exception as e:
        message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
            
        # apart from these add any show_results you want in any other variable names
        return render(request, 'dashboard/message_page.html',{
            'message' : message,
        })

# returns XML
def getConfigData():
    return '<?xml version="1.0" encoding="UTF-8"?> <rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:de3b5a79-f4f4-440e-bb8d-501249ef8aa7" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"><data><native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"><version>16.9</version><boot-start-marker/><boot-end-marker/><service><timestamps><debug><datetime><msec></msec></datetime></debug><log><datetime><msec/></datetime></log></timestamps></service><platform><hardware xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-platform"><throughput><level><kbps>100000</kbps></level></throughput></hardware></platform><hostname>Router</hostname><enable><password><secret>cisco</secret></password></enable><username><name>admin</name><privilege>15</privilege><secret><encryption>5</encryption><secret>$1$DgKW$Y8.k0.FDMTAzuZqZVdEeU.</secret></secret></username><vrf><definition><name>Mgmt-intf</name><address-family><ipv4></ipv4><ipv6></ipv6></address-family></definition></vrf><ip><forward-protocol><protocol>nd</protocol></forward-protocol><tftp><source-interface><GigabitEthernet>0</GigabitEthernet></source-interface></tftp><http xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-http"><authentication><local/></authentication><server>true</server><secure-server>true</secure-server></http></ip><interface><GigabitEthernet><name>0</name><shutdown/><vrf><forwarding>Mgmt-intf</forwarding></vrf><negotiation xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet"><auto>true</auto></negotiation></GigabitEthernet><GigabitEthernet><name>0/0/0</name><ip><address><primary><address>192.168.0.8</address><mask>255.255.255.0</mask></primary></address></ip><negotiation xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet"><auto>true</auto></negotiation></GigabitEthernet><GigabitEthernet><name>0/0/1</name><ip><address><primary><address>192.168.1.10</address><mask>255.255.255.0</mask></primary></address></ip><negotiation xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet"><auto>true</auto></negotiation></GigabitEthernet></interface><control-plane></control-plane><login><on-success><log></log></on-success></login><multilink><bundle-name xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ppp">authenticated</bundle-name></multilink><redundancy><mode>none</mode></redundancy><spanning-tree><extend xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-spanning-tree"><system-id/></extend></spanning-tree><subscriber><templating/></subscriber><crypto><pki xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-crypto"><trustpoint><id>TP-self-signed-2470217082</id><enrollment><selfsigned/></enrollment><revocation-check>none</revocation-check><rsakeypair><key-label>TP-self-signed-2470217082</key-label></rsakeypair><subject-name>cn=IOS-Self-Signed-Certificate-2470217082</subject-name></trustpoint><certificate><chain><name>TP-self-signed-2470217082</name><certificate><serial>01</serial><certtype>self-signed</certtype></certificate></chain></certificate></pki></crypto><license><udi><pid>ISR4321/K9</pid><sn>FDO20371PKD</sn></udi><accept><end/><user/><agreement/></accept><boot><level><securityk9/></level></boot></license><line><aux><first>0</first><stopbits>1</stopbits></aux><console><first>0</first><stopbits>1</stopbits><transport><input><input>none</input></input></transport></console><vty><first>0</first><last>4</last><login></login><password><secret>cisco</secret></password></vty></line><diagnostic xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-diagnostics"><bootup><level>minimal</level></bootup></diagnostic></native><licensing xmlns="http://cisco.com/ns/yang/cisco-smart-license"><config><enable>false</enable><privacy><hostname>false</hostname><version>false</version></privacy><utility><utility-enable>false</utility-enable></utility></config></licensing><interfaces xmlns="http://openconfig.net/yang/interfaces"><interface><name>GigabitEthernet0</name><config><name>GigabitEthernet0</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>false</enabled></config><subinterfaces><subinterface><index>0</index><config><index>0</index><enabled>false</enabled></config><ipv6 xmlns="http://openconfig.net/yang/interfaces/ip"><config><enabled>false</enabled></config></ipv6></subinterface></subinterfaces><ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet"><config><mac-address>00:6b:f1:6f:7f:9f</mac-address><auto-negotiate>true</auto-negotiate></config></ethernet></interface><interface><name>GigabitEthernet0/0/0</name><config><name>GigabitEthernet0/0/0</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>true</enabled></config><subinterfaces><subinterface><index>0</index><config><index>0</index><enabled>true</enabled></config><ipv4 xmlns="http://openconfig.net/yang/interfaces/ip"><addresses><address><ip>192.168.0.8</ip><config><ip>192.168.0.8</ip><prefix-length>24</prefix-length></config></address></addresses></ipv4><ipv6 xmlns="http://openconfig.net/yang/interfaces/ip"><config><enabled>false</enabled></config></ipv6></subinterface></subinterfaces><ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet"><config><mac-address>00:6b:f1:6f:7f:10</mac-address><auto-negotiate>true</auto-negotiate></config></ethernet></interface><interface><name>GigabitEthernet0/0/1</name><config><name>GigabitEthernet0/0/1</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>true</enabled></config><subinterfaces><subinterface><index>0</index><config><index>0</index><enabled>true</enabled></config><ipv4 xmlns="http://openconfig.net/yang/interfaces/ip"><addresses><address><ip>192.168.1.10</ip><config><ip>192.168.1.10</ip><prefix-length>24</prefix-length></config></address></addresses></ipv4><ipv6 xmlns="http://openconfig.net/yang/interfaces/ip"><config><enabled>false</enabled></config></ipv6></subinterface></subinterfaces><ethernet xmlns="http://openconfig.net/yang/interfaces/ethernet"><config><mac-address>00:6b:f1:6f:7f:11</mac-address><auto-negotiate>true</auto-negotiate></config></ethernet></interface></interfaces><network-instances xmlns="http://openconfig.net/yang/network-instance"><network-instance><name>Mgmt-intf</name><config><name>Mgmt-intf</name><type xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types">oc-ni-types:L3VRF</type><enabled-address-families xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</enabled-address-families><enabled-address-families xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</enabled-address-families></config><interfaces><interface><id>GigabitEthernet0</id><config><id>GigabitEthernet0</id><interface>GigabitEthernet0</interface></config></interface></interfaces><tables><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family></config></table></tables><protocols><protocol><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</identifier><name>DEFAULT</name><config><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</identifier><name>DEFAULT</name></config></protocol><protocol><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</identifier><name>DEFAULT</name><config><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</identifier><name>DEFAULT</name></config></protocol></protocols></network-instance><network-instance><name>default</name><config><name>default</name><type xmlns:oc-ni-types="http://openconfig.net/yang/network-instance-types">oc-ni-types:DEFAULT_INSTANCE</type><description>default-vrf [read-only]</description></config><tables><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV4</address-family></config></table><table><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family><config><protocol xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</protocol><address-family xmlns:oc-types="http://openconfig.net/yang/openconfig-types">oc-types:IPV6</address-family></config></table></tables><protocols><protocol><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</identifier><name>DEFAULT</name><config><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:STATIC</identifier><name>DEFAULT</name></config></protocol><protocol><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</identifier><name>DEFAULT</name><config><identifier xmlns:oc-pol-types="http://openconfig.net/yang/policy-types">oc-pol-types:DIRECTLY_CONNECTED</identifier><name>DEFAULT</name></config></protocol></protocols></network-instance></network-instances><components xmlns="http://openconfig.net/yang/platform"><component><name>Slot0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties><subcomponents><subcomponent><name>Subslot0/0</name><config><name>Subslot0/0</name></config></subcomponent></subcomponents></component><component><name>SlotF0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component><component><name>SlotP0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component><component><name>SlotP2</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component><component><name>SlotR0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component><component><name>ISR4321/K9</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties><subcomponents><subcomponent><name>Slot0</name><config><name>Slot0</name></config></subcomponent><subcomponent><name>SlotF0</name><config><name>SlotF0</name></config></subcomponent><subcomponent><name>SlotP0</name><config><name>SlotP0</name></config></subcomponent><subcomponent><name>SlotP2</name><config><name>SlotP2</name></config></subcomponent><subcomponent><name>SlotR0</name><config><name>SlotR0</name></config></subcomponent></subcomponents></component><component><name>Subslot0/0</name><properties><property><name>Operational Status</name><config><name>Operational Status</name></config></property></properties></component></components><interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"><interface><name>GigabitEthernet0</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>false</enabled><ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv4><ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv6></interface><interface><name>GigabitEthernet0/0/0</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>true</enabled><ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"><address><ip>192.168.0.8</ip><netmask>255.255.255.0</netmask></address></ipv4><ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv6></interface><interface><name>GigabitEthernet0/0/1</name><type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type><enabled>true</enabled><ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"><address><ip>192.168.1.10</ip><netmask>255.255.255.0</netmask></address></ipv4><ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"></ipv6></interface></interfaces><nacm xmlns="urn:ietf:params:xml:ns:yang:ietf-netconf-acm"><enable-nacm>true</enable-nacm><read-default>deny</read-default><write-default>deny</write-default><exec-default>deny</exec-default><enable-external-groups>true</enable-external-groups><rule-list><name>admin</name><group>PRIV15</group><rule><name>permit-all</name><module-name>*</module-name><access-operations>*</access-operations><action>permit</action></rule></rule-list></nacm><routing xmlns="urn:ietf:params:xml:ns:yang:ietf-routing"><routing-instance><name>Mgmt-intf</name><interfaces><interface>GigabitEthernet0</interface></interfaces><routing-protocols><routing-protocol><type>static</type><name>1</name></routing-protocol></routing-protocols></routing-instance><routing-instance><name>default</name><description>default-vrf [read-only]</description><routing-protocols><routing-protocol><type>static</type><name>1</name></routing-protocol></routing-protocols></routing-instance></routing></data></rpc-reply>'

# returns YAML
def getCapData():
    data = { "urn:ietf:params:netconf:base:1.0": "<ncclient.capabilities.Capability object at 0x7ff62888c550>", "urn:ietf:params:netconf:base:1.1": "<ncclient.capabilities.Capability object at 0x7ff62888c5b0>", "urn:ietf:params:netconf:capability:writable-running:1.0": "<ncclient.capabilities.Capability object at 0x7ff62888c610>", "urn:ietf:params:netconf:capability:xpath:1.0": "<ncclient.capabilities.Capability object at 0x7ff62888c670>", "urn:ietf:params:netconf:capability:validate:1.0": "<ncclient.capabilities.Capability object at 0x7ff62888c6d0>", "urn:ietf:params:netconf:capability:validate:1.1": "<ncclient.capabilities.Capability object at 0x7ff62888c730>", "urn:ietf:params:netconf:capability:rollback-on-error:1.0": "<ncclient.capabilities.Capability object at 0x7ff62888c790>", "urn:ietf:params:netconf:capability:notification:1.0": "<ncclient.capabilities.Capability object at 0x7ff62888c7f0>", "urn:ietf:params:netconf:capability:interleave:1.0": "<ncclient.capabilities.Capability object at 0x7ff62888c850>", "urn:ietf:params:netconf:capability:with-defaults:1.0?basic-mode=explicit&also-supported=report-all-tagged": "<ncclient.capabilities.Capability object at 0x7ff62888c8b0>", "urn:ietf:params:netconf:capability:yang-library:1.0?revision=2016-06-21&module-set-id=2b37546fdd72b6fa6a1d06d2dff00cfd": "<ncclient.capabilities.Capability object at 0x7ff62888c9a0>", "http://tail-f.com/ns/netconf/actions/1.0": "<ncclient.capabilities.Capability object at 0x7ff62888ca00>", "http://tail-f.com/ns/netconf/extensions": "<ncclient.capabilities.Capability object at 0x7ff62888c910>", "http://cisco.com/ns/cisco-xe-ietf-ip-deviation?module=cisco-xe-ietf-ip-deviation&revision=2016-08-10": "<ncclient.capabilities.Capability object at 0x7ff62888c970>", "http://cisco.com/ns/cisco-xe-ietf-ipv4-unicast-routing-deviation?module=cisco-xe-ietf-ipv4-unicast-routing-deviation&revision=2015-09-11": "<ncclient.capabilities.Capability object at 0x7ff62888cb20>", "http://cisco.com/ns/cisco-xe-ietf-ipv6-unicast-routing-deviation?module=cisco-xe-ietf-ipv6-unicast-routing-deviation&revision=2015-09-11": "<ncclient.capabilities.Capability object at 0x7ff62888cb80>", "http://cisco.com/ns/cisco-xe-ietf-ospf-deviation?module=cisco-xe-ietf-ospf-deviation&revision=2018-02-09": "<ncclient.capabilities.Capability object at 0x7ff62888cbe0>", "http://cisco.com/ns/cisco-xe-ietf-routing-deviation?module=cisco-xe-ietf-routing-deviation&revision=2016-07-09": "<ncclient.capabilities.Capability object at 0x7ff62888cc40>", "http://cisco.com/ns/cisco-xe-openconfig-acl-deviation?module=cisco-xe-openconfig-acl-deviation&revision=2017-08-25": "<ncclient.capabilities.Capability object at 0x7ff62888cca0>", "http://cisco.com/ns/mpls-static/devs?module=common-mpls-static-devs&revision=2015-09-11": "<ncclient.capabilities.Capability object at 0x7ff62888cd00>", "http://cisco.com/ns/nvo/devs?module=nvo-devs&revision=2015-09-11": "<ncclient.capabilities.Capability object at 0x7ff62888cd60>", "http://cisco.com/ns/yang/Cisco-IOS-XE-aaa?module=Cisco-IOS-XE-aaa&revision=2018-12-07": "<ncclient.capabilities.Capability object at 0x7ff62888cdc0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-aaa-oper?module=Cisco-IOS-XE-aaa-oper&revision=2018-04-16": "<ncclient.capabilities.Capability object at 0x7ff62888ce20>", "http://cisco.com/ns/yang/Cisco-IOS-XE-acl?module=Cisco-IOS-XE-acl&revision=2020-01-15": "<ncclient.capabilities.Capability object at 0x7ff62888ce80>", "http://cisco.com/ns/yang/Cisco-IOS-XE-acl-oper?module=Cisco-IOS-XE-acl-oper&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff62888cee0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-arp?module=Cisco-IOS-XE-arp&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff62888cf40>", "http://cisco.com/ns/yang/Cisco-IOS-XE-arp-oper?module=Cisco-IOS-XE-arp-oper&revision=2017-12-13": "<ncclient.capabilities.Capability object at 0x7ff62888cfa0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-atm?module=Cisco-IOS-XE-atm&revision=2018-03-28": "<ncclient.capabilities.Capability object at 0x7ff62888ca90>", "http://cisco.com/ns/yang/Cisco-IOS-XE-bba-group?module=Cisco-IOS-XE-bba-group&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff62888caf0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-bfd?module=Cisco-IOS-XE-bfd&revision=2018-10-10": "<ncclient.capabilities.Capability object at 0x7ff62881d100>", "http://cisco.com/ns/yang/Cisco-IOS-XE-bfd-oper?module=Cisco-IOS-XE-bfd-oper&revision=2017-09-10": "<ncclient.capabilities.Capability object at 0x7ff62881d160>", "http://cisco.com/ns/yang/Cisco-IOS-XE-bgp?module=Cisco-IOS-XE-bgp&revision=2019-01-09": "<ncclient.capabilities.Capability object at 0x7ff62881d1c0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-bgp-common-oper?module=Cisco-IOS-XE-bgp-common-oper&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff62881d220>", "http://cisco.com/ns/yang/Cisco-IOS-XE-bgp-oper?module=Cisco-IOS-XE-bgp-oper&revision=2017-09-25": "<ncclient.capabilities.Capability object at 0x7ff62881d280>", "http://cisco.com/ns/yang/Cisco-IOS-XE-bgp-route-oper?module=Cisco-IOS-XE-bgp-route-oper&revision=2017-09-25": "<ncclient.capabilities.Capability object at 0x7ff62881d2e0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-bridge-domain?module=Cisco-IOS-XE-bridge-domain&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff62881d340>", "http://cisco.com/ns/yang/Cisco-IOS-XE-bridge-oper?module=Cisco-IOS-XE-bridge-oper&revision=2018-03-10": "<ncclient.capabilities.Capability object at 0x7ff62881d3a0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-call-home?module=Cisco-IOS-XE-call-home&revision=2018-10-11": "<ncclient.capabilities.Capability object at 0x7ff62881d400>", "http://cisco.com/ns/yang/Cisco-IOS-XE-card?module=Cisco-IOS-XE-card&revision=2018-03-27": "<ncclient.capabilities.Capability object at 0x7ff62881d460>", "http://cisco.com/ns/yang/Cisco-IOS-XE-cdp?module=Cisco-IOS-XE-cdp&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff62881d4c0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper?module=Cisco-IOS-XE-cdp-oper&revision=2017-09-21": "<ncclient.capabilities.Capability object at 0x7ff62881d520>", "http://cisco.com/ns/yang/Cisco-IOS-XE-cef?module=Cisco-IOS-XE-cef&revision=2017-05-19&features=asr1k-dpi": "<ncclient.capabilities.Capability object at 0x7ff62881d580>", "http://cisco.com/ns/yang/Cisco-IOS-XE-cellular?module=Cisco-IOS-XE-cellular&revision=2017-12-20": "<ncclient.capabilities.Capability object at 0x7ff62881d040>", "http://cisco.com/ns/yang/Cisco-IOS-XE-cellwan-oper?module=Cisco-IOS-XE-cellwan-oper&revision=2018-05-18": "<ncclient.capabilities.Capability object at 0x7ff62881d640>", "http://cisco.com/ns/yang/Cisco-IOS-XE-cfm-oper?module=Cisco-IOS-XE-cfm-oper&revision=2017-06-06": "<ncclient.capabilities.Capability object at 0x7ff62881d6a0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-checkpoint-archive-oper?module=Cisco-IOS-XE-checkpoint-archive-oper&revision=2017-04-01": "<ncclient.capabilities.Capability object at 0x7ff62881d700>", "http://cisco.com/ns/yang/Cisco-IOS-XE-common-types?module=Cisco-IOS-XE-common-types&revision=2017-12-01": "<ncclient.capabilities.Capability object at 0x7ff62881d760>", "http://cisco.com/ns/yang/Cisco-IOS-XE-controller?module=Cisco-IOS-XE-controller&revision=2018-04-02": "<ncclient.capabilities.Capability object at 0x7ff62881d7c0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-controller-vdsl-oper?module=Cisco-IOS-XE-controller-vdsl-oper&revision=2018-01-31": "<ncclient.capabilities.Capability object at 0x7ff62881d820>", "http://cisco.com/ns/yang/Cisco-IOS-XE-crypto?module=Cisco-IOS-XE-crypto&revision=2019-04-25": "<ncclient.capabilities.Capability object at 0x7ff62881d880>", "http://cisco.com/ns/yang/Cisco-IOS-XE-cts?module=Cisco-IOS-XE-cts&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff62881d8e0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-device-hardware-oper?module=Cisco-IOS-XE-device-hardware-oper&revision=2017-11-01": "<ncclient.capabilities.Capability object at 0x7ff62881d940>", "http://cisco.com/ns/yang/Cisco-IOS-XE-device-tracking?module=Cisco-IOS-XE-device-tracking&revision=2018-01-29": "<ncclient.capabilities.Capability object at 0x7ff62881d9a0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp?module=Cisco-IOS-XE-dhcp&revision=2019-01-04": "<ncclient.capabilities.Capability object at 0x7ff62881da00>", "http://cisco.com/ns/yang/Cisco-IOS-XE-dhcp-oper?module=Cisco-IOS-XE-dhcp-oper&revision=2018-02-13": "<ncclient.capabilities.Capability object at 0x7ff62881da60>", "http://cisco.com/ns/yang/Cisco-IOS-XE-diagnostics?module=Cisco-IOS-XE-diagnostics&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff62881dac0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-dot1x?module=Cisco-IOS-XE-dot1x&revision=2018-01-30": "<ncclient.capabilities.Capability object at 0x7ff62881db20>", "http://cisco.com/ns/yang/Cisco-IOS-XE-eem?module=Cisco-IOS-XE-eem&revision=2017-12-20": "<ncclient.capabilities.Capability object at 0x7ff62881db80>", "http://cisco.com/ns/yang/Cisco-IOS-XE-efp-oper?module=Cisco-IOS-XE-efp-oper&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff62881dbe0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-eigrp?module=Cisco-IOS-XE-eigrp&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff62881dc40>", "http://cisco.com/ns/yang/Cisco-IOS-XE-environment-oper?module=Cisco-IOS-XE-environment-oper&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff62881dca0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-eta?module=Cisco-IOS-XE-eta&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff62881dd00>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet?module=Cisco-IOS-XE-ethernet&revision=2018-07-25": "<ncclient.capabilities.Capability object at 0x7ff62881dd60>", "http://cisco.com/ns/yang/Cisco-IOS-XE-event-history-types?module=Cisco-IOS-XE-event-history-types&revision=2018-03-20": "<ncclient.capabilities.Capability object at 0x7ff62881ddc0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ezpm?module=Cisco-IOS-XE-ezpm&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff62881de20>", "http://cisco.com/ns/yang/Cisco-IOS-XE-features?module=Cisco-IOS-XE-features&revision=2017-02-07&features=virtual-template,switching-platform,punt-num,parameter-map,multilink,l2vpn,l2,eth-evc,esmc,efp,dot1x,crypto": "<ncclient.capabilities.Capability object at 0x7ff62881de80>", "http://cisco.com/ns/yang/Cisco-IOS-XE-fib-oper?module=Cisco-IOS-XE-fib-oper&revision=2018-03-07": "<ncclient.capabilities.Capability object at 0x7ff62881d5e0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-flow?module=Cisco-IOS-XE-flow&revision=2018-01-04": "<ncclient.capabilities.Capability object at 0x7ff62881df40>", "http://cisco.com/ns/yang/Cisco-IOS-XE-flow-monitor-oper?module=Cisco-IOS-XE-flow-monitor-oper&revision=2017-11-30": "<ncclient.capabilities.Capability object at 0x7ff62881dfa0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-fw-oper?module=Cisco-IOS-XE-fw-oper&revision=2018-02-22": "<ncclient.capabilities.Capability object at 0x7ff62881d0d0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-http?module=Cisco-IOS-XE-http&revision=2018-01-24": "<ncclient.capabilities.Capability object at 0x7ff62881df10>", "http://cisco.com/ns/yang/Cisco-IOS-XE-icmp?module=Cisco-IOS-XE-icmp&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628833100>", "http://cisco.com/ns/yang/Cisco-IOS-XE-igmp?module=Cisco-IOS-XE-igmp&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628833160>", "http://cisco.com/ns/yang/Cisco-IOS-XE-interface-common?module=Cisco-IOS-XE-interface-common&revision=2018-02-08": "<ncclient.capabilities.Capability object at 0x7ff6288331c0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper?module=Cisco-IOS-XE-interfaces-oper&revision=2018-02-01": "<ncclient.capabilities.Capability object at 0x7ff628833220>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ios-common-oper?module=Cisco-IOS-XE-ios-common-oper&revision=2018-01-04": "<ncclient.capabilities.Capability object at 0x7ff628833280>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ip-sla-oper?module=Cisco-IOS-XE-ip-sla-oper&revision=2017-09-25": "<ncclient.capabilities.Capability object at 0x7ff6288332e0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ipv6-oper?module=Cisco-IOS-XE-ipv6-oper&revision=2017-11-01": "<ncclient.capabilities.Capability object at 0x7ff628833340>", "http://cisco.com/ns/yang/Cisco-IOS-XE-isis?module=Cisco-IOS-XE-isis&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff6288333a0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-iwanfabric?module=Cisco-IOS-XE-iwanfabric&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628833400>", "http://cisco.com/ns/yang/Cisco-IOS-XE-l2vpn?module=Cisco-IOS-XE-l2vpn&revision=2018-02-13": "<ncclient.capabilities.Capability object at 0x7ff628833460>", "http://cisco.com/ns/yang/Cisco-IOS-XE-linecard-oper?module=Cisco-IOS-XE-linecard-oper&revision=2018-03-26": "<ncclient.capabilities.Capability object at 0x7ff6288334c0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-lisp?module=Cisco-IOS-XE-lisp&revision=2018-04-17": "<ncclient.capabilities.Capability object at 0x7ff628833520>", "http://cisco.com/ns/yang/Cisco-IOS-XE-lisp-oper?module=Cisco-IOS-XE-lisp-oper&revision=2018-02-01": "<ncclient.capabilities.Capability object at 0x7ff628833580>", "http://cisco.com/ns/yang/Cisco-IOS-XE-lldp?module=Cisco-IOS-XE-lldp&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff6288335e0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-lldp-oper?module=Cisco-IOS-XE-lldp-oper&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff628833640>", "http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-cfg?module=Cisco-IOS-XE-mdt-cfg&revision=2018-02-12": "<ncclient.capabilities.Capability object at 0x7ff6288336a0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-common-defs?module=Cisco-IOS-XE-mdt-common-defs&revision=2018-02-12": "<ncclient.capabilities.Capability object at 0x7ff628833700>", "http://cisco.com/ns/yang/Cisco-IOS-XE-mdt-oper?module=Cisco-IOS-XE-mdt-oper&revision=2018-03-06": "<ncclient.capabilities.Capability object at 0x7ff628833760>", "http://cisco.com/ns/yang/Cisco-IOS-XE-memory-oper?module=Cisco-IOS-XE-memory-oper&revision=2017-04-01": "<ncclient.capabilities.Capability object at 0x7ff6288337c0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-mka?module=Cisco-IOS-XE-mka&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628833820>", "http://cisco.com/ns/yang/Cisco-IOS-XE-mld?module=Cisco-IOS-XE-mld&revision=2018-02-12": "<ncclient.capabilities.Capability object at 0x7ff628833880>", "http://cisco.com/ns/yang/Cisco-IOS-XE-mpls?module=Cisco-IOS-XE-mpls&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff6288338e0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-mpls-forwarding-oper?module=Cisco-IOS-XE-mpls-forwarding-oper&revision=2017-11-01": "<ncclient.capabilities.Capability object at 0x7ff628833940>", "http://cisco.com/ns/yang/Cisco-IOS-XE-multicast?module=Cisco-IOS-XE-multicast&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff6288339a0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-nam?module=Cisco-IOS-XE-nam&revision=2017-12-28": "<ncclient.capabilities.Capability object at 0x7ff628833a00>", "http://cisco.com/ns/yang/Cisco-IOS-XE-nat?module=Cisco-IOS-XE-nat&revision=2018-12-18": "<ncclient.capabilities.Capability object at 0x7ff628833a60>", "http://cisco.com/ns/yang/Cisco-IOS-XE-nat-oper?module=Cisco-IOS-XE-nat-oper&revision=2018-03-17": "<ncclient.capabilities.Capability object at 0x7ff628833ac0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-native?module=Cisco-IOS-XE-native&revision=2018-07-27": "<ncclient.capabilities.Capability object at 0x7ff628833b20>", "http://cisco.com/ns/yang/Cisco-IOS-XE-nbar?module=Cisco-IOS-XE-nbar&revision=2018-06-06": "<ncclient.capabilities.Capability object at 0x7ff628833b80>", "http://cisco.com/ns/yang/Cisco-IOS-XE-nd?module=Cisco-IOS-XE-nd&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628833be0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-nhrp?module=Cisco-IOS-XE-nhrp&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff628833c40>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ntp?module=Cisco-IOS-XE-ntp&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff628833ca0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ntp-oper?module=Cisco-IOS-XE-ntp-oper&revision=2018-01-16": "<ncclient.capabilities.Capability object at 0x7ff628833d00>", "http://cisco.com/ns/yang/Cisco-IOS-XE-object-group?module=Cisco-IOS-XE-object-group&revision=2017-07-31": "<ncclient.capabilities.Capability object at 0x7ff628833d60>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ospf?module=Cisco-IOS-XE-ospf&revision=2018-10-08": "<ncclient.capabilities.Capability object at 0x7ff628833dc0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-oper?module=Cisco-IOS-XE-ospf-oper&revision=2018-02-01": "<ncclient.capabilities.Capability object at 0x7ff628833e20>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ospfv3?module=Cisco-IOS-XE-ospfv3&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff628833e80>", "http://cisco.com/ns/yang/Cisco-IOS-XE-otv?module=Cisco-IOS-XE-otv&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff628833ee0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-pathmgr?module=Cisco-IOS-XE-pathmgr&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff628833f40>", "http://cisco.com/ns/yang/Cisco-IOS-XE-platform?module=Cisco-IOS-XE-platform&revision=2018-11-14": "<ncclient.capabilities.Capability object at 0x7ff628833fa0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-platform-oper?module=Cisco-IOS-XE-platform-oper&revision=2017-10-11": "<ncclient.capabilities.Capability object at 0x7ff6288330d0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-platform-software-oper?module=Cisco-IOS-XE-platform-software-oper&revision=2018-03-09": "<ncclient.capabilities.Capability object at 0x7ff628833070>", "http://cisco.com/ns/yang/Cisco-IOS-XE-pnp?module=Cisco-IOS-XE-pnp&revision=2018-07-10": "<ncclient.capabilities.Capability object at 0x7ff628844100>", "http://cisco.com/ns/yang/Cisco-IOS-XE-policy?module=Cisco-IOS-XE-policy&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff628844160>", "http://cisco.com/ns/yang/Cisco-IOS-XE-power?module=Cisco-IOS-XE-power&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff6288441c0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ppp?module=Cisco-IOS-XE-ppp&revision=2018-02-03": "<ncclient.capabilities.Capability object at 0x7ff628844220>", "http://cisco.com/ns/yang/Cisco-IOS-XE-ppp-oper?module=Cisco-IOS-XE-ppp-oper&revision=2018-02-19": "<ncclient.capabilities.Capability object at 0x7ff628844280>", "http://cisco.com/ns/yang/Cisco-IOS-XE-process-cpu-oper?module=Cisco-IOS-XE-process-cpu-oper&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff6288442e0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-process-memory-oper?module=Cisco-IOS-XE-process-memory-oper&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff628844340>", "http://cisco.com/ns/yang/Cisco-IOS-XE-qos?module=Cisco-IOS-XE-qos&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff6288443a0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-rip?module=Cisco-IOS-XE-rip&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff628844400>", "http://cisco.com/ns/yang/Cisco-IOS-XE-route-map?module=Cisco-IOS-XE-route-map&revision=2018-12-05": "<ncclient.capabilities.Capability object at 0x7ff628844460>", "http://cisco.com/ns/yang/Cisco-IOS-XE-rpc?module=Cisco-IOS-XE-rpc&revision=2018-04-18": "<ncclient.capabilities.Capability object at 0x7ff6288444c0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-rsvp?module=Cisco-IOS-XE-rsvp&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628844520>", "http://cisco.com/ns/yang/Cisco-IOS-XE-sanet?module=Cisco-IOS-XE-sanet&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628844580>", "http://cisco.com/ns/yang/Cisco-IOS-XE-segment-routing?module=Cisco-IOS-XE-segment-routing&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff6288445e0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-service-discovery?module=Cisco-IOS-XE-service-discovery&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff628844640>", "http://cisco.com/ns/yang/Cisco-IOS-XE-service-insertion?module=Cisco-IOS-XE-service-insertion&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff6288446a0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-service-routing?module=Cisco-IOS-XE-service-routing&revision=2017-07-24": "<ncclient.capabilities.Capability object at 0x7ff628844700>", "http://cisco.com/ns/yang/Cisco-IOS-XE-sla?module=Cisco-IOS-XE-sla&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff628844760>", "http://cisco.com/ns/yang/Cisco-IOS-XE-snmp?module=Cisco-IOS-XE-snmp&revision=2018-06-28": "<ncclient.capabilities.Capability object at 0x7ff6288447c0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-spanning-tree?module=Cisco-IOS-XE-spanning-tree&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628844820>", "http://cisco.com/ns/yang/Cisco-IOS-XE-switch?module=Cisco-IOS-XE-switch&revision=2018-01-10": "<ncclient.capabilities.Capability object at 0x7ff628844880>", "http://cisco.com/ns/yang/Cisco-IOS-XE-track?module=Cisco-IOS-XE-track&revision=2018-08-10": "<ncclient.capabilities.Capability object at 0x7ff6288448e0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-transceiver-oper?module=Cisco-IOS-XE-transceiver-oper&revision=2018-01-18": "<ncclient.capabilities.Capability object at 0x7ff628844940>", "http://cisco.com/ns/yang/Cisco-IOS-XE-trustsec-oper?module=Cisco-IOS-XE-trustsec-oper&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff6288449a0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-tunnel?module=Cisco-IOS-XE-tunnel&revision=2017-08-28": "<ncclient.capabilities.Capability object at 0x7ff628844a00>", "http://cisco.com/ns/yang/Cisco-IOS-XE-types?module=Cisco-IOS-XE-types&revision=2018-05-22": "<ncclient.capabilities.Capability object at 0x7ff628844a60>", "http://cisco.com/ns/yang/Cisco-IOS-XE-umbrella?module=Cisco-IOS-XE-umbrella&revision=2018-05-14": "<ncclient.capabilities.Capability object at 0x7ff628844ac0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-utd?module=Cisco-IOS-XE-utd&revision=2018-07-11": "<ncclient.capabilities.Capability object at 0x7ff628844b20>", "http://cisco.com/ns/yang/Cisco-IOS-XE-utd-common-oper?module=Cisco-IOS-XE-utd-common-oper&revision=2018-04-04": "<ncclient.capabilities.Capability object at 0x7ff628844b80>", "http://cisco.com/ns/yang/Cisco-IOS-XE-utd-oper?module=Cisco-IOS-XE-utd-oper&revision=2018-04-04": "<ncclient.capabilities.Capability object at 0x7ff628844be0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-cfg?module=Cisco-IOS-XE-virtual-service-cfg&revision=2018-01-01": "<ncclient.capabilities.Capability object at 0x7ff628844c40>", "http://cisco.com/ns/yang/Cisco-IOS-XE-virtual-service-oper?module=Cisco-IOS-XE-virtual-service-oper&revision=2018-02-01": "<ncclient.capabilities.Capability object at 0x7ff628844ca0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-vlan?module=Cisco-IOS-XE-vlan&revision=2018-03-13": "<ncclient.capabilities.Capability object at 0x7ff628844d00>", "http://cisco.com/ns/yang/Cisco-IOS-XE-voice?module=Cisco-IOS-XE-voice&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff628844d60>", "http://cisco.com/ns/yang/Cisco-IOS-XE-vpdn?module=Cisco-IOS-XE-vpdn&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff628844dc0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-vrrp?module=Cisco-IOS-XE-vrrp&revision=2018-08-15": "<ncclient.capabilities.Capability object at 0x7ff628844e20>", "http://cisco.com/ns/yang/Cisco-IOS-XE-vrrp-oper?module=Cisco-IOS-XE-vrrp-oper&revision=2018-05-10": "<ncclient.capabilities.Capability object at 0x7ff628844e80>", "http://cisco.com/ns/yang/Cisco-IOS-XE-vservice?module=Cisco-IOS-XE-vservice&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628844ee0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-vtp?module=Cisco-IOS-XE-vtp&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff628844f40>", "http://cisco.com/ns/yang/Cisco-IOS-XE-wccp?module=Cisco-IOS-XE-wccp&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff628844fa0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-wsma?module=Cisco-IOS-XE-wsma&revision=2017-02-07": "<ncclient.capabilities.Capability object at 0x7ff6288440d0>", "http://cisco.com/ns/yang/Cisco-IOS-XE-zone?module=Cisco-IOS-XE-zone&revision=2018-06-12": "<ncclient.capabilities.Capability object at 0x7ff628844070>", "http://cisco.com/ns/yang/cisco-smart-license?module=cisco-smart-license&revision=2017-10-11": "<ncclient.capabilities.Capability object at 0x7ff62884c100>", "http://cisco.com/ns/yang/cisco-xe-bgp-policy-deviation?module=cisco-xe-openconfig-bgp-policy-deviation&revision=2017-07-24": "<ncclient.capabilities.Capability object at 0x7ff62884c160>", "http://cisco.com/ns/yang/cisco-xe-ietf-event-notifications-deviation?module=cisco-xe-ietf-event-notifications-deviation&revision=2017-08-22": "<ncclient.capabilities.Capability object at 0x7ff62884c1c0>", "http://cisco.com/ns/yang/cisco-xe-ietf-yang-push-deviation?module=cisco-xe-ietf-yang-push-deviation&revision=2017-08-22": "<ncclient.capabilities.Capability object at 0x7ff62884c220>", "http://cisco.com/ns/yang/cisco-xe-openconfig-acl-ext?module=cisco-xe-openconfig-acl-ext&revision=2017-03-30": "<ncclient.capabilities.Capability object at 0x7ff62884c280>", "http://cisco.com/ns/yang/cisco-xe-openconfig-bgp-deviation?module=cisco-xe-openconfig-bgp-deviation&revision=2017-05-24": "<ncclient.capabilities.Capability object at 0x7ff62884c2e0>", "http://cisco.com/ns/yang/cisco-xe-openconfig-if-ethernet-ext?module=cisco-xe-openconfig-if-ethernet-ext&revision=2017-10-30": "<ncclient.capabilities.Capability object at 0x7ff62884c340>", "http://cisco.com/ns/yang/cisco-xe-openconfig-interfaces-ext?module=cisco-xe-openconfig-interfaces-ext&revision=2017-03-05": "<ncclient.capabilities.Capability object at 0x7ff62884c3a0>", "http://cisco.com/ns/yang/cisco-xe-openconfig-network-instance-deviation?module=cisco-xe-openconfig-network-instance-deviation&revision=2017-02-14": "<ncclient.capabilities.Capability object at 0x7ff62884c400>", "http://cisco.com/ns/yang/cisco-xe-openconfig-platform-ext?module=cisco-xe-openconfig-platform-ext&revision=2018-02-05": "<ncclient.capabilities.Capability object at 0x7ff62884c460>", "http://cisco.com/ns/yang/cisco-xe-openconfig-rib-bgp-ext?module=cisco-xe-openconfig-rib-bgp-ext&revision=2016-11-30": "<ncclient.capabilities.Capability object at 0x7ff62884c4c0>", "http://cisco.com/ns/yang/cisco-xe-openconfig-system-ext?module=cisco-xe-openconfig-system-ext&revision=2018-03-21": "<ncclient.capabilities.Capability object at 0x7ff62884c520>", "http://cisco.com/ns/yang/cisco-xe-openconfig-vlan-deviation?module=cisco-xe-openconfig-vlan-deviation&revision=2018-10-09": "<ncclient.capabilities.Capability object at 0x7ff62884c580>", "http://cisco.com/ns/yang/cisco-xe-routing-policy-deviation?module=cisco-xe-openconfig-routing-policy-deviation&revision=2017-03-30": "<ncclient.capabilities.Capability object at 0x7ff62884c5e0>", "http://cisco.com/ns/yang/ios-xe/template?module=Cisco-IOS-XE-template&revision=2017-11-06": "<ncclient.capabilities.Capability object at 0x7ff62884c640>", "http://cisco.com/yang/cisco-ia?module=cisco-ia&revision=2018-08-03": "<ncclient.capabilities.Capability object at 0x7ff62884c6a0>", "http://cisco.com/yang/cisco-self-mgmt?module=cisco-self-mgmt&revision=2016-05-14": "<ncclient.capabilities.Capability object at 0x7ff62884c700>", "http://openconfig.net/yang/aaa?module=openconfig-aaa&revision=2017-09-18": "<ncclient.capabilities.Capability object at 0x7ff62884c760>", "http://openconfig.net/yang/aaa/types?module=openconfig-aaa-types&revision=2017-09-18": "<ncclient.capabilities.Capability object at 0x7ff62884c7c0>", "http://openconfig.net/yang/acl?module=openconfig-acl&revision=2017-05-26&deviations=cisco-xe-openconfig-acl-deviation": "<ncclient.capabilities.Capability object at 0x7ff62884c820>", "http://openconfig.net/yang/alarms?module=openconfig-alarms&revision=2017-08-24": "<ncclient.capabilities.Capability object at 0x7ff62884c040>", "http://openconfig.net/yang/bgp?module=openconfig-bgp&revision=2016-06-21": "<ncclient.capabilities.Capability object at 0x7ff62884c8e0>", "http://openconfig.net/yang/bgp-policy?module=openconfig-bgp-policy&revision=2016-06-21&deviations=cisco-xe-openconfig-bgp-policy-deviation": "<ncclient.capabilities.Capability object at 0x7ff62884c940>", "http://openconfig.net/yang/bgp-types?module=openconfig-bgp-types&revision=2016-06-21": "<ncclient.capabilities.Capability object at 0x7ff62884c880>", "http://openconfig.net/yang/cisco-xe-openconfig-if-ethernet-deviation?module=cisco-xe-openconfig-if-ethernet-deviation&revision=2017-11-01": "<ncclient.capabilities.Capability object at 0x7ff62884ca00>", "http://openconfig.net/yang/cisco-xe-openconfig-if-ip-deviation?module=cisco-xe-openconfig-if-ip-deviation&revision=2017-03-04": "<ncclient.capabilities.Capability object at 0x7ff62884ca60>", "http://openconfig.net/yang/cisco-xe-openconfig-interfaces-deviation?module=cisco-xe-openconfig-interfaces-deviation&revision=2018-03-27": "<ncclient.capabilities.Capability object at 0x7ff62884cac0>", "http://openconfig.net/yang/cisco-xe-openconfig-system-deviation?module=cisco-xe-openconfig-system-deviation&revision=2017-11-27": "<ncclient.capabilities.Capability object at 0x7ff62884cb20>", "http://openconfig.net/yang/header-fields?module=openconfig-packet-match&revision=2017-05-26": "<ncclient.capabilities.Capability object at 0x7ff62884cb80>", "http://openconfig.net/yang/interfaces?module=openconfig-interfaces&revision=2018-01-05&deviations=cisco-xe-openconfig-interfaces-deviation": "<ncclient.capabilities.Capability object at 0x7ff62884cbe0>", "http://openconfig.net/yang/interfaces/aggregate?module=openconfig-if-aggregate&revision=2018-01-05": "<ncclient.capabilities.Capability object at 0x7ff62884c9a0>", "http://openconfig.net/yang/interfaces/ethernet?module=openconfig-if-ethernet&revision=2018-01-05&deviations=cisco-xe-openconfig-if-ethernet-deviation": "<ncclient.capabilities.Capability object at 0x7ff62884cca0>", "http://openconfig.net/yang/interfaces/ip?module=openconfig-if-ip&revision=2018-01-05&deviations=cisco-xe-openconfig-if-ip-deviation,cisco-xe-openconfig-interfaces-deviation": "<ncclient.capabilities.Capability object at 0x7ff62884cc40>", "http://openconfig.net/yang/interfaces/ip-ext?module=openconfig-if-ip-ext&revision=2018-01-05": "<ncclient.capabilities.Capability object at 0x7ff62884cd00>", "http://openconfig.net/yang/local-routing?module=openconfig-local-routing&revision=2016-05-11": "<ncclient.capabilities.Capability object at 0x7ff62884cdc0>", "http://openconfig.net/yang/network-instance?module=openconfig-network-instance&revision=2017-01-13&deviations=cisco-xe-openconfig-bgp-deviation,cisco-xe-openconfig-network-instance-deviation": "<ncclient.capabilities.Capability object at 0x7ff62884ce20>", "http://openconfig.net/yang/network-instance-l3?module=openconfig-network-instance-l3&revision=2017-01-13": "<ncclient.capabilities.Capability object at 0x7ff62884cd60>", "http://openconfig.net/yang/network-instance-types?module=openconfig-network-instance-types&revision=2016-12-15": "<ncclient.capabilities.Capability object at 0x7ff62884cee0>", "http://openconfig.net/yang/openconfig-ext?module=openconfig-extensions&revision=2017-04-11": "<ncclient.capabilities.Capability object at 0x7ff62884cf40>", "http://openconfig.net/yang/openconfig-types?module=openconfig-types&revision=2018-01-16": "<ncclient.capabilities.Capability object at 0x7ff62884cfa0>", "http://openconfig.net/yang/packet-match-types?module=openconfig-packet-match-types&revision=2017-05-26": "<ncclient.capabilities.Capability object at 0x7ff62884c0d0>", "http://openconfig.net/yang/platform?module=openconfig-platform&revision=2016-12-22": "<ncclient.capabilities.Capability object at 0x7ff62884ceb0>", "http://openconfig.net/yang/platform-types?module=openconfig-platform-types&revision=2017-08-16": "<ncclient.capabilities.Capability object at 0x7ff628854100>", "http://openconfig.net/yang/platform/linecard?module=openconfig-platform-linecard&revision=2017-08-03": "<ncclient.capabilities.Capability object at 0x7ff628854160>", "http://openconfig.net/yang/platform/port?module=openconfig-platform-port&revision=2016-10-24": "<ncclient.capabilities.Capability object at 0x7ff6288541c0>", "http://openconfig.net/yang/platform/transceiver?module=openconfig-platform-transceiver&revision=2017-09-18": "<ncclient.capabilities.Capability object at 0x7ff628854220>", "http://openconfig.net/yang/policy-types?module=openconfig-policy-types&revision=2016-05-12": "<ncclient.capabilities.Capability object at 0x7ff628854280>", "http://openconfig.net/yang/rib/bgp?module=openconfig-rib-bgp&revision=2017-03-07": "<ncclient.capabilities.Capability object at 0x7ff6288542e0>", "http://openconfig.net/yang/rib/bgp-ext?module=openconfig-rib-bgp-ext&revision=2016-04-11": "<ncclient.capabilities.Capability object at 0x7ff628854340>", "http://openconfig.net/yang/rib/bgp-types?module=openconfig-rib-bgp-types&revision=2016-04-11": "<ncclient.capabilities.Capability object at 0x7ff6288543a0>", "http://openconfig.net/yang/routing-policy?module=openconfig-routing-policy&revision=2016-05-12&deviations=cisco-xe-openconfig-routing-policy-deviation": "<ncclient.capabilities.Capability object at 0x7ff628854400>", "http://openconfig.net/yang/system?module=openconfig-system&revision=2018-01-21&deviations=cisco-xe-openconfig-system-deviation": "<ncclient.capabilities.Capability object at 0x7ff628854040>", "http://openconfig.net/yang/system/logging?module=openconfig-system-logging&revision=2017-09-18": "<ncclient.capabilities.Capability object at 0x7ff628854460>", "http://openconfig.net/yang/system/procmon?module=openconfig-procmon&revision=2017-09-18": "<ncclient.capabilities.Capability object at 0x7ff628854520>", "http://openconfig.net/yang/system/terminal?module=openconfig-system-terminal&revision=2017-09-18": "<ncclient.capabilities.Capability object at 0x7ff628854580>", "http://openconfig.net/yang/transport-line-common?module=openconfig-transport-line-common&revision=2016-03-31": "<ncclient.capabilities.Capability object at 0x7ff6288545e0>", "http://openconfig.net/yang/transport-types?module=openconfig-transport-types&revision=2017-08-16": "<ncclient.capabilities.Capability object at 0x7ff628854640>", "http://openconfig.net/yang/types/inet?module=openconfig-inet-types&revision=2017-08-24": "<ncclient.capabilities.Capability object at 0x7ff6288546a0>", "http://openconfig.net/yang/types/yang?module=openconfig-yang-types&revision=2017-07-30": "<ncclient.capabilities.Capability object at 0x7ff628854700>", "http://openconfig.net/yang/vlan?module=openconfig-vlan&revision=2016-05-26&deviations=cisco-xe-openconfig-vlan-deviation": "<ncclient.capabilities.Capability object at 0x7ff628854760>", "http://openconfig.net/yang/vlan-types?module=openconfig-vlan-types&revision=2016-05-26": "<ncclient.capabilities.Capability object at 0x7ff6288544c0>", "http://tail-f.com/ns/common/query?module=tailf-common-query&revision=2017-12-15": "<ncclient.capabilities.Capability object at 0x7ff628854820>", "http://tail-f.com/yang/common?module=tailf-common&revision=2018-09-11": "<ncclient.capabilities.Capability object at 0x7ff628854880>", "http://tail-f.com/yang/common-monitoring?module=tailf-common-monitoring&revision=2013-06-14": "<ncclient.capabilities.Capability object at 0x7ff6288548e0>", "http://tail-f.com/yang/confd-monitoring?module=tailf-confd-monitoring&revision=2013-06-14": "<ncclient.capabilities.Capability object at 0x7ff628854940>", "http://tail-f.com/yang/netconf-monitoring?module=tailf-netconf-monitoring&revision=2016-11-24": "<ncclient.capabilities.Capability object at 0x7ff6288549a0>", "urn:cisco:params:xml:ns:yang:cisco-bridge-common?module=cisco-bridge-common&revision=2016-12-14&features=configurable-bd-mac-limit-notif,configurable-bd-mac-limit-max,configurable-bd-mac-limit-actions,configurable-bd-mac-aging-types,configurable-bd-flooding-control": "<ncclient.capabilities.Capability object at 0x7ff628854a00>", "urn:cisco:params:xml:ns:yang:cisco-bridge-domain?module=cisco-bridge-domain&revision=2016-12-14&features=parameterized-bridge-domains,configurable-bd-storm-control,configurable-bd-static-mac,configurable-bd-snooping-profiles,configurable-bd-sh-group-number,configurable-bd-mtu,configurable-bd-member-features,configurable-bd-mac-secure,configurable-bd-mac-features,configurable-bd-mac-event-action,configurable-bd-ipsg,configurable-bd-groups,configurable-bd-flooding-mode,configurable-bd-flooding,configurable-bd-dai,clear-bridge-domain": "<ncclient.capabilities.Capability object at 0x7ff6288547c0>", "urn:cisco:params:xml:ns:yang:cisco-ethernet?module=cisco-ethernet&revision=2016-05-10": "<ncclient.capabilities.Capability object at 0x7ff628854a60>", "urn:cisco:params:xml:ns:yang:cisco-routing-ext?module=cisco-routing-ext&revision=2016-07-09": "<ncclient.capabilities.Capability object at 0x7ff628854b20>", "urn:cisco:params:xml:ns:yang:cisco-storm-control?module=cisco-storm-control&revision=2016-12-14&features=configurable-storm-control-actions": "<ncclient.capabilities.Capability object at 0x7ff628854b80>", "urn:cisco:params:xml:ns:yang:cisco-xe-ietf-yang-push-ext?module=cisco-xe-ietf-yang-push-ext&revision=2017-08-14": "<ncclient.capabilities.Capability object at 0x7ff628854ac0>", "urn:cisco:params:xml:ns:yang:pim?module=pim&revision=2014-06-27&features=bsr,auto-rp": "<ncclient.capabilities.Capability object at 0x7ff628854c40>", "urn:cisco:params:xml:ns:yang:pw?module=cisco-pw&revision=2016-12-07&features=static-label-direct-config,pw-vccv,pw-tag-impose-vlan-id,pw-status-config,pw-static-oam-config,pw-short-config,pw-sequencing,pw-preferred-path,pw-port-profiles,pw-oam-refresh-config,pw-mac-withdraw-config,pw-load-balancing,pw-ipv6-source,pw-interface,pw-grouping-config,pw-class-tag-rewrite,pw-class-switchover-delay,pw-class-status,pw-class-source-ip,pw-class-flow-setting,preferred-path-peer,predictive-redundancy-config,flow-label-tlv-code17,flow-label-static-config": "<ncclient.capabilities.Capability object at 0x7ff628854be0>", "urn:ietf:params:xml:ns:yang:c3pl-types?module=policy-types&revision=2013-10-07&features=protocol-name-support,match-wlan-user-priority-support,match-vpls-support,match-vlan-support,match-vlan-inner-support,match-src-mac-support,match-security-group-support,match-qos-group-support,match-prec-support,match-packet-length-support,match-mpls-exp-top-support,match-mpls-exp-imp-support,match-metadata-support,match-ipv6-acl-support,match-ipv6-acl-name-support,match-ipv4-acl-support,match-ipv4-acl-name-support,match-ip-rtp-support,match-input-interface-support,match-fr-dlci-support,match-fr-de-support,match-flow-record-support,match-flow-ip-support,match-dst-mac-support,match-discard-class-support,match-dei-support,match-dei-inner-support,match-cos-support,match-cos-inner-support,match-class-map-support,match-atm-vci-support,match-atm-clp-support,match-application-support": "<ncclient.capabilities.Capability object at 0x7ff628854ca0>", "urn:ietf:params:xml:ns:yang:cisco-ospf?module=cisco-ospf&revision=2016-03-30&features=graceful-shutdown,flood-reduction,database-filter": "<ncclient.capabilities.Capability object at 0x7ff628854d00>", "urn:ietf:params:xml:ns:yang:cisco-policy?module=cisco-policy&revision=2016-03-30": "<ncclient.capabilities.Capability object at 0x7ff628854d60>", "urn:ietf:params:xml:ns:yang:cisco-policy-filters?module=cisco-policy-filters&revision=2016-03-30": "<ncclient.capabilities.Capability object at 0x7ff628854e20>", "urn:ietf:params:xml:ns:yang:cisco-policy-target?module=cisco-policy-target&revision=2016-03-30": "<ncclient.capabilities.Capability object at 0x7ff628854e80>", "urn:ietf:params:xml:ns:yang:common-mpls-static?module=common-mpls-static&revision=2015-07-22&deviations=common-mpls-static-devs": "<ncclient.capabilities.Capability object at 0x7ff628854ee0>", "urn:ietf:params:xml:ns:yang:common-mpls-types?module=common-mpls-types&revision=2015-05-28": "<ncclient.capabilities.Capability object at 0x7ff628854dc0>", "urn:ietf:params:xml:ns:yang:iana-crypt-hash?module=iana-crypt-hash&revision=2014-08-06&features=crypt-hash-sha-512,crypt-hash-sha-256,crypt-hash-md5": "<ncclient.capabilities.Capability object at 0x7ff628854fa0>", "urn:ietf:params:xml:ns:yang:iana-if-type?module=iana-if-type&revision=2014-05-08": "<ncclient.capabilities.Capability object at 0x7ff628854f40>", "urn:ietf:params:xml:ns:yang:ietf-diffserv-action?module=ietf-diffserv-action&revision=2015-04-07&features=priority-rate-burst-support,hierarchial-policy-support,aqm-red-support": "<ncclient.capabilities.Capability object at 0x7ff6288540d0>", "urn:ietf:params:xml:ns:yang:ietf-diffserv-classifier?module=ietf-diffserv-classifier&revision=2015-04-07&features=policy-inline-classifier-config": "<ncclient.capabilities.Capability object at 0x7ff6287dc0a0>", "urn:ietf:params:xml:ns:yang:ietf-diffserv-policy?module=ietf-diffserv-policy&revision=2015-04-07&features=policy-template-support,hierarchial-policy-support": "<ncclient.capabilities.Capability object at 0x7ff6287dc100>", "urn:ietf:params:xml:ns:yang:ietf-diffserv-target?module=ietf-diffserv-target&revision=2015-04-07&features=target-inline-policy-config": "<ncclient.capabilities.Capability object at 0x7ff6287dc160>", "urn:ietf:params:xml:ns:yang:ietf-event-notifications?module=ietf-event-notifications&revision=2016-10-27&features=json,configured-subscriptions&deviations=cisco-xe-ietf-event-notifications-deviation,cisco-xe-ietf-yang-push-deviation": "<ncclient.capabilities.Capability object at 0x7ff6287dc1c0>", "urn:ietf:params:xml:ns:yang:ietf-inet-types?module=ietf-inet-types&revision=2013-07-15": "<ncclient.capabilities.Capability object at 0x7ff6287dc280>", "urn:ietf:params:xml:ns:yang:ietf-interfaces?module=ietf-interfaces&revision=2014-05-08&features=pre-provisioning,if-mib,arbitrary-names": "<ncclient.capabilities.Capability object at 0x7ff6287dc2e0>", "urn:ietf:params:xml:ns:yang:ietf-interfaces-ext?module=ietf-interfaces-ext": "<ncclient.capabilities.Capability object at 0x7ff6287dc220>", "urn:ietf:params:xml:ns:yang:ietf-ip?module=ietf-ip&revision=2014-06-16&features=ipv6-privacy-autoconf,ipv4-non-contiguous-netmasks&deviations=cisco-xe-ietf-ip-deviation": "<ncclient.capabilities.Capability object at 0x7ff6287dc340>", "urn:ietf:params:xml:ns:yang:ietf-ipv4-unicast-routing?module=ietf-ipv4-unicast-routing&revision=2015-05-25&deviations=cisco-xe-ietf-ipv4-unicast-routing-deviation": "<ncclient.capabilities.Capability object at 0x7ff6287dc400>", "urn:ietf:params:xml:ns:yang:ietf-ipv6-unicast-routing?module=ietf-ipv6-unicast-routing&revision=2015-05-25&deviations=cisco-xe-ietf-ipv6-unicast-routing-deviation": "<ncclient.capabilities.Capability object at 0x7ff6287dc3a0>", "urn:ietf:params:xml:ns:yang:ietf-key-chain?module=ietf-key-chain&revision=2015-02-24&features=independent-send-accept-lifetime,hex-key-string,accept-tolerance": "<ncclient.capabilities.Capability object at 0x7ff6287dc460>", "urn:ietf:params:xml:ns:yang:ietf-netconf-acm?module=ietf-netconf-acm&revision=2012-02-22": "<ncclient.capabilities.Capability object at 0x7ff6287dc4c0>", "urn:ietf:params:xml:ns:yang:ietf-netconf-monitoring?module=ietf-netconf-monitoring&revision=2010-10-04": "<ncclient.capabilities.Capability object at 0x7ff6287dc580>", "urn:ietf:params:xml:ns:yang:ietf-netconf-notifications?module=ietf-netconf-notifications&revision=2012-02-06": "<ncclient.capabilities.Capability object at 0x7ff6287dc5e0>", "urn:ietf:params:xml:ns:yang:ietf-ospf?module=ietf-ospf&revision=2015-03-09&features=ttl-security,te-rid,router-id,remote-lfa,prefix-suppression,ospfv3-authentication-ipsec,nsr,node-flag,multi-topology,multi-area-adj,mtu-ignore,max-lsa,max-ecmp,lls,lfa,ldp-igp-sync,ldp-igp-autoconfig,interface-inheritance,instance-inheritance,graceful-restart,fast-reroute,demand-circuit,bfd,auto-cost,area-inheritance,admin-control&deviations=cisco-xe-ietf-ospf-deviation": "<ncclient.capabilities.Capability object at 0x7ff6287dc640>", "urn:ietf:params:xml:ns:yang:ietf-restconf-monitoring?module=ietf-restconf-monitoring&revision=2017-01-26": "<ncclient.capabilities.Capability object at 0x7ff6287dc6a0>", "urn:ietf:params:xml:ns:yang:ietf-routing?module=ietf-routing&revision=2015-05-25&features=router-id,multiple-ribs&deviations=cisco-xe-ietf-routing-deviation": "<ncclient.capabilities.Capability object at 0x7ff6287dc700>", "urn:ietf:params:xml:ns:yang:ietf-yang-library?module=ietf-yang-library&revision=2016-06-21": "<ncclient.capabilities.Capability object at 0x7ff6287dc760>", "urn:ietf:params:xml:ns:yang:ietf-yang-push?module=ietf-yang-push&revision=2016-10-28&features=on-change&deviations=cisco-xe-ietf-yang-push-deviation": "<ncclient.capabilities.Capability object at 0x7ff6287dc7c0>", "urn:ietf:params:xml:ns:yang:ietf-yang-smiv2?module=ietf-yang-smiv2&revision=2012-06-22": "<ncclient.capabilities.Capability object at 0x7ff6287dc820>", "urn:ietf:params:xml:ns:yang:ietf-yang-types?module=ietf-yang-types&revision=2013-07-15": "<ncclient.capabilities.Capability object at 0x7ff6287dc880>", "urn:ietf:params:xml:ns:yang:nvo?module=nvo&revision=2015-06-02&deviations=nvo-devs": "<ncclient.capabilities.Capability object at 0x7ff6287dc8e0>", "urn:ietf:params:xml:ns:yang:policy-attr?module=policy-attr&revision=2015-04-27": "<ncclient.capabilities.Capability object at 0x7ff6287dc520>", "urn:ietf:params:xml:ns:yang:smiv2:ATM-FORUM-TC-MIB?module=ATM-FORUM-TC-MIB": "<ncclient.capabilities.Capability object at 0x7ff6287dc9a0>", "urn:ietf:params:xml:ns:yang:smiv2:ATM-MIB?module=ATM-MIB&revision=1998-10-19": "<ncclient.capabilities.Capability object at 0x7ff6287dc940>", "urn:ietf:params:xml:ns:yang:smiv2:ATM-TC-MIB?module=ATM-TC-MIB&revision=1998-10-19": "<ncclient.capabilities.Capability object at 0x7ff6287dca60>", "urn:ietf:params:xml:ns:yang:smiv2:BGP4-MIB?module=BGP4-MIB&revision=1994-05-05": "<ncclient.capabilities.Capability object at 0x7ff6287dcac0>", "urn:ietf:params:xml:ns:yang:smiv2:BRIDGE-MIB?module=BRIDGE-MIB&revision=2005-09-19": "<ncclient.capabilities.Capability object at 0x7ff6287dcb20>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-AAA-SERVER-MIB?module=CISCO-AAA-SERVER-MIB&revision=2003-11-17": "<ncclient.capabilities.Capability object at 0x7ff6287dcb80>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-AAA-SESSION-MIB?module=CISCO-AAA-SESSION-MIB&revision=2006-03-21": "<ncclient.capabilities.Capability object at 0x7ff6287dcbe0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-AAL5-MIB?module=CISCO-AAL5-MIB&revision=2003-09-22": "<ncclient.capabilities.Capability object at 0x7ff6287dcc40>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ATM-EXT-MIB?module=CISCO-ATM-EXT-MIB&revision=2003-01-06": "<ncclient.capabilities.Capability object at 0x7ff6287dcca0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ATM-PVCTRAP-EXTN-MIB?module=CISCO-ATM-PVCTRAP-EXTN-MIB&revision=2003-01-20": "<ncclient.capabilities.Capability object at 0x7ff6287dcd00>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ATM-QOS-MIB?module=CISCO-ATM-QOS-MIB&revision=2002-06-10": "<ncclient.capabilities.Capability object at 0x7ff6287dcd60>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-BGP-POLICY-ACCOUNTING-MIB?module=CISCO-BGP-POLICY-ACCOUNTING-MIB&revision=2002-07-26": "<ncclient.capabilities.Capability object at 0x7ff6287dcdc0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-BGP4-MIB?module=CISCO-BGP4-MIB&revision=2010-09-30": "<ncclient.capabilities.Capability object at 0x7ff6287dce20>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-BULK-FILE-MIB?module=CISCO-BULK-FILE-MIB&revision=2002-06-10": "<ncclient.capabilities.Capability object at 0x7ff6287dce80>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-CBP-TARGET-MIB?module=CISCO-CBP-TARGET-MIB&revision=2006-05-24": "<ncclient.capabilities.Capability object at 0x7ff6287dcee0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-CBP-TARGET-TC-MIB?module=CISCO-CBP-TARGET-TC-MIB&revision=2006-03-24": "<ncclient.capabilities.Capability object at 0x7ff6287dcf40>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-CBP-TC-MIB?module=CISCO-CBP-TC-MIB&revision=2008-06-24": "<ncclient.capabilities.Capability object at 0x7ff6287dcfa0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-CDP-MIB?module=CISCO-CDP-MIB&revision=2005-03-21": "<ncclient.capabilities.Capability object at 0x7ff6287dc070>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-CEF-MIB?module=CISCO-CEF-MIB&revision=2006-01-30": "<ncclient.capabilities.Capability object at 0x7ff6287dca30>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-CEF-TC?module=CISCO-CEF-TC&revision=2005-09-30": "<ncclient.capabilities.Capability object at 0x7ff6287e3100>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-COPY-MIB?module=CISCO-CONFIG-COPY-MIB&revision=2005-04-06": "<ncclient.capabilities.Capability object at 0x7ff6287e3160>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONFIG-MAN-MIB?module=CISCO-CONFIG-MAN-MIB&revision=2007-04-27": "<ncclient.capabilities.Capability object at 0x7ff6287e31c0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-CONTEXT-MAPPING-MIB?module=CISCO-CONTEXT-MAPPING-MIB&revision=2008-11-22": "<ncclient.capabilities.Capability object at 0x7ff6287e3220>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-DATA-COLLECTION-MIB?module=CISCO-DATA-COLLECTION-MIB&revision=2002-10-30": "<ncclient.capabilities.Capability object at 0x7ff6287e3280>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-DIAL-CONTROL-MIB?module=CISCO-DIAL-CONTROL-MIB&revision=2005-05-26": "<ncclient.capabilities.Capability object at 0x7ff6287e32e0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-DOT3-OAM-MIB?module=CISCO-DOT3-OAM-MIB&revision=2006-05-31": "<ncclient.capabilities.Capability object at 0x7ff6287e3340>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-DYNAMIC-TEMPLATE-MIB?module=CISCO-DYNAMIC-TEMPLATE-MIB&revision=2007-09-06": "<ncclient.capabilities.Capability object at 0x7ff6287e33a0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-DYNAMIC-TEMPLATE-TC-MIB?module=CISCO-DYNAMIC-TEMPLATE-TC-MIB&revision=2012-01-27": "<ncclient.capabilities.Capability object at 0x7ff6287e3400>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-EIGRP-MIB?module=CISCO-EIGRP-MIB&revision=2004-11-16": "<ncclient.capabilities.Capability object at 0x7ff6287e3460>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-EMBEDDED-EVENT-MGR-MIB?module=CISCO-EMBEDDED-EVENT-MGR-MIB&revision=2006-11-07": "<ncclient.capabilities.Capability object at 0x7ff6287e34c0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENHANCED-MEMPOOL-MIB?module=CISCO-ENHANCED-MEMPOOL-MIB&revision=2008-12-05": "<ncclient.capabilities.Capability object at 0x7ff6287e3520>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-ALARM-MIB?module=CISCO-ENTITY-ALARM-MIB&revision=1999-07-06": "<ncclient.capabilities.Capability object at 0x7ff6287e3580>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-EXT-MIB?module=CISCO-ENTITY-EXT-MIB&revision=2008-11-24": "<ncclient.capabilities.Capability object at 0x7ff6287e35e0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-FRU-CONTROL-MIB?module=CISCO-ENTITY-FRU-CONTROL-MIB&revision=2013-08-19": "<ncclient.capabilities.Capability object at 0x7ff6287e3640>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-QFP-MIB?module=CISCO-ENTITY-QFP-MIB&revision=2014-06-18": "<ncclient.capabilities.Capability object at 0x7ff6287e36a0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-SENSOR-MIB?module=CISCO-ENTITY-SENSOR-MIB&revision=2015-01-15": "<ncclient.capabilities.Capability object at 0x7ff6287e3700>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ENTITY-VENDORTYPE-OID-MIB?module=CISCO-ENTITY-VENDORTYPE-OID-MIB&revision=2014-12-09": "<ncclient.capabilities.Capability object at 0x7ff6287e3760>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ETHER-CFM-MIB?module=CISCO-ETHER-CFM-MIB&revision=2004-12-28": "<ncclient.capabilities.Capability object at 0x7ff6287e37c0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ETHERLIKE-EXT-MIB?module=CISCO-ETHERLIKE-EXT-MIB&revision=2010-06-04": "<ncclient.capabilities.Capability object at 0x7ff6287e3820>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-FIREWALL-TC?module=CISCO-FIREWALL-TC&revision=2006-03-03": "<ncclient.capabilities.Capability object at 0x7ff6287e3880>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-FLASH-MIB?module=CISCO-FLASH-MIB&revision=2013-08-06": "<ncclient.capabilities.Capability object at 0x7ff6287e38e0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-FTP-CLIENT-MIB?module=CISCO-FTP-CLIENT-MIB&revision=2006-03-31": "<ncclient.capabilities.Capability object at 0x7ff6287e3940>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-HSRP-EXT-MIB?module=CISCO-HSRP-EXT-MIB&revision=2010-09-02": "<ncclient.capabilities.Capability object at 0x7ff6287e39a0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-HSRP-MIB?module=CISCO-HSRP-MIB&revision=2010-09-06": "<ncclient.capabilities.Capability object at 0x7ff6287e3a00>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-ATM2-PVCTRAP-MIB?module=CISCO-IETF-ATM2-PVCTRAP-MIB&revision=1998-02-03": "<ncclient.capabilities.Capability object at 0x7ff6287e3a60>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-ATM2-PVCTRAP-MIB-EXTN?module=CISCO-IETF-ATM2-PVCTRAP-MIB-EXTN&revision=2000-07-11": "<ncclient.capabilities.Capability object at 0x7ff6287e3ac0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-BFD-MIB?module=CISCO-IETF-BFD-MIB&revision=2011-04-16": "<ncclient.capabilities.Capability object at 0x7ff6287e3b20>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-FRR-MIB?module=CISCO-IETF-FRR-MIB&revision=2008-04-29": "<ncclient.capabilities.Capability object at 0x7ff6287e3b80>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-ISIS-MIB?module=CISCO-IETF-ISIS-MIB&revision=2005-08-16": "<ncclient.capabilities.Capability object at 0x7ff6287e3be0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-MPLS-ID-STD-03-MIB?module=CISCO-IETF-MPLS-ID-STD-03-MIB&revision=2012-06-07": "<ncclient.capabilities.Capability object at 0x7ff6287e3c40>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-MPLS-TE-EXT-STD-03-MIB?module=CISCO-IETF-MPLS-TE-EXT-STD-03-MIB&revision=2012-06-06": "<ncclient.capabilities.Capability object at 0x7ff6287e3ca0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-ATM-MIB?module=CISCO-IETF-PW-ATM-MIB&revision=2005-04-19": "<ncclient.capabilities.Capability object at 0x7ff6287e3d00>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-ENET-MIB?module=CISCO-IETF-PW-ENET-MIB&revision=2002-09-22": "<ncclient.capabilities.Capability object at 0x7ff6287e3d60>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-MIB?module=CISCO-IETF-PW-MIB&revision=2004-03-17": "<ncclient.capabilities.Capability object at 0x7ff6287e3dc0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-MPLS-MIB?module=CISCO-IETF-PW-MPLS-MIB&revision=2003-02-26": "<ncclient.capabilities.Capability object at 0x7ff6287e3e20>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-TC-MIB?module=CISCO-IETF-PW-TC-MIB&revision=2006-07-21": "<ncclient.capabilities.Capability object at 0x7ff6287e3e80>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IETF-PW-TDM-MIB?module=CISCO-IETF-PW-TDM-MIB&revision=2006-07-21": "<ncclient.capabilities.Capability object at 0x7ff6287e3ee0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IF-EXTENSION-MIB?module=CISCO-IF-EXTENSION-MIB&revision=2013-03-13": "<ncclient.capabilities.Capability object at 0x7ff6287e3f40>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IGMP-FILTER-MIB?module=CISCO-IGMP-FILTER-MIB&revision=2005-11-29": "<ncclient.capabilities.Capability object at 0x7ff6287e3fa0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IMAGE-LICENSE-MGMT-MIB?module=CISCO-IMAGE-LICENSE-MGMT-MIB&revision=2007-10-16": "<ncclient.capabilities.Capability object at 0x7ff6287e30d0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IMAGE-MIB?module=CISCO-IMAGE-MIB&revision=1995-08-15": "<ncclient.capabilities.Capability object at 0x7ff6287e3070>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IP-LOCAL-POOL-MIB?module=CISCO-IP-LOCAL-POOL-MIB&revision=2007-11-12": "<ncclient.capabilities.Capability object at 0x7ff6287ec100>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IP-TAP-MIB?module=CISCO-IP-TAP-MIB&revision=2004-03-11": "<ncclient.capabilities.Capability object at 0x7ff6287ec160>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IP-URPF-MIB?module=CISCO-IP-URPF-MIB&revision=2011-12-29": "<ncclient.capabilities.Capability object at 0x7ff6287ec1c0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPMROUTE-MIB?module=CISCO-IPMROUTE-MIB&revision=2005-03-07": "<ncclient.capabilities.Capability object at 0x7ff6287ec220>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSEC-FLOW-MONITOR-MIB?module=CISCO-IPSEC-FLOW-MONITOR-MIB&revision=2007-10-24": "<ncclient.capabilities.Capability object at 0x7ff6287ec280>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSEC-MIB?module=CISCO-IPSEC-MIB&revision=2000-08-07": "<ncclient.capabilities.Capability object at 0x7ff6287ec2e0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSEC-POLICY-MAP-MIB?module=CISCO-IPSEC-POLICY-MAP-MIB&revision=2000-08-17": "<ncclient.capabilities.Capability object at 0x7ff6287ec340>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSLA-AUTOMEASURE-MIB?module=CISCO-IPSLA-AUTOMEASURE-MIB&revision=2007-06-13": "<ncclient.capabilities.Capability object at 0x7ff6287ec3a0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSLA-ECHO-MIB?module=CISCO-IPSLA-ECHO-MIB&revision=2007-08-16": "<ncclient.capabilities.Capability object at 0x7ff6287ec400>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSLA-JITTER-MIB?module=CISCO-IPSLA-JITTER-MIB&revision=2007-07-24": "<ncclient.capabilities.Capability object at 0x7ff6287ec460>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-IPSLA-TC-MIB?module=CISCO-IPSLA-TC-MIB&revision=2007-03-23": "<ncclient.capabilities.Capability object at 0x7ff6287ec4c0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-LICENSE-MGMT-MIB?module=CISCO-LICENSE-MGMT-MIB&revision=2012-04-19": "<ncclient.capabilities.Capability object at 0x7ff6287ec520>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-MEDIA-GATEWAY-MIB?module=CISCO-MEDIA-GATEWAY-MIB&revision=2009-02-25": "<ncclient.capabilities.Capability object at 0x7ff6287ec580>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-MPLS-LSR-EXT-STD-MIB?module=CISCO-MPLS-LSR-EXT-STD-MIB&revision=2012-04-30": "<ncclient.capabilities.Capability object at 0x7ff6287ec5e0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-MPLS-TC-EXT-STD-MIB?module=CISCO-MPLS-TC-EXT-STD-MIB&revision=2012-02-22": "<ncclient.capabilities.Capability object at 0x7ff6287ec640>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-NBAR-PROTOCOL-DISCOVERY-MIB?module=CISCO-NBAR-PROTOCOL-DISCOVERY-MIB&revision=2002-08-16": "<ncclient.capabilities.Capability object at 0x7ff6287ec6a0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-NETSYNC-MIB?module=CISCO-NETSYNC-MIB&revision=2010-10-15": "<ncclient.capabilities.Capability object at 0x7ff6287ec700>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-NTP-MIB?module=CISCO-NTP-MIB&revision=2006-07-31": "<ncclient.capabilities.Capability object at 0x7ff6287ec790>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-OSPF-MIB?module=CISCO-OSPF-MIB&revision=2003-07-18": "<ncclient.capabilities.Capability object at 0x7ff6287ec7f0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-OSPF-TRAP-MIB?module=CISCO-OSPF-TRAP-MIB&revision=2003-07-18": "<ncclient.capabilities.Capability object at 0x7ff6287ec850>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-PIM-MIB?module=CISCO-PIM-MIB&revision=2000-11-02": "<ncclient.capabilities.Capability object at 0x7ff6287ec8b0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-PING-MIB?module=CISCO-PING-MIB&revision=2001-08-28": "<ncclient.capabilities.Capability object at 0x7ff6287ec910>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-PROCESS-MIB?module=CISCO-PROCESS-MIB&revision=2011-06-23": "<ncclient.capabilities.Capability object at 0x7ff6287ec970>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-PRODUCTS-MIB?module=CISCO-PRODUCTS-MIB&revision=2014-11-06": "<ncclient.capabilities.Capability object at 0x7ff6287ec9d0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-PTP-MIB?module=CISCO-PTP-MIB&revision=2011-01-28": "<ncclient.capabilities.Capability object at 0x7ff6287eca30>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-QOS-PIB-MIB?module=CISCO-QOS-PIB-MIB&revision=2007-08-29": "<ncclient.capabilities.Capability object at 0x7ff6287eca90>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-RADIUS-EXT-MIB?module=CISCO-RADIUS-EXT-MIB&revision=2010-05-25": "<ncclient.capabilities.Capability object at 0x7ff6287ecaf0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-RF-MIB?module=CISCO-RF-MIB&revision=2005-09-01": "<ncclient.capabilities.Capability object at 0x7ff6287ecb50>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-RTTMON-MIB?module=CISCO-RTTMON-MIB&revision=2012-08-16": "<ncclient.capabilities.Capability object at 0x7ff6287ecbb0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-RTTMON-TC-MIB?module=CISCO-RTTMON-TC-MIB&revision=2012-05-25": "<ncclient.capabilities.Capability object at 0x7ff6287ecc10>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-SESS-BORDER-CTRLR-CALL-STATS-MIB?module=CISCO-SESS-BORDER-CTRLR-CALL-STATS-MIB&revision=2010-09-03": "<ncclient.capabilities.Capability object at 0x7ff6287ecc70>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-SESS-BORDER-CTRLR-STATS-MIB?module=CISCO-SESS-BORDER-CTRLR-STATS-MIB&revision=2010-09-15": "<ncclient.capabilities.Capability object at 0x7ff6287eccd0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-SIP-UA-MIB?module=CISCO-SIP-UA-MIB&revision=2004-02-19": "<ncclient.capabilities.Capability object at 0x7ff6287ecd30>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-SMI?module=CISCO-SMI&revision=2012-08-29": "<ncclient.capabilities.Capability object at 0x7ff6287ecd90>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-SONET-MIB?module=CISCO-SONET-MIB&revision=2003-03-07": "<ncclient.capabilities.Capability object at 0x7ff6287ecdf0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-ST-TC?module=CISCO-ST-TC&revision=2012-08-08": "<ncclient.capabilities.Capability object at 0x7ff6287ece50>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-STP-EXTENSIONS-MIB?module=CISCO-STP-EXTENSIONS-MIB&revision=2013-03-07": "<ncclient.capabilities.Capability object at 0x7ff6287eceb0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-SUBSCRIBER-IDENTITY-TC-MIB?module=CISCO-SUBSCRIBER-IDENTITY-TC-MIB&revision=2011-12-23": "<ncclient.capabilities.Capability object at 0x7ff6287ecf10>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-SUBSCRIBER-SESSION-MIB?module=CISCO-SUBSCRIBER-SESSION-MIB&revision=2012-08-08": "<ncclient.capabilities.Capability object at 0x7ff6287ecf70>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-SUBSCRIBER-SESSION-TC-MIB?module=CISCO-SUBSCRIBER-SESSION-TC-MIB&revision=2012-01-27": "<ncclient.capabilities.Capability object at 0x7ff6287ecfd0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-SYSLOG-MIB?module=CISCO-SYSLOG-MIB&revision=2005-12-03": "<ncclient.capabilities.Capability object at 0x7ff6287ec070>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-TAP2-MIB?module=CISCO-TAP2-MIB&revision=2009-11-06": "<ncclient.capabilities.Capability object at 0x7ff6287f40d0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-TC?module=CISCO-TC&revision=2011-11-11": "<ncclient.capabilities.Capability object at 0x7ff6287f4130>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-UBE-MIB?module=CISCO-UBE-MIB&revision=2010-11-29": "<ncclient.capabilities.Capability object at 0x7ff6287f4190>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-UNIFIED-FIREWALL-MIB?module=CISCO-UNIFIED-FIREWALL-MIB&revision=2005-09-22": "<ncclient.capabilities.Capability object at 0x7ff6287f41f0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB?module=CISCO-VLAN-IFTABLE-RELATIONSHIP-MIB&revision=2013-07-15": "<ncclient.capabilities.Capability object at 0x7ff6287f4250>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-VLAN-MEMBERSHIP-MIB?module=CISCO-VLAN-MEMBERSHIP-MIB&revision=2007-12-14": "<ncclient.capabilities.Capability object at 0x7ff6287f42b0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-VOICE-COMMON-DIAL-CONTROL-MIB?module=CISCO-VOICE-COMMON-DIAL-CONTROL-MIB&revision=2010-06-30": "<ncclient.capabilities.Capability object at 0x7ff6287f4310>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-VOICE-DIAL-CONTROL-MIB?module=CISCO-VOICE-DIAL-CONTROL-MIB&revision=2012-05-15": "<ncclient.capabilities.Capability object at 0x7ff6287f4370>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-VOICE-DNIS-MIB?module=CISCO-VOICE-DNIS-MIB&revision=2002-05-01": "<ncclient.capabilities.Capability object at 0x7ff6287f43d0>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-VPDN-MGMT-MIB?module=CISCO-VPDN-MGMT-MIB&revision=2009-06-16": "<ncclient.capabilities.Capability object at 0x7ff6287f4430>", "urn:ietf:params:xml:ns:yang:smiv2:CISCO-VTP-MIB?module=CISCO-VTP-MIB&revision=2013-10-14": "<ncclient.capabilities.Capability object at 0x7ff6287f4490>", "urn:ietf:params:xml:ns:yang:smiv2:DIAL-CONTROL-MIB?module=DIAL-CONTROL-MIB&revision=1996-09-23": "<ncclient.capabilities.Capability object at 0x7ff6287f44f0>", "urn:ietf:params:xml:ns:yang:smiv2:DIFFSERV-DSCP-TC?module=DIFFSERV-DSCP-TC&revision=2002-05-09": "<ncclient.capabilities.Capability object at 0x7ff6287f4550>", "urn:ietf:params:xml:ns:yang:smiv2:DIFFSERV-MIB?module=DIFFSERV-MIB&revision=2002-02-07": "<ncclient.capabilities.Capability object at 0x7ff6287f45b0>", "urn:ietf:params:xml:ns:yang:smiv2:DISMAN-EVENT-MIB?module=DISMAN-EVENT-MIB&revision=2000-10-16": "<ncclient.capabilities.Capability object at 0x7ff6287f4610>", "urn:ietf:params:xml:ns:yang:smiv2:DISMAN-EXPRESSION-MIB?module=DISMAN-EXPRESSION-MIB&revision=2000-10-16": "<ncclient.capabilities.Capability object at 0x7ff6287f4670>", "urn:ietf:params:xml:ns:yang:smiv2:DRAFT-MSDP-MIB?module=DRAFT-MSDP-MIB&revision=1999-12-16": "<ncclient.capabilities.Capability object at 0x7ff6287f46d0>", "urn:ietf:params:xml:ns:yang:smiv2:DS1-MIB?module=DS1-MIB&revision=1998-08-01": "<ncclient.capabilities.Capability object at 0x7ff6287f4730>", "urn:ietf:params:xml:ns:yang:smiv2:DS3-MIB?module=DS3-MIB&revision=1998-08-01": "<ncclient.capabilities.Capability object at 0x7ff6287f4790>", "urn:ietf:params:xml:ns:yang:smiv2:ENTITY-MIB?module=ENTITY-MIB&revision=2005-08-10": "<ncclient.capabilities.Capability object at 0x7ff6287f47f0>", "urn:ietf:params:xml:ns:yang:smiv2:ENTITY-SENSOR-MIB?module=ENTITY-SENSOR-MIB&revision=2002-12-16": "<ncclient.capabilities.Capability object at 0x7ff6287f4850>", "urn:ietf:params:xml:ns:yang:smiv2:ENTITY-STATE-MIB?module=ENTITY-STATE-MIB&revision=2005-11-22": "<ncclient.capabilities.Capability object at 0x7ff6287f48b0>", "urn:ietf:params:xml:ns:yang:smiv2:ENTITY-STATE-TC-MIB?module=ENTITY-STATE-TC-MIB&revision=2005-11-22": "<ncclient.capabilities.Capability object at 0x7ff6287f4910>", "urn:ietf:params:xml:ns:yang:smiv2:ETHER-WIS?module=ETHER-WIS&revision=2003-09-19": "<ncclient.capabilities.Capability object at 0x7ff6287f4970>", "urn:ietf:params:xml:ns:yang:smiv2:EXPRESSION-MIB?module=EXPRESSION-MIB&revision=2005-11-24": "<ncclient.capabilities.Capability object at 0x7ff6287f49d0>", "urn:ietf:params:xml:ns:yang:smiv2:EtherLike-MIB?module=EtherLike-MIB&revision=2003-09-19": "<ncclient.capabilities.Capability object at 0x7ff6287f4a30>", "urn:ietf:params:xml:ns:yang:smiv2:FRAME-RELAY-DTE-MIB?module=FRAME-RELAY-DTE-MIB&revision=1997-05-01": "<ncclient.capabilities.Capability object at 0x7ff6287f4a90>", "urn:ietf:params:xml:ns:yang:smiv2:HCNUM-TC?module=HCNUM-TC&revision=2000-06-08": "<ncclient.capabilities.Capability object at 0x7ff6287f4af0>", "urn:ietf:params:xml:ns:yang:smiv2:IANA-ADDRESS-FAMILY-NUMBERS-MIB?module=IANA-ADDRESS-FAMILY-NUMBERS-MIB&revision=2000-09-08": "<ncclient.capabilities.Capability object at 0x7ff6287f4b50>", "urn:ietf:params:xml:ns:yang:smiv2:IANA-RTPROTO-MIB?module=IANA-RTPROTO-MIB&revision=2000-09-26": "<ncclient.capabilities.Capability object at 0x7ff6287f4bb0>", "urn:ietf:params:xml:ns:yang:smiv2:IANAifType-MIB?module=IANAifType-MIB&revision=2006-03-31": "<ncclient.capabilities.Capability object at 0x7ff6287f4c10>", "urn:ietf:params:xml:ns:yang:smiv2:IEEE8021-TC-MIB?module=IEEE8021-TC-MIB&revision=2008-10-15": "<ncclient.capabilities.Capability object at 0x7ff6287f4c70>", "urn:ietf:params:xml:ns:yang:smiv2:IF-MIB?module=IF-MIB&revision=2000-06-14": "<ncclient.capabilities.Capability object at 0x7ff6287f4cd0>", "urn:ietf:params:xml:ns:yang:smiv2:IGMP-STD-MIB?module=IGMP-STD-MIB&revision=2000-09-28": "<ncclient.capabilities.Capability object at 0x7ff6287f4d30>", "urn:ietf:params:xml:ns:yang:smiv2:INET-ADDRESS-MIB?module=INET-ADDRESS-MIB&revision=2005-02-04": "<ncclient.capabilities.Capability object at 0x7ff6287f4d90>", "urn:ietf:params:xml:ns:yang:smiv2:INT-SERV-MIB?module=INT-SERV-MIB&revision=1997-10-03": "<ncclient.capabilities.Capability object at 0x7ff6287f4df0>", "urn:ietf:params:xml:ns:yang:smiv2:INTEGRATED-SERVICES-MIB?module=INTEGRATED-SERVICES-MIB&revision=1995-11-03": "<ncclient.capabilities.Capability object at 0x7ff6287f4e50>", "urn:ietf:params:xml:ns:yang:smiv2:IP-FORWARD-MIB?module=IP-FORWARD-MIB&revision=1996-09-19": "<ncclient.capabilities.Capability object at 0x7ff6287f4eb0>", "urn:ietf:params:xml:ns:yang:smiv2:IP-MIB?module=IP-MIB&revision=2006-02-02": "<ncclient.capabilities.Capability object at 0x7ff6287f4f10>", "urn:ietf:params:xml:ns:yang:smiv2:IPMROUTE-STD-MIB?module=IPMROUTE-STD-MIB&revision=2000-09-22": "<ncclient.capabilities.Capability object at 0x7ff6287f4f70>", "urn:ietf:params:xml:ns:yang:smiv2:IPV6-FLOW-LABEL-MIB?module=IPV6-FLOW-LABEL-MIB&revision=2003-08-28": "<ncclient.capabilities.Capability object at 0x7ff6287f4fd0>", "urn:ietf:params:xml:ns:yang:smiv2:LLDP-MIB?module=LLDP-MIB&revision=2005-05-06": "<ncclient.capabilities.Capability object at 0x7ff6287f40a0>", "urn:ietf:params:xml:ns:yang:smiv2:MPLS-L3VPN-STD-MIB?module=MPLS-L3VPN-STD-MIB&revision=2006-01-23": "<ncclient.capabilities.Capability object at 0x7ff6287fc0d0>", "urn:ietf:params:xml:ns:yang:smiv2:MPLS-LDP-GENERIC-STD-MIB?module=MPLS-LDP-GENERIC-STD-MIB&revision=2004-06-03": "<ncclient.capabilities.Capability object at 0x7ff6287fc130>", "urn:ietf:params:xml:ns:yang:smiv2:MPLS-LDP-STD-MIB?module=MPLS-LDP-STD-MIB&revision=2004-06-03": "<ncclient.capabilities.Capability object at 0x7ff6287fc190>", "urn:ietf:params:xml:ns:yang:smiv2:MPLS-LSR-STD-MIB?module=MPLS-LSR-STD-MIB&revision=2004-06-03": "<ncclient.capabilities.Capability object at 0x7ff6287fc1f0>", "urn:ietf:params:xml:ns:yang:smiv2:MPLS-TC-MIB?module=MPLS-TC-MIB&revision=2001-01-04": "<ncclient.capabilities.Capability object at 0x7ff6287fc250>", "urn:ietf:params:xml:ns:yang:smiv2:MPLS-TC-STD-MIB?module=MPLS-TC-STD-MIB&revision=2004-06-03": "<ncclient.capabilities.Capability object at 0x7ff6287fc2b0>", "urn:ietf:params:xml:ns:yang:smiv2:MPLS-TE-STD-MIB?module=MPLS-TE-STD-MIB&revision=2004-06-03": "<ncclient.capabilities.Capability object at 0x7ff6287fc310>", "urn:ietf:params:xml:ns:yang:smiv2:MPLS-VPN-MIB?module=MPLS-VPN-MIB&revision=2001-10-15": "<ncclient.capabilities.Capability object at 0x7ff6287fc370>", "urn:ietf:params:xml:ns:yang:smiv2:NHRP-MIB?module=NHRP-MIB&revision=1999-08-26": "<ncclient.capabilities.Capability object at 0x7ff6287fc3d0>", "urn:ietf:params:xml:ns:yang:smiv2:NOTIFICATION-LOG-MIB?module=NOTIFICATION-LOG-MIB&revision=2000-11-27": "<ncclient.capabilities.Capability object at 0x7ff6287fc430>", "urn:ietf:params:xml:ns:yang:smiv2:OSPF-MIB?module=OSPF-MIB&revision=2006-11-10": "<ncclient.capabilities.Capability object at 0x7ff6287fc490>", "urn:ietf:params:xml:ns:yang:smiv2:OSPF-TRAP-MIB?module=OSPF-TRAP-MIB&revision=2006-11-10": "<ncclient.capabilities.Capability object at 0x7ff6287fc4f0>", "urn:ietf:params:xml:ns:yang:smiv2:P-BRIDGE-MIB?module=P-BRIDGE-MIB&revision=2006-01-09": "<ncclient.capabilities.Capability object at 0x7ff6287fc550>", "urn:ietf:params:xml:ns:yang:smiv2:PIM-MIB?module=PIM-MIB&revision=2000-09-28": "<ncclient.capabilities.Capability object at 0x7ff6287fc5b0>", "urn:ietf:params:xml:ns:yang:smiv2:PerfHist-TC-MIB?module=PerfHist-TC-MIB&revision=1998-11-07": "<ncclient.capabilities.Capability object at 0x7ff6287fc610>", "urn:ietf:params:xml:ns:yang:smiv2:Q-BRIDGE-MIB?module=Q-BRIDGE-MIB&revision=2006-01-09": "<ncclient.capabilities.Capability object at 0x7ff6287fc670>", "urn:ietf:params:xml:ns:yang:smiv2:RFC-1212?module=RFC-1212": "<ncclient.capabilities.Capability object at 0x7ff6287fc6d0>", "urn:ietf:params:xml:ns:yang:smiv2:RFC-1215?module=RFC-1215": "<ncclient.capabilities.Capability object at 0x7ff6287fc0a0>", "urn:ietf:params:xml:ns:yang:smiv2:RFC1155-SMI?module=RFC1155-SMI": "<ncclient.capabilities.Capability object at 0x7ff6287fc730>", "urn:ietf:params:xml:ns:yang:smiv2:RFC1213-MIB?module=RFC1213-MIB": "<ncclient.capabilities.Capability object at 0x7ff6287fc790>", "urn:ietf:params:xml:ns:yang:smiv2:RFC1315-MIB?module=RFC1315-MIB": "<ncclient.capabilities.Capability object at 0x7ff6287fc7f0>", "urn:ietf:params:xml:ns:yang:smiv2:RMON-MIB?module=RMON-MIB&revision=2000-05-11": "<ncclient.capabilities.Capability object at 0x7ff6287fc850>", "urn:ietf:params:xml:ns:yang:smiv2:RMON2-MIB?module=RMON2-MIB&revision=1996-05-27": "<ncclient.capabilities.Capability object at 0x7ff6287fc910>", "urn:ietf:params:xml:ns:yang:smiv2:RSVP-MIB?module=RSVP-MIB&revision=1998-08-25": "<ncclient.capabilities.Capability object at 0x7ff6287fc970>", "urn:ietf:params:xml:ns:yang:smiv2:SNMP-FRAMEWORK-MIB?module=SNMP-FRAMEWORK-MIB&revision=2002-10-14": "<ncclient.capabilities.Capability object at 0x7ff6287fc9d0>", "urn:ietf:params:xml:ns:yang:smiv2:SNMP-PROXY-MIB?module=SNMP-PROXY-MIB&revision=2002-10-14": "<ncclient.capabilities.Capability object at 0x7ff6287fca30>", "urn:ietf:params:xml:ns:yang:smiv2:SNMP-TARGET-MIB?module=SNMP-TARGET-MIB&revision=1998-08-04": "<ncclient.capabilities.Capability object at 0x7ff6287fca90>", "urn:ietf:params:xml:ns:yang:smiv2:SNMPv2-MIB?module=SNMPv2-MIB&revision=2002-10-16": "<ncclient.capabilities.Capability object at 0x7ff6287fcaf0>", "urn:ietf:params:xml:ns:yang:smiv2:SNMPv2-TC?module=SNMPv2-TC": "<ncclient.capabilities.Capability object at 0x7ff6287fcb50>", "urn:ietf:params:xml:ns:yang:smiv2:SONET-MIB?module=SONET-MIB&revision=2003-08-11": "<ncclient.capabilities.Capability object at 0x7ff6287fc8b0>", "urn:ietf:params:xml:ns:yang:smiv2:TCP-MIB?module=TCP-MIB&revision=2005-02-18": "<ncclient.capabilities.Capability object at 0x7ff6287fcc10>", "urn:ietf:params:xml:ns:yang:smiv2:TOKEN-RING-RMON-MIB?module=TOKEN-RING-RMON-MIB": "<ncclient.capabilities.Capability object at 0x7ff6287fcc70>", "urn:ietf:params:xml:ns:yang:smiv2:TOKENRING-MIB?module=TOKENRING-MIB&revision=1994-10-23": "<ncclient.capabilities.Capability object at 0x7ff6287fcbb0>", "urn:ietf:params:xml:ns:yang:smiv2:TUNNEL-MIB?module=TUNNEL-MIB&revision=2005-05-16": "<ncclient.capabilities.Capability object at 0x7ff6287fcd30>", "urn:ietf:params:xml:ns:yang:smiv2:UDP-MIB?module=UDP-MIB&revision=2005-05-20": "<ncclient.capabilities.Capability object at 0x7ff6287fcd90>", "urn:ietf:params:xml:ns:yang:smiv2:VPN-TC-STD-MIB?module=VPN-TC-STD-MIB&revision=2005-11-15": "<ncclient.capabilities.Capability object at 0x7ff6287fcdf0>", "urn:ietf:params:xml:ns:netconf:base:1.0?module=ietf-netconf&revision=2011-06-01": "<ncclient.capabilities.Capability object at 0x7ff6287fce50>", "urn:ietf:params:xml:ns:yang:ietf-netconf-with-defaults?module=ietf-netconf-with-defaults&revision=2011-06-01": "<ncclient.capabilities.Capability object at 0x7ff6287fceb0>", "\\n urn:ietf:params:netconf:capability:notification:1.1\\n ": "<ncclient.capabilities.Capability object at 0x7ff6287fcf10>" }
    return data

def getRestConfTrunk():
    data = {"jsonrpc": "2.0", "result": {"body": {"TABLE_allowed_vlans": {"ROW_allowed_vlans": {"interface": "Ethernet1/3", "allowedvlans": "1"
                }
            }, "TABLE_vtp_pruning": {"ROW_vtp_pruning": {"interface": "Ethernet1/3", "vtppruning_vlans": "1"
                }
            }, "TABLE_stp_forward": {"ROW_stp_forward": {"interface": "Ethernet1/3", "stpfwd_vlans": "1"
                }
            }, "TABLE_errored_vlans": {"ROW_errored_vlans": {"interface": "Ethernet1/3", "erroredvlans": "none"
                }
            }, "TABLE_interface": {"ROW_interface": {"interface": "Ethernet1/3", "native": 1, "status": "trunking", "portchannel": "--"
                }
            }
        }
    }, "id": 1
    }
    return data
def getRestConfBrief():
    data = {
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
    return data
def showRun():
    data = {
    "jsonrpc": "2.0",
    "result": {
        "body": {
            "nf:filter": {
                "m:configure": {
                    "m:terminal": {
                        "no": [
                            {
                                "password": {
                                    "strength-check": ""
                                }
                            },
                            {
                                "port-channel": {
                                    "load-balance": {
                                        "resilient": ""
                                    }
                                }
                            }
                        ],
                        "feature-set": {
                            "__XML__PARAM__fs": {
                                "__XML__value": "mpls"
                            }
                        },
                        "install": {
                            "feature-set": {
                                "mpls": ""
                            }
                        },
                        "nxapi": [
                            {
                                "http": {
                                    "port": {
                                        "__XML__PARAM__s0": {
                                            "__XML__value": "80"
                                        }
                                    }
                                }
                            },
                            {
                                "idle-timeout": {
                                    "__XML__PARAM__i0": {
                                        "__XML__value": "1440"
                                    }
                                }
                            }
                        ],
                        "ipv6": [
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-eigrp6",
                                        "m3:__XML__PARAM__seqno": {
                                            "m3:__XML__value": "10",
                                            "m3:__XML__PARAM__permitdeny": {
                                                "m3:__XML__value": "permit",
                                                "m3:__XML__PARAM__ipv6_other_proto": {
                                                    "m3:__XML__value": "eigrp",
                                                    "m3:__XML__PARAM__ipv6_src_any": {
                                                        "m3:__XML__value": "any",
                                                        "m3:__XML__PARAM__ipv6_dst_prefix": {
                                                            "m3:__XML__value": "ff02::a/128"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-v6routingProto2",
                                        "m3:__XML__PARAM__seqno": [
                                            {
                                                "m3:__XML__value": "10",
                                                "m3:__XML__PARAM__permitdeny": {
                                                    "m3:__XML__value": "permit",
                                                    "m3:__XML__PARAM__proto_udp": {
                                                        "m3:__XML__value": "udp",
                                                        "m3:__XML__PARAM__ipv6_udp_src_any": {
                                                            "m3:__XML__value": "any",
                                                            "m3:__XML__PARAM__ipv6_udp_dst_prefix": {
                                                                "m3:__XML__value": "ff02::66/128",
                                                                "m3:__XML__PARAM__UDP_dst_portop": {
                                                                    "m3:__XML__value": "eq",
                                                                    "m3:__XML__PARAM__UDP_ipv6_dst_port0": {
                                                                        "m3:__XML__value": "2029"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m3:__XML__value": "20",
                                                "m3:__XML__PARAM__permitdeny": {
                                                    "m3:__XML__value": "permit",
                                                    "m3:__XML__PARAM__proto_udp": {
                                                        "m3:__XML__value": "udp",
                                                        "m3:__XML__PARAM__ipv6_udp_src_any": {
                                                            "m3:__XML__value": "any",
                                                            "m3:__XML__PARAM__ipv6_udp_dst_prefix": {
                                                                "m3:__XML__value": "ff02::fb/128",
                                                                "m3:__XML__PARAM__UDP_dst_portop": {
                                                                    "m3:__XML__value": "eq",
                                                                    "m3:__XML__PARAM__UDP_ipv6_dst_port0": {
                                                                        "m3:__XML__value": "5353"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m3:__XML__value": "30",
                                                "m3:__XML__PARAM__permitdeny": {
                                                    "m3:__XML__value": "permit",
                                                    "m3:__XML__PARAM__proto": {
                                                        "m3:__XML__value": "112",
                                                        "m3:__XML__PARAM__ipv6_src_any": {
                                                            "m3:__XML__value": "any",
                                                            "m3:__XML__PARAM__ipv6_dst_prefix": {
                                                                "m3:__XML__value": "ff02::12/128"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-v6routingproto1",
                                        "m3:__XML__PARAM__seqno": [
                                            {
                                                "m3:__XML__value": "10",
                                                "m3:__XML__PARAM__permitdeny": {
                                                    "m3:__XML__value": "permit",
                                                    "m3:__XML__PARAM__proto": {
                                                        "m3:__XML__value": "89",
                                                        "m3:__XML__PARAM__ipv6_src_any": {
                                                            "m3:__XML__value": "any",
                                                            "m3:__XML__PARAM__ipv6_dst_prefix": {
                                                                "m3:__XML__value": "ff02::5/128"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m3:__XML__value": "20",
                                                "m3:__XML__PARAM__permitdeny": {
                                                    "m3:__XML__value": "permit",
                                                    "m3:__XML__PARAM__proto": {
                                                        "m3:__XML__value": "89",
                                                        "m3:__XML__PARAM__ipv6_src_any": {
                                                            "m3:__XML__value": "any",
                                                            "m3:__XML__PARAM__ipv6_dst_prefix": {
                                                                "m3:__XML__value": "ff02::6/128"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m3:__XML__value": "30",
                                                "m3:__XML__PARAM__permitdeny": {
                                                    "m3:__XML__value": "permit",
                                                    "m3:__XML__PARAM__proto_udp": {
                                                        "m3:__XML__value": "udp",
                                                        "m3:__XML__PARAM__ipv6_udp_src_any": {
                                                            "m3:__XML__value": "any",
                                                            "m3:__XML__PARAM__ipv6_udp_dst_prefix": {
                                                                "m3:__XML__value": "ff02::9/128",
                                                                "m3:__XML__PARAM__UDP_dst_portop": {
                                                                    "m3:__XML__value": "eq",
                                                                    "m3:__XML__PARAM__UDP_ipv6_dst_port0": {
                                                                        "m3:__XML__value": "521"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        ],
                        "feature": [
                            {
                                "telnet": ""
                            },
                            {
                                "nxapi": ""
                            },
                            {
                                "bash-shell": ""
                            },
                            {
                                "interface-vlan": ""
                            },
                            {
                                "ptp": ""
                            },
                            {
                                "lldp": ""
                            }
                        ],
                        "line": [
                            {
                                "console": ""
                            },
                            {
                                "vty": ""
                            }
                        ],
                        "control-plane": {
                            "m7:service-policy": {
                                "m7:input": {
                                    "m7:__XML__PARAM__policy_name": {
                                        "m7:__XML__value": "copp-system-policy"
                                    }
                                }
                            }
                        },
                        "service": {
                            "unsupported-transceiver": ""
                        },
                        "password": {
                            "prompt": {
                                "username": ""
                            }
                        },
                        "rmon": [
                            {
                                "event": {
                                    "__XML__PARAM__i0": {
                                        "__XML__value": "1",
                                        "log": {
                                            "trap": {
                                                "__XML__PARAM__s0": {
                                                    "__XML__value": "public",
                                                    "description": {
                                                        "__XML__PARAM__s1": {
                                                            "__XML__value": "FATAL(1)",
                                                            "owner": {
                                                                "__XML__PARAM__s2": {
                                                                    "__XML__value": "PMON@FATAL"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "event": {
                                    "__XML__PARAM__i0": {
                                        "__XML__value": "2",
                                        "log": {
                                            "trap": {
                                                "__XML__PARAM__s0": {
                                                    "__XML__value": "public",
                                                    "description": {
                                                        "__XML__PARAM__s1": {
                                                            "__XML__value": "CRITICAL(2)",
                                                            "owner": {
                                                                "__XML__PARAM__s2": {
                                                                    "__XML__value": "PMON@CRITICAL"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "event": {
                                    "__XML__PARAM__i0": {
                                        "__XML__value": "3",
                                        "log": {
                                            "trap": {
                                                "__XML__PARAM__s0": {
                                                    "__XML__value": "public",
                                                    "description": {
                                                        "__XML__PARAM__s1": {
                                                            "__XML__value": "ERROR(3)",
                                                            "owner": {
                                                                "__XML__PARAM__s2": {
                                                                    "__XML__value": "PMON@ERROR"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "event": {
                                    "__XML__PARAM__i0": {
                                        "__XML__value": "4",
                                        "log": {
                                            "trap": {
                                                "__XML__PARAM__s0": {
                                                    "__XML__value": "public",
                                                    "description": {
                                                        "__XML__PARAM__s1": {
                                                            "__XML__value": "WARNING(4)",
                                                            "owner": {
                                                                "__XML__PARAM__s2": {
                                                                    "__XML__value": "PMON@WARNING"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "event": {
                                    "__XML__PARAM__i0": {
                                        "__XML__value": "5",
                                        "log": {
                                            "trap": {
                                                "__XML__PARAM__s0": {
                                                    "__XML__value": "public",
                                                    "description": {
                                                        "__XML__PARAM__s1": {
                                                            "__XML__value": "INFORMATION(5)",
                                                            "owner": {
                                                                "__XML__PARAM__s2": {
                                                                    "__XML__value": "PMON@INFO"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ],
                        "clock": [
                            {
                                "timezone": {
                                    "__XML__PARAM__s7": {
                                        "__XML__value": "IST",
                                        "__XML__PARAM__i3": {
                                            "__XML__value": "5",
                                            "__XML__PARAM__i4": {
                                                "__XML__value": "30"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "protocol": {
                                    "none": {
                                        "vdc": {
                                            "__XML__PARAM__vdc-id": {
                                                "__XML__value": "1"
                                            }
                                        }
                                    }
                                }
                            }
                        ],
                        "vlan": {
                            "__XML__PARAM__vlan-id-create-delete": {
                                "__XML__value": "1"
                            }
                        },
                        "vdc": {
                            "__XML__PARAM__e-vdc": {
                                "__XML__value": "switch",
                                "id": {
                                    "__XML__PARAM__new_id": {
                                        "__XML__value": "1",
                                        "m1:limit-resource": [
                                            {
                                                "m1:vlan": {
                                                    "m1:minimum": {
                                                        "m1:__XML__PARAM__min-val": {
                                                            "m1:__XML__value": "16",
                                                            "m1:maximum": {
                                                                "m1:__XML__PARAM__max-val": {
                                                                    "m1:__XML__value": "4094"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m1:vrf": {
                                                    "m1:minimum": {
                                                        "m1:__XML__PARAM__number1": {
                                                            "m1:__XML__value": "2",
                                                            "m1:maximum": {
                                                                "m1:__XML__PARAM__number2": {
                                                                    "m1:__XML__value": "4096"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m1:port-channel": {
                                                    "m1:minimum": {
                                                        "m1:__XML__PARAM__min-val": {
                                                            "m1:__XML__value": "0",
                                                            "m1:maximum": {
                                                                "m1:__XML__PARAM__max-val": {
                                                                    "m1:__XML__value": "104"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m1:u4route-mem": {
                                                    "m1:minimum": {
                                                        "m1:__XML__PARAM__min": {
                                                            "m1:__XML__value": "128",
                                                            "m1:maximum": {
                                                                "m1:__XML__PARAM__max": {
                                                                    "m1:__XML__value": "128"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m1:u6route-mem": {
                                                    "m1:minimum": {
                                                        "m1:__XML__PARAM__min": {
                                                            "m1:__XML__value": "96",
                                                            "m1:maximum": {
                                                                "m1:__XML__PARAM__max": {
                                                                    "m1:__XML__value": "96"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m1:m4route-mem": {
                                                    "m1:minimum": {
                                                        "m1:__XML__PARAM__min": {
                                                            "m1:__XML__value": "58",
                                                            "m1:maximum": {
                                                                "m1:__XML__PARAM__max": {
                                                                    "m1:__XML__value": "58"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m1:m6route-mem": {
                                                    "m1:minimum": {
                                                        "m1:__XML__PARAM__min": {
                                                            "m1:__XML__value": "8",
                                                            "m1:maximum": {
                                                                "m1:__XML__PARAM__max": {
                                                                    "m1:__XML__value": "8"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ],
                                        "m1:allow": {
                                            "m1:feature-set": {
                                                "m1:__XML__PARAM__fs": {
                                                    "m1:__XML__value": "mpls"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "vrf": {
                            "context": {
                                "__XML__PARAM__vrf-name-known-name": {
                                    "__XML__value": "management",
                                    "m8:ip": {
                                        "m8:route": {
                                            "m8:__XML__PARAM__ip-prefix": {
                                                "m8:__XML__value": "0.0.0.0/0",
                                                "m8:__XML__PARAM__next-hop": {
                                                    "m8:__XML__value": "10.5.196.1"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "boot": {
                            "nxos": {
                                "__XML__PARAM__uri0": {
                                    "__XML__value": "bootflash:/nxos.9.3.6.bin"
                                }
                            }
                        },
                        "ip": [
                            {
                                "domain-lookup": ""
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-eigrp",
                                        "m2:__XML__PARAM__seqno": {
                                            "m2:__XML__value": "10",
                                            "m2:__XML__PARAM__permitdeny": {
                                                "m2:__XML__value": "permit",
                                                "m2:__XML__PARAM__ip_other_proto": {
                                                    "m2:__XML__value": "eigrp",
                                                    "m2:__XML__PARAM__ip_src_any": {
                                                        "m2:__XML__value": "any",
                                                        "m2:__XML__PARAM__ip_dst_prefix": {
                                                            "m2:__XML__value": "224.0.0.10/32"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-icmp",
                                        "m2:__XML__PARAM__seqno": {
                                            "m2:__XML__value": "10",
                                            "m2:__XML__PARAM__permitdeny": {
                                                "m2:__XML__value": "permit",
                                                "m2:__XML__PARAM__proto_icmp": {
                                                    "m2:__XML__value": "icmp",
                                                    "m2:__XML__PARAM__icmp_src_any": {
                                                        "m2:__XML__value": "any",
                                                        "m2:__XML__PARAM__icmp_dst_any": {
                                                            "m2:__XML__value": "any"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-igmp",
                                        "m2:__XML__PARAM__seqno": {
                                            "m2:__XML__value": "10",
                                            "m2:__XML__PARAM__permitdeny": {
                                                "m2:__XML__value": "permit",
                                                "m2:__XML__PARAM__proto_igmp": {
                                                    "m2:__XML__value": "igmp",
                                                    "m2:__XML__PARAM__igmp_src_any": {
                                                        "m2:__XML__value": "any",
                                                        "m2:__XML__PARAM__igmp_dst_any": {
                                                            "m2:__XML__value": "any"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-ntp",
                                        "m2:__XML__PARAM__seqno": [
                                            {
                                                "m2:__XML__value": "10",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0_str": {
                                                                        "m2:__XML__value": "ntp"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "20",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__UDP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__UDP_ip_src_port0_str": {
                                                                    "m2:__XML__value": "ntp",
                                                                    "m2:__XML__PARAM__udp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-pimreg",
                                        "m2:__XML__PARAM__seqno": {
                                            "m2:__XML__value": "10",
                                            "m2:__XML__PARAM__permitdeny": {
                                                "m2:__XML__value": "permit",
                                                "m2:__XML__PARAM__ip_other_proto": {
                                                    "m2:__XML__value": "pim",
                                                    "m2:__XML__PARAM__ip_src_any": {
                                                        "m2:__XML__value": "any",
                                                        "m2:__XML__PARAM__ip_dst_any": {
                                                            "m2:__XML__value": "any"
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-ping",
                                        "m2:__XML__PARAM__seqno": [
                                            {
                                                "m2:__XML__value": "10",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_icmp": {
                                                        "m2:__XML__value": "icmp",
                                                        "m2:__XML__PARAM__icmp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__icmp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__icmp_str": {
                                                                    "m2:__XML__value": "echo"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "20",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_icmp": {
                                                        "m2:__XML__value": "icmp",
                                                        "m2:__XML__PARAM__icmp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__icmp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__icmp_str": {
                                                                    "m2:__XML__value": "echo-reply"
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-routingproto1",
                                        "m2:__XML__PARAM__seqno": [
                                            {
                                                "m2:__XML__value": "10",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__TCP_src_portop": {
                                                                "m2:__XML__value": "gt",
                                                                "m2:__XML__PARAM__TCP_ip_src_port0": {
                                                                    "m2:__XML__value": "1024",
                                                                    "m2:__XML__PARAM__tcp_dst_any": {
                                                                        "m2:__XML__value": "any",
                                                                        "m2:__XML__PARAM__TCP_dst_portop": {
                                                                            "m2:__XML__value": "eq",
                                                                            "m2:__XML__PARAM__TCP_ip_dst_port0_str": {
                                                                                "m2:__XML__value": "bgp"
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "20",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__TCP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__TCP_ip_src_port0_str": {
                                                                    "m2:__XML__value": "bgp",
                                                                    "m2:__XML__PARAM__tcp_dst_any": {
                                                                        "m2:__XML__value": "any",
                                                                        "m2:__XML__PARAM__TCP_dst_portop": {
                                                                            "m2:__XML__value": "gt",
                                                                            "m2:__XML__PARAM__TCP_ip_dst_port0": {
                                                                                "m2:__XML__value": "1024"
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "30",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_prefix": {
                                                                "m2:__XML__value": "224.0.0.0/24",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0_str": {
                                                                        "m2:__XML__value": "rip"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "40",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__TCP_src_portop": {
                                                                "m2:__XML__value": "gt",
                                                                "m2:__XML__PARAM__TCP_ip_src_port0": {
                                                                    "m2:__XML__value": "1024",
                                                                    "m2:__XML__PARAM__tcp_dst_any": {
                                                                        "m2:__XML__value": "any",
                                                                        "m2:__XML__PARAM__TCP_dst_portop": {
                                                                            "m2:__XML__value": "eq",
                                                                            "m2:__XML__PARAM__TCP_ip_dst_port0": {
                                                                                "m2:__XML__value": "639"
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "50",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__TCP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__TCP_ip_src_port0": {
                                                                    "m2:__XML__value": "639",
                                                                    "m2:__XML__PARAM__tcp_dst_any": {
                                                                        "m2:__XML__value": "any",
                                                                        "m2:__XML__PARAM__TCP_dst_portop": {
                                                                            "m2:__XML__value": "gt",
                                                                            "m2:__XML__PARAM__TCP_ip_dst_port0": {
                                                                                "m2:__XML__value": "1024"
                                                                            }
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "70",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__ip_other_proto": {
                                                        "m2:__XML__value": "ospf",
                                                        "m2:__XML__PARAM__ip_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__ip_dst_any": {
                                                                "m2:__XML__value": "any"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "80",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__ip_other_proto": {
                                                        "m2:__XML__value": "ospf",
                                                        "m2:__XML__PARAM__ip_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__ip_dst_prefix": {
                                                                "m2:__XML__value": "224.0.0.5/32"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "90",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__ip_other_proto": {
                                                        "m2:__XML__value": "ospf",
                                                        "m2:__XML__PARAM__ip_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__ip_dst_prefix": {
                                                                "m2:__XML__value": "224.0.0.6/32"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-routingproto2",
                                        "m2:__XML__PARAM__seqno": [
                                            {
                                                "m2:__XML__value": "10",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_prefix": {
                                                                "m2:__XML__value": "224.0.0.0/24",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0": {
                                                                        "m2:__XML__value": "1985"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "20",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto": {
                                                        "m2:__XML__value": "112",
                                                        "m2:__XML__PARAM__ip_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__ip_dst_prefix": {
                                                                "m2:__XML__value": "224.0.0.0/24"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-snmp",
                                        "m2:__XML__PARAM__seqno": [
                                            {
                                                "m2:__XML__value": "10",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0_str": {
                                                                        "m2:__XML__value": "snmp"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "20",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0_str": {
                                                                        "m2:__XML__value": "snmptrap"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-ssh",
                                        "m2:__XML__PARAM__seqno": [
                                            {
                                                "m2:__XML__value": "10",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__tcp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__TCP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__TCP_ip_dst_port0": {
                                                                        "m2:__XML__value": "22"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "20",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__TCP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__TCP_ip_src_port0": {
                                                                    "m2:__XML__value": "22",
                                                                    "m2:__XML__PARAM__tcp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-stftp",
                                        "m2:__XML__PARAM__seqno": [
                                            {
                                                "m2:__XML__value": "10",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0_str": {
                                                                        "m2:__XML__value": "tftp"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "20",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0": {
                                                                        "m2:__XML__value": "1758"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "30",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__UDP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__UDP_ip_src_port0_str": {
                                                                    "m2:__XML__value": "tftp",
                                                                    "m2:__XML__PARAM__udp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "40",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__UDP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__UDP_ip_src_port0": {
                                                                    "m2:__XML__value": "1758",
                                                                    "m2:__XML__PARAM__udp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "50",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__tcp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__TCP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__TCP_ip_dst_port0": {
                                                                        "m2:__XML__value": "115"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "60",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__TCP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__TCP_ip_src_port0": {
                                                                    "m2:__XML__value": "115",
                                                                    "m2:__XML__PARAM__tcp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-tacacsradius",
                                        "m2:__XML__PARAM__seqno": [
                                            {
                                                "m2:__XML__value": "10",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__tcp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__TCP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__TCP_ip_dst_port0_str": {
                                                                        "m2:__XML__value": "tacacs"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "20",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__TCP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__TCP_ip_src_port0_str": {
                                                                    "m2:__XML__value": "tacacs",
                                                                    "m2:__XML__PARAM__tcp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "30",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0": {
                                                                        "m2:__XML__value": "1812"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "40",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0": {
                                                                        "m2:__XML__value": "1813"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "50",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0": {
                                                                        "m2:__XML__value": "1645"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "60",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__udp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__UDP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__UDP_ip_dst_port0": {
                                                                        "m2:__XML__value": "1646"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "70",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__UDP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__UDP_ip_src_port0": {
                                                                    "m2:__XML__value": "1812",
                                                                    "m2:__XML__PARAM__udp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "80",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__UDP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__UDP_ip_src_port0": {
                                                                    "m2:__XML__value": "1813",
                                                                    "m2:__XML__PARAM__udp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "90",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__UDP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__UDP_ip_src_port0": {
                                                                    "m2:__XML__value": "1645",
                                                                    "m2:__XML__PARAM__udp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "100",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_udp": {
                                                        "m2:__XML__value": "udp",
                                                        "m2:__XML__PARAM__udp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__UDP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__UDP_ip_src_port0": {
                                                                    "m2:__XML__value": "1646",
                                                                    "m2:__XML__PARAM__udp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-acl-telnet",
                                        "m2:__XML__PARAM__seqno": [
                                            {
                                                "m2:__XML__value": "10",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__tcp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__TCP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__TCP_ip_dst_port0_str": {
                                                                        "m2:__XML__value": "telnet"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "20",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__tcp_dst_any": {
                                                                "m2:__XML__value": "any",
                                                                "m2:__XML__PARAM__TCP_dst_portop": {
                                                                    "m2:__XML__value": "eq",
                                                                    "m2:__XML__PARAM__TCP_ip_dst_port0": {
                                                                        "m2:__XML__value": "107"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "30",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__TCP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__TCP_ip_src_port0_str": {
                                                                    "m2:__XML__value": "telnet",
                                                                    "m2:__XML__PARAM__tcp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m2:__XML__value": "40",
                                                "m2:__XML__PARAM__permitdeny": {
                                                    "m2:__XML__value": "permit",
                                                    "m2:__XML__PARAM__proto_tcp": {
                                                        "m2:__XML__value": "tcp",
                                                        "m2:__XML__PARAM__tcp_src_any": {
                                                            "m2:__XML__value": "any",
                                                            "m2:__XML__PARAM__TCP_src_portop": {
                                                                "m2:__XML__value": "eq",
                                                                "m2:__XML__PARAM__TCP_ip_src_port0": {
                                                                    "m2:__XML__value": "107",
                                                                    "m2:__XML__PARAM__tcp_dst_any": {
                                                                        "m2:__XML__value": "any"
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            },
                            {
                                "access-list": {
                                    "__XML__PARAM__name": {
                                        "__XML__value": "copp-system-dhcp-relay",
                                        "m2:__XML__PARAM__seqno": {
                                            "m2:__XML__value": "10",
                                            "m2:__XML__PARAM__permitdeny": {
                                                "m2:__XML__value": "permit",
                                                "m2:__XML__PARAM__proto_udp": {
                                                    "m2:__XML__value": "udp",
                                                    "m2:__XML__PARAM__udp_src_any": {
                                                        "m2:__XML__value": "any",
                                                        "m2:__XML__PARAM__UDP_src_portop": {
                                                            "m2:__XML__value": "eq",
                                                            "m2:__XML__PARAM__UDP_ip_src_port0_str": {
                                                                "m2:__XML__value": "bootps",
                                                                "m2:__XML__PARAM__udp_dst_any": {
                                                                    "m2:__XML__value": "any",
                                                                    "m2:__XML__PARAM__UDP_dst_portop": {
                                                                        "m2:__XML__value": "eq",
                                                                        "m2:__XML__PARAM__UDP_ip_dst_port0_str": {
                                                                            "m2:__XML__value": "bootps"
                                                                        }
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ],
                        "hardware": {
                            "profile": {
                                "portmode": {
                                    "__XML__PARAM__port-mode": {
                                        "__XML__value": "64x10G"
                                    }
                                }
                            }
                        },
                        "username": {
                            "__XML__PARAM__s0": {
                                "__XML__value": "admin",
                                "password": {
                                    "__DIGIT__5": {
                                        "__XML__PARAM__s3": {
                                            "__XML__value": "$5$7o4V1guL$QF46ooIxkK805/tyG4y.0EtmrBpOW.Hu6fF9JXmFkMA",
                                            "role": {
                                                "__XML__PARAM__s6": {
                                                    "__XML__value": "network-admin"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "class-map": [
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-icmp",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-icmp"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-ntp",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-ntp"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-arp"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-bfd"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-bpdu"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-dai"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-default"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-dhcpreq"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-dhcpresp",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-dhcp-relay"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-dpss"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-eigrp",
                                                "m4:match": [
                                                    {
                                                        "m4:access-group": {
                                                            "m4:name": {
                                                                "m4:__XML__PARAM__acs-grp-name": {
                                                                    "m4:__XML__value": "copp-system-acl-eigrp"
                                                                }
                                                            }
                                                        }
                                                    },
                                                    {
                                                        "m4:access-group": {
                                                            "m4:name": {
                                                                "m4:__XML__PARAM__acs-grp-name": {
                                                                    "m4:__XML__value": "copp-system-acl-eigrp6"
                                                                }
                                                            }
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-glean"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-igmp",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-igmp"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-ipmcmiss"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-l2switched"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-l3destmiss"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-l3mtufail"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-l3slowpath"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-mpls"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-pimautorp"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-pimreg",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-pimreg"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-ping",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-ping"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-ptp"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-routingProto1",
                                                "m4:match": [
                                                    {
                                                        "m4:access-group": {
                                                            "m4:name": {
                                                                "m4:__XML__PARAM__acs-grp-name": {
                                                                    "m4:__XML__value": "copp-system-acl-routingproto1"
                                                                }
                                                            }
                                                        }
                                                    },
                                                    {
                                                        "m4:access-group": {
                                                            "m4:name": {
                                                                "m4:__XML__PARAM__acs-grp-name": {
                                                                    "m4:__XML__value": "copp-system-acl-v6routingproto1"
                                                                }
                                                            }
                                                        }
                                                    }
                                                ]
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-routingProto2",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-routingproto2"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-selfIp"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-ttl1"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-v6routingProto2",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-v6routingProto2"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-s-vxlan"
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-snmp",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-snmp"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-ssh",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-ssh"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-stftp",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-stftp"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-tacacsradius",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-tacacsradius"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "type": {
                                    "control-plane": {
                                        "__XML__PARAM__opt_any_or_all": {
                                            "__XML__value": "match-any",
                                            "__XML__PARAM__cmap-name": {
                                                "__XML__value": "copp-telnet",
                                                "m4:match": {
                                                    "m4:access-group": {
                                                        "m4:name": {
                                                            "m4:__XML__PARAM__acs-grp-name": {
                                                                "m4:__XML__value": "copp-system-acl-telnet"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        ],
                        "policy-map": {
                            "type": {
                                "control-plane": {
                                    "__XML__PARAM__pmap-name": {
                                        "__XML__value": "copp-system-policy",
                                        "m5:class": [
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-default",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "400"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-l2switched",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "200"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-ping",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "100"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-l3destmiss",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "100"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-glean",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "500"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-selfIp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "500"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-l3mtufail",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "100"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-ttl1",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "100"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-ipmcmiss",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "400"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-l3slowpath",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "100"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-dhcpreq",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "300"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-dhcpresp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "300"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-dai",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "300"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-igmp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "400"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-routingProto2",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "1300"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-v6routingProto2",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "1300"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-eigrp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "200"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-pimreg",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "200"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-pimautorp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "200"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-routingProto1",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "1000"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-arp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "200"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-ptp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "1000"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-vxlan",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "1000"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-bfd",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "350"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-bpdu",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "12000"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-dpss",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "1000"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-s-mpls",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "100"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-icmp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "200"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-telnet",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "500"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-ssh",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "500"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-snmp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "500"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-ntp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "100"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-tacacsradius",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "400"
                                                            }
                                                        }
                                                    }
                                                }
                                            },
                                            {
                                                "m5:__XML__PARAM__cmap-name": {
                                                    "m5:__XML__value": "copp-stftp",
                                                    "m6:police": {
                                                        "m6:pps": {
                                                            "m6:__XML__PARAM__pps-val": {
                                                                "m6:__XML__value": "400"
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        ]
                                    }
                                }
                            }
                        },
                        "snmp-server": {
                            "user": {
                                "__XML__PARAM__s0": {
                                    "__XML__value": "admin",
                                    "__XML__PARAM__s1": {
                                        "__XML__value": "network-admin",
                                        "auth": {
                                            "md5": {
                                                "__XML__PARAM__s2": {
                                                    "__XML__value": "0xdcfb0051dc54304fadcb0c9facffa2fb",
                                                    "priv": {
                                                        "__XML__PARAM__s3": {
                                                            "__XML__value": "0xdcfb0051dc54304fadcb0c9facffa2fb",
                                                            "localizedkey": ""
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "interface": [
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Vlan1",
                                    "m10:ip": {
                                        "m10:address": {
                                            "m10:__XML__PARAM__ip-prefix": {
                                                "m10:__XML__value": "192.168.0.5/24"
                                            }
                                        }
                                    },
                                    "m9:no": {
                                        "m9:shutdown": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/1",
                                    "m12:speed": {
                                        "m12:__XML__PARAM__speed_val": {
                                            "m12:__XML__value": "1000"
                                        }
                                    },
                                    "m10:ip": {
                                        "m10:address": {
                                            "m10:__XML__PARAM__ip-prefix": {
                                                "m10:__XML__value": "192.168.1.5/24"
                                            }
                                        }
                                    },
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/2",
                                    "m12:speed": {
                                        "m12:__XML__PARAM__speed_val": {
                                            "m12:__XML__value": "1000"
                                        }
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/3",
                                    "m13:switchport": {
                                        "m13:mode": {
                                            "m13:__XML__PARAM__port_mode": {
                                                "m13:__XML__value": "trunk"
                                            }
                                        }
                                    },
                                    "m14:switchport": {
                                        "m14:trunk": {
                                            "m14:allowed": {
                                                "m14:vlan": {
                                                    "m14:__XML__PARAM__allow-vlans": {
                                                        "m14:__XML__value": "1"
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/4"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/5"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/6"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/7",
                                    "m12:speed": {
                                        "m12:__XML__PARAM__speed_val": {
                                            "m12:__XML__value": "1000"
                                        }
                                    },
                                    "m10:ip": {
                                        "m10:address": {
                                            "m10:__XML__PARAM__ip-prefix": {
                                                "m10:__XML__value": "192.168.2.7/24"
                                            }
                                        }
                                    },
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/8"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/9"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/10"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/11"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/12"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/13"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/14"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/15"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/16"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/17"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/18"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/19"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/20"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/21"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/22"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/23"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/24"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/25"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/26"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/27"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/28"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/29"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/30"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/31"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/32"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/33"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/34"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/35"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/36"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/37"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/38"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/39"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/40"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/41"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/42"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/43"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/44"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/45"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/46"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/47"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/48"
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/49/1",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/49/2",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/49/3",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/49/4",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/50/1",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/50/2",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/50/3",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/50/4",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/51/1",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/51/2",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/51/3",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/51/4",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/52/1",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/52/2",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/52/3",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "Ethernet1/52/4",
                                    "m11:no": {
                                        "m11:switchport": ""
                                    }
                                }
                            },
                            {
                                "__XML__PARAM__interface": {
                                    "__XML__value": "mgmt0",
                                    "m15:vrf": {
                                        "m15:member": {
                                            "m15:__XML__PARAM__vrf-name": {
                                                "m15:__XML__value": "management"
                                            }
                                        }
                                    },
                                    "m16:ip": {
                                        "m16:address": {
                                            "m16:__XML__PARAM__ip-prefix": {
                                                "m16:__XML__value": "192.168.1.5/24"
                                            }
                                        }
                                    }
                                }
                            }
                        ]
                    }
                }
            },
            "nf:source": {
                "nf:running": ""
            }
        }
    },
    "id": 1
    }
    return data
def getRestConfTrunk():
    data = {"jsonrpc": "2.0", "result": {"body": {"TABLE_allowed_vlans": {"ROW_allowed_vlans": {"interface": "Ethernet1/3", "allowedvlans": "1"
                }
            }, "TABLE_vtp_pruning": {"ROW_vtp_pruning": {"interface": "Ethernet1/3", "vtppruning_vlans": "1"
                }
            }, "TABLE_stp_forward": {"ROW_stp_forward": {"interface": "Ethernet1/3", "stpfwd_vlans": "1"
                }
            }, "TABLE_errored_vlans": {"ROW_errored_vlans": {"interface": "Ethernet1/3", "erroredvlans": "none"
                }
            }, "TABLE_interface": {"ROW_interface": {"interface": "Ethernet1/3", "native": 1, "status": "trunking", "portchannel": "--"
                }
            }
        }
    }, "id": 1
    }
    return data
def getRestConfTrunk():
    data = {"jsonrpc": "2.0", "result": {"body": {"TABLE_allowed_vlans": {"ROW_allowed_vlans": {"interface": "Ethernet1/3", "allowedvlans": "1"
                }
            }, "TABLE_vtp_pruning": {"ROW_vtp_pruning": {"interface": "Ethernet1/3", "vtppruning_vlans": "1"
                }
            }, "TABLE_stp_forward": {"ROW_stp_forward": {"interface": "Ethernet1/3", "stpfwd_vlans": "1"
                }
            }, "TABLE_errored_vlans": {"ROW_errored_vlans": {"interface": "Ethernet1/3", "erroredvlans": "none"
                }
            }, "TABLE_interface": {"ROW_interface": {"interface": "Ethernet1/3", "native": 1, "status": "trunking", "portchannel": "--"
                }
            }
        }
    }, "id": 1
    }
    return data
def getRestConfTrunk():
    data = {"jsonrpc": "2.0", "result": {"body": {"TABLE_allowed_vlans": {"ROW_allowed_vlans": {"interface": "Ethernet1/3", "allowedvlans": "1"
                }
            }, "TABLE_vtp_pruning": {"ROW_vtp_pruning": {"interface": "Ethernet1/3", "vtppruning_vlans": "1"
                }
            }, "TABLE_stp_forward": {"ROW_stp_forward": {"interface": "Ethernet1/3", "stpfwd_vlans": "1"
                }
            }, "TABLE_errored_vlans": {"ROW_errored_vlans": {"interface": "Ethernet1/3", "erroredvlans": "none"
                }
            }, "TABLE_interface": {"ROW_interface": {"interface": "Ethernet1/3", "native": 1, "status": "trunking", "portchannel": "--"
                }
            }
        }
    }, "id": 1
    }
    return data

def showVersion():
    data = {
    "jsonrpc": "2.0",
    "result": {
        "body": {
            "header_str": "Cisco Nexus Operating System (NX-OS) Software\nTAC support: http://www.cisco.com/tac\nCopyright (C) 2002-2020, Cisco and/or its affiliates.\nAll rights reserved.\nThe copyrights to certain works contained in this software are\nowned by other third parties and used and distributed under their own\nlicenses, such as open source.  This software is provided as is, and unless\notherwise stated, there is no warranty, express or implied, including but not\nlimited to warranties of merchantability and fitness for a particular purpose.\nCertain components of this software are licensed under\nthe GNU General Public License (GPL) version 2.0 or \nGNU General Public License (GPL) version 3.0  or the GNU\nLesser General Public License (LGPL) Version 2.1 or \nLesser General Public License (LGPL) Version 2.0. \nA copy of each such license is available at\nhttp://www.opensource.org/licenses/gpl-2.0.php and\nhttp://opensource.org/licenses/gpl-3.0.html and\nhttp://www.opensource.org/licenses/lgpl-2.1.php and\nhttp://www.gnu.org/licenses/old-licenses/library.txt.\n",
            "bios_ver_str": "5.0.0",
            "kickstart_ver_str": "9.3(6)",
            "nxos_ver_str": "9.3(6)",
            "bios_cmpl_time": "06/05/2018",
            "kick_file_name": "bootflash:///nxos.9.3.6.bin",
            "nxos_file_name": "bootflash:///nxos.9.3.6.bin",
            "kick_cmpl_time": "11/9/2020 23:00:00",
            "nxos_cmpl_time": "11/9/2020 23:00:00",
            "kick_tmstmp": "11/10/2020 16:30:21",
            "nxos_tmstmp": "11/10/2020 16:30:21",
            "chassis_id": "Nexus3000 C3064PQ Chassis",
            "cpu_name": "Intel(R) Celeron(R) CPU        P4505  @ 1.87GHz",
            "memory": 6025200,
            "mem_type": "kB",
            "proc_board_id": "FOC17211CCD",
            "host_name": "switch",
            "bootflash_size": 1596672,
            "slot0_size": 0,
            "kern_uptm_days": 0,
            "kern_uptm_hrs": 13,
            "kern_uptm_mins": 26,
            "kern_uptm_secs": 50,
            "rr_reason": "Reload due to unknown reason, possible power loss",
            "rr_sys_ver": "9.3(6)",
            "rr_service": "",
            "plugins": "Core Plugin, Ethernet Plugin",
            "manufacturer": "Cisco Systems, Inc.",
            "TABLE_package_list": {
                "ROW_package_list": {
                    "package_id": ""
                }
            }
        }
    },
    "id": 1
    }
    return data

def showVlan():
    data = {
    "jsonrpc": "2.0",
    "result": {
        "body": {
            "TABLE_vlanbrief": {
                "ROW_vlanbrief": {
                    "vlanshowbr-vlanid": "1",
                    "vlanshowbr-vlanid-utf": "1",
                    "vlanshowbr-vlanname": "default",
                    "vlanshowbr-vlanstate": "active",
                    "vlanshowbr-shutstate": "noshutdown",
                    "vlanshowplist-ifidx": "Ethernet1/2,Ethernet1/3,Ethernet1/4,Ethernet1/5,Ethernet1/6,Ethernet1/8,Ethernet1/9,Ethernet1/10,Ethernet1/11,Ethernet1/12,Ethernet1/13,Ethernet1/14,Ethernet1/15,Ethernet1/16,Ethernet1/17,Ethernet1/18,Ethernet1/19,Ethernet1/20,Ethernet1/21,Ethernet1/22,Ethernet1/23,Ethernet1/24,Ethernet1/25,Ethernet1/26,Ethernet1/27,Ethernet1/28,Ethernet1/29,Ethernet1/30,Ethernet1/31,Ethernet1/32,Ethernet1/33,Ethernet1/34,Ethernet1/35,Ethernet1/36,Ethernet1/37,Ethernet1/38,Ethernet1/39,Ethernet1/40,Ethernet1/41,Ethernet1/42,Ethernet1/43,Ethernet1/44,Ethernet1/45,Ethernet1/46,Ethernet1/47,Ethernet1/48"
                }
            },
            "TABLE_mtuinfo": {
                "ROW_mtuinfo": {
                    "vlanshowinfo-vlanid": "1",
                    "vlanshowinfo-media-type": "enet",
                    "vlanshowinfo-vlanmode": "ce-vlan"
                }
            }
        }
    },
    "id": 1
    }
    return data

def snmpshow():
    data = {
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
    return data

def echart(request):
    from uptime import uptime
    if request.user.is_authenticated:
        nf = Notification()
        try:
            count = 0
            for proc in psutil.process_iter():
                count = count + 1
            p = count
            network = pd.read_csv("dashboard/extraFiles/network.csv")
            time = [str(i) for i in list(network['TIME'])]
            download = [float(i) for i in list(network['DOWNLOAD'])]
            upload = [float(i) for i in list(network['UPLOAD'])]
            # print(time)
            # print(df)
            total_users = User.objects.count()
            web_websites = WebsiteLinks.objects.count()
            dc = addDataCenter.objects.count()
            notification = Notif.objects.filter(user=request.user, is_delete=False).count()
            device = DeviceCapibility.objects.count()
            camera = CameraMonitor.objects.all().count()
            label = []
            data = []
            process = ProcessUtil.objects.all()
            uptime = uptime() 

            virtualMemory = psutil.virtual_memory()[2]
            cpuPercentage = psutil.cpu_percent()
            colVm = ""
            colCPU = ""
            MemoryPoloCol = ""
            if (virtualMemory > 0) and (virtualMemory <= 60):
                colVm = "green"
            elif (virtualMemory > 60) and (virtualMemory <= 85):
                colVm = "orange"
            else:
                colVm = "red"
            if (cpuPercentage > 0) and (cpuPercentage <= 60):
                colCPU = "green"
            elif (cpuPercentage > 60) and (cpuPercentage <= 85):
                colCPU = "orange"
            else:
                colCPU = "red"
            svmem = psutil.virtual_memory() 
            usedRam = round(svmem.used/1024**3,2)
            AvailRam = round(svmem.available/1024**3,2)
            totalRam = round(svmem.total/1024**3,2)
            swapMemory = psutil.swap_memory()
            usedSMemory = round(swapMemory.used/(1000000000),2)
            availSMemory = round(swapMemory.free/(1000000000),2)
            hdd = psutil.disk_usage('/')
            totalStorage = round(hdd[0]/(1000000000),2)
            usedStorage = round(hdd[1]/(1000000000),2)
            freeStorage = round(hdd[2]/(1000000000),2)
            if ((usedStorage/totalStorage)*100 > 0) and ((usedStorage/totalStorage)*100 <= 60):
                MemoryPoloCol = "green"
            elif ((usedStorage/totalStorage)*100 > 60) and ((usedStorage/totalStorage)*100 <= 85):
                MemoryPoloCol = "orange"
            else:
                MemoryPoloCol = "red"
            # print((usedStorage/totalStorage)*100, MemoryPoloCol)
            i = 1
            for ps in process:
                label.append('L'+str(i))
                i = i+1
                data.append(ps.utilpercentage)
            return render(request, 'dashboard/charts.html',{'total_users':total_users,'web_websites':web_websites,'datacenter':dc, 'notification':notification,'device':device,'camera':camera,'labels':label, 'data':data, 'second':uptime,'virtualMemory':virtualMemory,'cpuPercentage':cpuPercentage,'usedRam':usedRam,'AvailRam':AvailRam,'totalRam':totalRam,'totalStorage':totalStorage,'usedStorage':usedStorage,'freeStorage':freeStorage, 'cpuGaugeColor':colCPU, 'vmGaugeColor':colVm,'download':download,'upload':upload,'networkTime':time,'usedSMemory':usedSMemory, 'availSMemory':availSMemory,'runningProcess':p,'MemoryPoloCol':MemoryPoloCol})
        except Exception as e:
            message = nf.show_result(result="Error", helping_text=str(e), title="Page can't be opened ", button_text="Visit Last Page", button_url="{% url 'home_page' %}", error_output=str(e))
                
            # apart from these add any show_results you want in any other variable names
            return render(request, 'dashboard/message_page.html',{
                'message' : message,
            })
    else:
        return redirect('login_page')

def UsedRam(request):
    try:
        count = 0
        for proc in psutil.process_iter():
            count = count + 1
        p = count
        network = pd.read_csv("dashboard/extraFiles/network.csv")
        time = [str(i) for i in list(network['TIME'])]
        download = [float(i) for i in list(network['DOWNLOAD'])]
        upload = [float(i) for i in list(network['UPLOAD'])]
        svmem = psutil.virtual_memory() 
        usedRam = round(svmem.used/1024**3,2)
        AvailRam = round(svmem.available/1024**3,2)
        totalRam = round(svmem.total/1024**3,2)
        virtualMemory = psutil.virtual_memory()[2]
        cpuPercentage = psutil.cpu_percent()
        colVm = ""
        colCPU = ""
        MemoryPoloCol = ""
        if (virtualMemory > 0) and (virtualMemory <= 60):
            colVm = "green"
        elif (virtualMemory > 60) and (virtualMemory <= 85):
            colVm = "orange"
        else:
            colVm = "red"
        if (cpuPercentage > 0) and (cpuPercentage <= 60):
            colCPU = "green"
        elif (cpuPercentage > 60) and (cpuPercentage <= 85):
            colCPU = "orange"
        else:
            colCPU = "red"
        swapMemory = psutil.swap_memory()
        usedSMemory = round(swapMemory.used/(1000000000),2)
        availSMemory = round(swapMemory.free/(1000000000),2)
        hdd = psutil.disk_usage('/')
        totalStorage = round(hdd[0]/(1000000000),2)
        usedStorage = round(hdd[1]/(1000000000),2)
        freeStorage = round(hdd[2]/(1000000000),2)
        if ((usedStorage/totalStorage)*100 > 0) and ((usedStorage/totalStorage)*100 <= 60):
            MemoryPoloCol = "green"
        elif ((usedStorage/totalStorage)*100 > 60) and ((usedStorage/totalStorage)*100 <= 85):
            MemoryPoloCol = "orange"
        else:
            MemoryPoloCol = "red"
        # print((usedStorage/totalStorage)*100, MemoryPoloCol)
        return JsonResponse({
            'usedRam':usedRam,
            'totalRam':totalRam,
            'availRam':AvailRam,
            'virtualMemory':virtualMemory,
            'cpuPercentage':cpuPercentage,
            'totalStorage':totalStorage,
            'usedStorage':usedStorage,
            'freeStorage':freeStorage,
            'cpuGaugeColor':colCPU,
            'vmGaugeColor':colVm,
            'download':download,
            'upload':upload,
            'networkTime':time,
            'usedSMemory':usedSMemory,
            'availSMemory':availSMemory,
            'runningProcess':p,
            'MemoryPoloCol':MemoryPoloCol
        })
    except Exception as e:
        print(str(e))

def networkspeed(request):
    try:
        formula = (10000000/1.192)
        st=speedtest.Speedtest()
        time = datetime.now().strftime("%H:%M:%S")
        download = round(st.download()/formula,2)
        upload= round(st.upload()/formula,2)
        List=[time,upload,download]
        with open('dashboard/extraFiles/network.csv', 'a') as f_object:
            writer_object = writer(f_object)
            #f_object.write("\n")
            writer_object.writerow(List)
            f_object.close()
        return JsonResponse({'status':'200'})
    except Exception as e:
        print(str(e))
        time = datetime.now().strftime("%H:%M:%S")
        List=[time,0,0]
        with open('dashboard/extraFiles/network.csv', 'a') as f_object:
            writer_object = writer(f_object)
            #f_object.write("\n")
            writer_object.writerow(List)
            f_object.close()
        return JsonResponse({'status':'200'})