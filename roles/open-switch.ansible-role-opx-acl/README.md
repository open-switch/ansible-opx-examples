Sample ACL role for OpenSwitch OPX
====================================

This sample role facilitates the configuration of ACL table/entries supported using CPS API in OPX. 

The ansible-role-opx-acl role requires an SSH connection for connectivity to a OPX device. 

Installation
------------

    ansible-galaxy install open-switch.ansible-role-opx-acl

Role variables
--------------

- Role is abstracted using the *ansible_net_os_name* variable that needs the value "openswitch".
- Variables and values are case-sensitive

**ansible-role-opx-acl keys**

| Key        | Type                      | Description                                             |
|------------|---------------------------|---------------------------------------------------------|
| ``opx_acl`` | list        | Configuration to create/delete of ACL table/entry. (see ``opx_acl.*``)       |
| ``opx_acl.operation`` | string: create,delete | Specifies whether to add or remove an an ACL table or entry; if unspecified, the value is set to *create* by default  |
| ``opx_acl.acl_tbl_attr_data`` | dictionary | Configures attibutes to be set in CPS for ACL table. For complete attributes, refer to the yang model of ACL table. (see ``acl_tbl_attr_data.*``) |
| ``acl_tbl_attr_data.name`` | string          | Configures the ACL table name         |
| ``acl_tbl_attr_data.stage`` | integer          | Configures 1 if INGRESS, 2 if EGRESS         |
| ``acl_tbl_attr_data.priority`` | integer          | Configures the priority for the ACL table         |
| ``acl_tbl_attr_data.allowed-match-fields`` | list of integer          | Configures the ACL table. Refer the ACL yang model for the values to be specified         |
| ``opx_acl.acl_entries`` | list | Configures attibutes to be set in CPS for ACL entries operation. For complete attributes, refer to the yang model of ACL entry. (see ``acl_entries.*``) |
| ``acl_entries.name`` | string         | Configures the ACL entry name         |
| ``acl_entries.priority`` | integer         | Configures the priority of the ACL entry         |

> **NOTE**: Asterisk (\*) denotes the default value if none is specified. 

Dependencies
------------

The *ansible-role-opx-acl* role is built on modules included in the core Ansible code. These modules were added in Ansible version 2.4.0.

Example playbook
----------------

This example uses the *open-switch.ansible-role-opx-acl* role to setup ACL table/entries using CPS Generic module. It creates a *hosts* file with the switch details and corresponding variables. The hosts file should define the *ansible_net_os_name* variable "openswitch". 

It writes a simple playbook that only references the *ansible-role-opx-acl* role. By including the role, you automatically get access to all of the tasks to configure ACL table. 

**Sample hosts file**

    leaf1 ansible_host= <ip_address> ansible_net_os_name="openswitch" ansible_ssh_user=<login> ansible_ssh_pass=<pwd> 
    
**Sample host_vars/leaf1**

    opx_acl:
      - operation: delete
        acl_tbl_attr_data:
          name: l2_mac
          id: 79
        acl_entries:
          - name: l2_mac_entry1
            id: 1
      - operation: create
        acl_tbl_attr_data:
          name: l2_mac
          stage: 1
          priority: 102
          allowed-match-fields: [3, 6, 9, 21]
        acl_entries:
          - name: l2_mac_entry1
            priority: 512
            match,0,type: 3
            match,0,SRC_MAC_VALUE,addr: '50:10:6e:00:00:00'
      - operation: delete
        acl_entries:
          - name: l2_mac_entry2
            table-id : 35
            id: 45

**Simple playbook to setup acl - leaf.yaml**

    - hosts: leaf1
      roles:
         - { role: open-switch.ansible-role-opx-acl, when: ansible_net_os_name is defined and ansible_net_os_name == "openswitch" }

**Run**

    ansible-playbook -i hosts leaf.yaml

(c) 2017 Dell EMC
