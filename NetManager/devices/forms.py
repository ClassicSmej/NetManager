"""

DEVICES FORMS

* DEVICE FORM
    * ADD DEVICE
    * EDIT DEVICE

* SECURITY FORM
    * EDIT DEVICE SECURITY SETTINGS

* INTERFACE FORM
    * CONFIGURING INTERFACES

* ACL FORM
    * CREATING ACCESS LISTS

"""

from django import forms
from devices.models import Device, Security


class DeviceForm(forms.ModelForm):
    name = forms.CharField(label="Device Name", widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))
    type = forms.CharField(label="Device Type", widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))
    host = forms.CharField(label="SSH Address", widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))
    vendor = forms.CharField(label='Vendor', widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'true'}), initial='Cisco')
    location = forms.CharField(label="Location", widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))
    contact = forms.CharField(label='Contact', widget=forms.TextInput(attrs={'class': 'form-control textbox edit', 'disabled': 'true'}))

    class Meta:
        model = Device
        fields = [
            'name',
            'type',
            'host',
            'vendor',
            'location',
            'contact',
        ]


class SecurityForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control textbox security', 'disabled': 'true'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control textbox security', 'disabled': 'true'}))
    secret = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control textbox security', 'disabled': 'true'}))

    class Meta:
        model = Security
        fields = [
            'username',
            'password',
            'secret',
        ]


class InterfaceForm(forms.Form):
    interface = forms.CharField(widget=forms.HiddenInput)
    ip_address = forms.CharField(label='IP Address', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter IP Address'}))
    mask = forms.CharField(label='', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Subnet Mask'}))
    enable = forms.BooleanField(label='Enable Interface', required=False, initial=True)


class AclForm(forms.Form):
    type_choices = [('standard', 'Standard'), ('extended', 'Extended')]

    type = forms.CharField(label='Access List Type', widget=forms.Select(choices=type_choices, attrs={'class': 'form-control'}))
    name = forms.CharField(label='Access List Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Access List Name'}))
    statement = forms.CharField(label='Access List Command', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. permit tcp any any'}))

