from import_export import resources
from .models import *
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User, Permission, Group
from django.contrib.sessions.models import Session


class LogEntryResource(resources.ModelResource):
    class Meta:
        model = LogEntry    
class ContentTypeResource(resources.ModelResource):
    class Meta:
        model = ContentType    
class UserResource(resources.ModelResource):
    class Meta:
        model = User    
class PermissionResource(resources.ModelResource):
    class Meta:
        model = Permission    
class GroupResource(resources.ModelResource):
    class Meta:
        model = Group    
class SessionResource(resources.ModelResource):
    class Meta:
        model = Session    
        
class AnsibleOutputResource(resources.ModelResource):
    class Meta:
        model = AnsibleOutput    

class ProductResource(resources.ModelResource):
    class Meta:
        model = Product    
    
class CameraMonitorResource(resources.ModelResource):
    class Meta:
        model = CameraMonitor    

class WebsiteLinksResource(resources.ModelResource):
    class Meta:
        model = WebsiteLinks    

class DCResource(resources.ModelResource):
    class Meta:
        model = DC    

class DataCenterCountryResource(resources.ModelResource):
    class Meta:
        model = DataCenterCountry    

class DataCenterStateResource(resources.ModelResource):
    class Meta:
        model = DataCenterState    

class DeviceEquipementResource(resources.ModelResource):
    class Meta:
        model = DeviceEquipement    

class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile    

class PersonResource(resources.ModelResource):
    class Meta:
        model = Person    

class PostResource(resources.ModelResource):
    class Meta:
        model = Post    

class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee    

class PagePermissionForGroupResource(resources.ModelResource):
    class Meta:
        model = PagePermissionForGroup    

class addDataCenterResource(resources.ModelResource):
    class Meta:
        model = addDataCenter    

class addDataCenterRowResource(resources.ModelResource):
    class Meta:
        model = addDataCenterRow    

class AddDataCenterRackcabinetResource(resources.ModelResource):
    class Meta:
        model = AddDataCenterRackcabinet    

class AddDeviceResource(resources.ModelResource):
    class Meta:
        model = AddDevice    

class DeviceTemplateResource(resources.ModelResource):
    class Meta:
        model = DeviceTemplate    
    
class DeviceDetailsResource(resources.ModelResource):
    class Meta:
        model = DeviceDetails    

class RRResource(resources.ModelResource):
    class Meta:
        model = RR    

class NotifResource(resources.ModelResource):
    class Meta:
        model = Notif    

class PatchPanelResource(resources.ModelResource):
    class Meta:
        model = PatchPanel    

class PatchPanelPortResource(resources.ModelResource):
    class Meta:
        model = PatchPanelPort    

class UptimeResource(resources.ModelResource):
    class Meta:
        model = Uptime    

class ProcessUtilResource(resources.ModelResource):
    class Meta:
        model = ProcessUtil    

class BrowserResource(resources.ModelResource):
    class Meta:
        model = Browser    

class SeriesResource(resources.ModelResource):
    class Meta:
        model = Series    

class Test1Resource(resources.ModelResource):
    class Meta:
        model = Test1    

class ServerDataResource(resources.ModelResource):
    class Meta:
        model = ServerData    

class DeviceCapibilityResource(resources.ModelResource):
    class Meta:
        model = DeviceCapibility
    
