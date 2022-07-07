from django import forms
from django.forms import fields, ModelForm


from .models import Group, PagePermissionForGroup, PatchPanel, RaiseTicket

class PagePermissionForGroupForm(ModelForm):
    class Meta:
        model = PagePermissionForGroup
        fields = ('groupname', 'name_of_page', 'all_perm', 'read_perm', 'write_perm', 'delete_perm', 'update_perm', 'patch_perm',)

class PatchPanelForm(ModelForm):
    class Meta:
        model = PatchPanel
        fields = ('rack', 'name', 'incoming', 'outgoing',)

class RaiseTicketForm(ModelForm):
    class Meta:
        model = RaiseTicket
        fields = ('fname', 'lname', 'email','img','subject', 'msg',)
