"""

File: devices/views/interface.py

Purpose:
    This code is a class based view used to render
    and provide functions for the interface details view.

    Functions allow users to view interface configuration,
    apply and remove access lists from an interface

"""
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from devices.controllers import cisco_controller as controller
from devices.models import *


class InterfaceDetails(View):
    template = 'device_interface.html'
    success_redirect = 'devices:Interface-Details'
    exception_redirect = 'devices:Device-Manager'

    # get interface configuration
    # **kwargs = devices primary key
    # returns interface details page
    def get(self, request, **kwargs):
        device_id = self.kwargs['device_id']
        intface = self.kwargs['interface']
        device = Device.get_device(device_id)
        args = {'device': device, 'interface': intface, 'details': controller.get_interface_details(device, intface),
                'int_acl': controller.get_interface_ip(device, intface), 'acl': controller.get_acl(device)}

        try:
            return render(request, self.template, args)
        except Exception as e:
            messages.error(request, 'Error - ' + str(e))
            return redirect(self.exception_redirect)

    # post interface configuration
    # **kwargs = devices primary key
    # returns interface details page
    def post(self, request, **kwargs):

        device_id = self.kwargs['device_id']
        intface = self.kwargs['interface']
        device = Device.get_device(device_id)

        # apply access list to interface
        if 'apply' in request.POST:
            # poor form implementation
            acl = request.POST.get('acl')
            direction = request.POST.get('dir')
            c = controller.apply_acl(request.user, device, intface, acl, direction)
            messages.success(request, str(c))

        # remove access list from interface
        if 'remove' in request.POST:
            # poor form implementation
            acl = request.POST.get('acl')
            direction = request.POST.get('dir')
            c = controller.remove_acl(request.user, device, intface, acl, direction)
            messages.success(request, str(c))

        try:
            return redirect(self.success_redirect, device_id, intface)
        except Exception as e:
            messages.error(request, 'Unexpected Error - ' + str(e))
            return redirect(self.exception_redirect)
