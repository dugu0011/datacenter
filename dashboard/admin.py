from django.contrib import admin
from dashboard.models import *
# Register your models here.

admin.site.register(DataCenterCountry)
admin.site.register(DataCenterState)
admin.site.register(UserProfile)
admin.site.register(DeviceEquipement)
admin.site.register(DC)
admin.site.register(RR)
admin.site.register(WebsiteLinks)
admin.site.register(Product)
admin.site.register(Notif)
admin.site.register(addDataCenter)
admin.site.register(AddDevice)
admin.site.register(DeviceDetails)
admin.site.register(addDataCenterRow)
admin.site.register(AddDataCenterRackcabinet)
admin.site.register(PatchPanel)
admin.site.register(PatchPanelPort)
admin.site.register(Uptime)
admin.site.register(ProcessUtil)
admin.site.register(Browser)
admin.site.register(Series)
admin.site.register(DeviceTemplate)
admin.site.register(ServerData)
admin.site.register(DeviceCapibility)
admin.site.register(CameraMonitor)
admin.site.register(ContactUs)
admin.site.register(RaiseTicket)


from .models import  Person, Post
from import_export.admin import ImportExportModelAdmin
from .models import Employee

@admin.register(Person)
class PersonAdmin(ImportExportModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(ImportExportModelAdmin):
    pass

@admin.register(Employee)
class EmployeeAdmin(ImportExportModelAdmin):
    pass


@admin.register(PagePermissionForGroup)
class PagePermissionAdmin(ImportExportModelAdmin):
    pass