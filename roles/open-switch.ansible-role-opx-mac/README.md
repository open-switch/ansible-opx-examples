Sample MAC role for OpenSwitch OPX
====================================

This sample role facilitates the configuration of MAC table supported using CPS API in OPX. 

The ansible-role-opx-mac role requires an SSH connection for connectivity to a Dell EMC OPX device. 

Installation
------------

    ansible-galaxy install open-switch.ansible-role-opx-mac

Role variables
--------------

- Role is abstracted using the *ansible_net_os_name* variable that needs the value "openswitch".
- Variables and values are case-sensitive

**ansible-role-opx-mac keys**

| Key        | Type                      | Description                                             |
|------------|---------------------------|---------------------------------------------------------|
| ``opx_mac`` | list        | Configuration to create/delete static entry into MAC table. (see ``opx_mac.*``)       |
| ``opx_mac.operation`` | string: create,delete | Specifies whether to add or remove an entry; if unspecified, the value is set to *create* by default  |
| ``opx_mac.mac_attr_type`` | dictionary | Configures attibutes types to be set in CPS . For the complete attributes, refer to the yang model of MAC table. |
| ``opx_mac.mac_attr_data`` | dictionary | Configures attibutes to be set in CPS for MAC entry. For the complete attributes, refer to the yang model of MAC table. (see ``mac_attr_data.*``) |
| ``mac_attr_data.mac-address`` | string          | Configures the MAC address         |
| ``mac_attr_data.ifindex`` | integer          | Configures the interface index         |
| ``mac_attr_data.vlan`` | string          | Configures the vlan ID         |

> **NOTE**: Asterisk (\*) denotes the default value if none is specified. 

Dependencies
------------

The *ansible-role-opx-mac* role is built on modules included in the core Ansible code. These modules were added in Ansible version 2.4.0.

Example playbook
----------------

This example uses the *open-switch.ansible-role-opx-mac* role to setup MAC entries using CPS Generic module. It creates a *hosts* file with the switch details and corresponding variables. The hosts file should define the *ansible_net_os_name* variable "openswitch". 

It writes a simple playbook that only references the *ansible-role-opx-mac* role. By including the role, you automatically get access to all of the tasks to configure MAC table. 

**Sample hosts file**

    leaf1 ansible_host= <ip_address> ansible_net_os_name="openswitch" ansible_ssh_user=<login> ansible_ssh_pass=<pwd> 
    
**Sample host_vars/leaf1**

    opx_mac:
      - operation: create
        mac_attr_data:
          mac-address: "aa:0a:0b:cc:0d:0e"
          ifindex: 18
          vlan: "1"
      - operation: delete
        mac_attr_data:
          mac-address: "aa:0a:0b:cc:0d:0e"
          ifindex: 18
          vlan: "1"

**Simple playbook to setup mac - leaf.yaml**

    - hosts: leaf1
      roles:
         - { role: open-switch.ansible-role-opx-mac, when: ansible_net_os_name is defined and ansible_net_os_name == "openswitch" }

**Run**

    ansible-playbook -i hosts leaf.yaml

(c) 2017 Dell EMC
