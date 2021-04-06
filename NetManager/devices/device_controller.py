"""

CISCO DEVICE CONTROLLER

"""

from netmiko import ConnectHandler
from .models import Security
from devices import alert_generator


def connect(d):
    device = {
        'device_type': 'cisco_ios',
        'ip': d.host,
        'username': Security.get_username(d),
        'password': Security.get_password(d),
        'secret': Security.get_secret(d),
        'port': 22,
    }
    return device


# retrieve devices information
def retrieve(device, command):
    try:
        c = ConnectHandler(**connect(device))
        output = c.send_command(command ,use_textfsm=True)
        print(output)
        c.disconnect()
    except Exception as e:
        output = e
    return output


# send configuration to devices
def configure(d, command):
    try:
        c = ConnectHandler(**connect(d))
        c.enable()
        c.send_config_set(command)
        c.disconnect()
        return True
    except Exception as e:
        return e


# test connection to all devices
def connect_test(user_devices):
    for i in user_devices:
        try:
            # if connection established
            c = ConnectHandler(**connect(i))
            i.status = True
            c.disconnect()
        except:
            i.status = False
        i.save()


# get show ip interface brief output
# d = devices object
def get_interfaces(d):
    output = retrieve(d, 'show ip interface brief')
    return output


# get show version output
# d = devices object
def get_version(d):
    output = retrieve(d, 'show version')
    return output


# get show ip access-lists output
# d = devices object
def get_acl(d):
    output = retrieve(d, 'show ip access-lists')
    return output


# get show interface <interface> output
# d = devices object
# i = interface as string
def get_interface_details(d, i):
    output = retrieve(d, 'show interface ' + i)
    return output


# get show ip interface <interface> output
# d = devices object
# i = interface as string
def get_interface_ip(d, i):
    output = retrieve(d, 'show ip interface ' + i)
    return output


# save config with Netmiko save_config() function
def save_config(user, d):
    try:
        c = ConnectHandler(**connect(d))
        c.save_config()
        c.disconnect()
        return alert_generator.save_alert(user, d)
    except Exception as e:
        return str(e)


# Configure interface with ip address
# d = devices object
# form = InterfaceForm
def config_interface(user, d, form):
    intface = form.cleaned_data.get('interface')
    ip = form.cleaned_data.get('ip_address')
    mask = form.cleaned_data.get('subnet')
    enable = form.cleaned_data.get('enable')
    if enable:
        cmd = ['interface ' + intface, 'ip address ' + ip + ' ' + mask, 'no shutdown']
    else:
        cmd = ['interface ' + intface, 'ip address ' + ip + ' ' + mask, 'shutdown']
    c = configure(d, cmd)
    if c:
        return alert_generator.configuration_alert(user, d, intface, ip, 'CONFIG')
    else:
        return str(c)


# Reset specific interface to default
# d = devices object
# intface = interface as string
def reset_interface(user, d, intface):
    cmd = ['interface ' + intface, 'no ip address', 'shutdown']
    c = configure(d, cmd)
    if c:
        return alert_generator.configuration_alert(user, d, intface, None, 'RESET')
    else:
        return str(c)


# Reset all unused interfaces
# d = devices object
def disable_interfaces(user, d):
    interfaces = retrieve(d, 'show ip int brief')
    for i in interfaces:
        if i['ipaddr'] == 'unassigned' and i['status'] != 'administratively down':
            cmd = ['interface ' + i['intf'], 'shutdown']
            configure(d, cmd)
    return True


# Create new access lists & add to access lists
# d = devices object
# form = AccessListForm
def create_acl(user, d, form):
    acl_type = form.cleaned_data.get('type')
    acl_name = form.cleaned_data.get('name')
    statement = form.cleaned_data.get('statement')
    cmd = ['ip access-list ' + acl_type + " " + acl_name, statement]
    c = configure(d, cmd)
    if c:
        return alert_generator.security_alert(user, d, acl_name, None, 'CREATE')
    else:
        return str(c)


# Delete access lists from devices
# d = devices object
# acl_name = list name as string
def delete_acl(user, d, acl_name):
    cmd = ['no ip access-list ' + acl_name]
    c = configure(d, cmd)
    if c:
        return alert_generator.security_alert(user, d, acl_name, None, 'DELETE')
    else:
        return str(c)


# Apply access list to interface
# d = devices object
# intface = interface as string
# acl_name = access list as string
# direction = direction as string
def apply_acl(user, d, intface, acl_name, direction):
    cmd = ['interface ' + intface, 'ip access-group ' + acl_name + ' ' + direction]
    c = configure(d, cmd)
    if c:
        return alert_generator.security_alert(user, d, acl_name, intface, 'APPLY')
    else:
        return str(c)


# Remove access list from interface
# d = devices object
# intface = interface as string
# acl_name = access list as string
# direction = direction as string
def remove_acl(user, d, intface, acl_name, direction):
    cmd = ['interface ' + intface, 'no ip access-group ' + acl_name + ' ' + direction]
    c = configure(d, cmd)
    if c:
        return alert_generator.security_alert(user, d.name, acl_name, intface, 'REMOVE')
    else:
        return str(c)