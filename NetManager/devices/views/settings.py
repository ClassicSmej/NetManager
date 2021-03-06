"""

File: devices/views/settings.py

Purpose:
    This code is a class based view used to render
    and provide functions for the device settings view.

    Functions allow users to edit and delete devices
    from the database including the security information

"""
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from devices.forms import *
from devices.models import *
from devices.factory import alert_factory


class DeviceSettings(View):
    template = 'device_settings.html'
    success_redirect = 'devices:Device-Settings'
    exception_redirect = 'devices:Device-Manager'

    # get device database information
    # **kwargs = devices primary key
    # returns device settings page
    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        device = Device.get_device(device_id)
        device_form = DeviceForm(instance=device)
        security_form = SecurityForm(instance=Security.get_device_security(device_id))
        args = {'device': device, 'security_form': security_form, 'device_form': device_form}

        try:
            return render(request, self.template, args)
        except Exception as e:
            messages.error(request, 'Error - ' + str(e))
            return redirect(self.exception_redirect)

    # post device information
    # **kwargs = devices primary key
    # returns device settings page (except 'delete')
    def post(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        device = Device.get_device(device_id)

        # edit device information
        if 'edit' in request.POST:
            form = DeviceForm(request.POST or None, instance=device)
            if form.is_valid():
                device.save()
                alert = alert_factory.device_alert(request.user, device, 'UPDATE')
                messages.success(request, alert)

        # edit device security information
        if 'security' in request.POST:
            s = Security.get_device_security(device_id)
            form = SecurityForm(request.POST or None, instance=s)
            if form.is_valid():
                s.save()
                alert = alert_factory.device_alert(request.user, s.device, 'SECURITY')
                messages.success(request, alert)

        # delete device - returns device manager
        if 'delete' in request.POST:
            device.delete()
            alert = alert_factory.device_alert(request.user, device, 'DELETE')
            messages.success(request, alert)
            return redirect('devices:Device-Manager')

        try:
            return redirect(self.success_redirect, device_id)
        except Exception as e:
            messages.error(request, 'Unexpected Error - ' + str(e))
            return redirect(self.exception_redirect)
