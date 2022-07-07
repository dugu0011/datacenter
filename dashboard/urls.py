# Django imports
from django.urls import path, include
from dashboard.views import aboutUs, assetsWorld, GP,topology
# Custom imports
from . import views, views_home , views_apm
from dashboard.views import Test,Home,Registration,Login,ResetPassword,ProfileUpdate,Assets,assetsForms,ValidateIP,GetCapability, netconfTopology, AddDeviceCapability, ShowDeviceCapability,EditDeviceCapability,DelDeviceCapability,ScheduleDeviceCapability,EditDeviceCapabilityPage,DelDeviceCapabilityPage,autoDiscovery,Ansible 
# from view_home import akus_dashboard

# app_name = "dashboard"

urlpatterns = [

    path('test/', Test.as_view(), name = 'test_page'),
    path('apmMonitoring/getEverything/' , views_apm.mainFunction , name="APM_AJAX" ),
    # path('', views_home.akus_dashboard, name = 'home_page'),
    path('register/', Registration.as_view(), name = 'register_page'),
    path('login/', Login.as_view(), name = 'login_page'),
    path('reset-password/', ResetPassword.as_view(), name = 'reset_password_page'),
    path('edit-profile/', ProfileUpdate.as_view(), name = 'edit-profile'),
    path('assets/world/', assetsWorld.as_view(), name='assets-world'),
    path('assets/india/', Assets.as_view(), name='assets-india'),
    path('asset/datacenter/information/hall/', views.rackInformation, name='rack_information'),
    path('asset/datacenter/information/hall/<int:id>/', views.rack_page, name='rack_page'),
    path('asset/datacenter/information/hall/delete/<int:id>/', views.delete_rack, name='delete_rack'),
    path('asset/forms/rack/edit/<int:id>/', views.edit_rack, name='edit_rack'),
    path('asset/datacenter/information/hall/patchpanel/', views.patch_panel, name='patch_panel'),
    path('asset/datacenter/information/hall/patchpanel/form/', views.patchPanelForm, name='patchPanelForm'),
    path('asset/datacenter/information/hall/patchpanel/show/<int:id>/', views.patchPanelShow, name='patchPanelShow'),
    path('asset/datacenter/information/hall/device/<int:id>/', views.device_page, name='device_page'),
    path('asset/datacenter/information/hall/device/status/left/', views.change_device_status_left, name='change_device_status_left'),
    path('asset/datacenter/information/hall/device/status/right/', views.change_device_status_right, name='change_device_status_right'),
    path('asset/forms/', assetsForms.as_view(), name='assets-forms'),
    path('asset/forms/template/data/', views.getTemplateData, name='getTemplateData'),
    path('validate/ip-address/', ValidateIP.as_view(), name = 'validate_ip_address'),
    path('device/capability/test/', GetCapability.as_view(), name = 'get-capability-test'),
    # path('device/capability/',views.newPage, name='get-capability'),
    # path('device/capability/autodiscovering/', autoDiscovery.as_view(), name = 'autoDiscovery'),
    path('device/capability/add', AddDeviceCapability.as_view(), name = 'add-device-capability'),
    path('device/capability/show', ShowDeviceCapability.as_view(), name = 'show-device-capability'),
    path('device/capability/edit', EditDeviceCapabilityPage.as_view(), name = 'edit-device-capability-page'),
    path('device/capability/edit/<int:pk>/', EditDeviceCapability.as_view(), name = 'edit-device-capability'),
    path('device/capability/delete', DelDeviceCapabilityPage.as_view(), name = 'del-device-capability-page'),
    path('device/capability/delete/<int:pk>/', DelDeviceCapability.as_view(), name = 'del-device-capability'),
    path('device/capability/schedule/<int:id>/', ScheduleDeviceCapability.as_view(), name = 'schedule-device-capability'),
    path('device/capability/test/<int:id>/<value>/', views.myPath, name = 'myPath'),
    path('import/',views.importEx , name="import-export"),
    path('export/',views.exportData, name="exports"),
    path('groups/',GP.as_view(), name="group_data"),
    path('test/group/',views.getUserPermission,name="test_groups"),
    path('assign/group/',views.assignGroup,name="assign_groups"),
    path('ap/',views.fun1,name="ap"),  
    path('topview/',views.top,name="top-view"),  
    path('tempview/',views.temp,name="temp-view"),
    path('settings',views.setting,name="setting-view"),
    path('logout',views.logoutView,name="logout-view"),
    path('changestatus/<int:id>',views.changeStatus,name="change_status"),    
    path('show/user/',views.showUser,name="show_user"),
    path('asset/datacenter/hall/',views.newDataCenter, name='new_data_center'),
    path("data-browser/", include("data_browser.urls")),
    path('asset/datacenter/hall/<int:id>/',views.datacenter_page, name='datacenter'), 
    #NOTIFICATION AJAX HANDLING
    path('notificationMarkRead/<int:id>/',views.notification_update, name='notification_update'),
    path('notifications/',views.all_notifications, name='all_notifications'),
    path('notificationDelet/<int:id>/',views.notification_delete, name='notification_delete'),

    #Send Deive Mail
    path('senddevicemail/',views.send_device_via_mail, name='send_device_via_mail'),
    #menubar functionality
    path('reports/',views.reports,name='reports'),
    path('genearteRawDataReport/',views.genearte_raw_data_report,name='genearte_raw_data_report'),
    path('rackReport/',views.rack_report,name='rack_report'),
    path('networkGraph/',views.network_graph,name='network_graph'),
    path('plotlyGraph/', views.plotly_graph, name='plotly_graph'),
    path('homeNetwork/',views.home_network,name='home_network'),
    path('apmMonitoring/', views.apm_monitoring, name='apm_monitoring'),
    path('databaseMonitoring/',views.database_monitoring,name='database_monitoring'),
    path('storage/',views.storage,name='storage'),
    path('web/monitoring/',views.hexbin_graph, name='hexbin_graph'),
    path('web/monitoring/delete/<int:id>/',views.delete_web_monitor, name='delete_web_monitor'),
    path('cctv/delete/cctv/<int:id>/',views.delete_cctv, name='delete_cctv'),
    path('cctv/delete/camera/<int:id>/',views.delete_camera, name='delete_camera'),
    path('cctv/', views.cctv, name='cctv'),
    path('apmReport/',views.apmReport,name='apm_report'),
    path('mail/',views.mail,name='mail'),
    path('aboutUs/',views.aboutUs,name="about-us"),
    path('dataReview/',autoDiscovery.as_view(),name="data-review"),
    path('dataCheck/',views.dataCheck,name="data-check"),
    path('contactUs/',views.contactUs,name="contact-us"),
    path('raiseticket/',views.raiseTicket,name="raiseTicket"),
    path('viewraiseticket/<int:id>/',views.viewRaiseTicket,name="viewRaiseTicket"),
    path('topology/',topology.as_view(),name="topology-graph"),
    path('ansible/', Ansible.as_view(), name="ansible"),

    path('netconf/topology/',netconfTopology.as_view(),name="netconf-topology"),
    # path("data-browser/", include("data_browser.urls")),
    


    #add_data_center_cainet
    path('showrows',views.showRows, name='showrows'),
    path('showracks',views.showRacks, name='showracks'),
    #add_data_center_cainet

    path('tables/',views.table, name='table'),


    
    path('',views.echart, name="home_page"),
    #JSON RESPONSE FOR LIVE DATA
    path('charts/usedram/', views.UsedRam, name='UsedRam'),
    path('charts/networkspeed/', views.networkspeed, name='networkspeed'),
]
