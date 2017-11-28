Sample Linux role for OpenSwitch OPX
====================================

This sample role facilitates the configuration of various networking features supported using Linux commands in OpenSwitch OPX. This role currently supports LLDP, IPv4/IPv6 unicast routing, ARP and neighbor table updates, STP and ECMP configurations.

The ansible-role-opx-system role requires an SSH connection for connectivity to a Dell EMC OPX device. You can use any of the built-in Dell EMC Networking OS connection variables.

Installation
------------

    ansible-galaxy install open-switch.ansible-role-opx-system

Role variables
--------------

- Role is abstracted using the *ansible_net_os_name* variable that needs the value "openswitch".
- Any role variable with a corresponding state variable set to absent negates the configuration of that variable
- Setting an empty value for any variable negates the corresponding configuration
- Variables and values are case-sensitive

**ansible-role-opx-system keys**

| Key        | Type                      | Description                                             |
|------------|---------------------------|---------------------------------------------------------|
| ``opx_lldp`` | dictionary        | Configures LLDP parameters (see ``opx_lldp.*``)       |
| ``opx_lldp.tx-interval`` | integer         | Configures the LLDP transmit-delay         |
| ``opx_lldp.tx-hold`` | integer         | Configures LLDP transmit hold         |
| ``opx_lldp.fast-start-enable`` | string: present,absent | Enables/Disables fast start mechanism in LLDP, default: present |
| ``opx_lldp.fast-start-tx-interval`` | integer         | Configures LLDP fast transmit delay         |
| ``opx_route_v4`` | list         | Configures add/delete parameters for static entries to the IPv4 routing table (see ``opx_route_v4.*``)    |
| ``opx_route_v4.ip_and_mask`` | string (required)        | Configures the IPv4 address for route operation (192.168.11.1/24 format)    |
| ``opx_route_v4.interface`` | string       | Configures the interface name to be used for route add operation; if value is unspecified, *nexthop_ip* must be provided for adding a route   |
| ``opx_route_v4.nexthop_ip`` | list (of IPs)         | Configures a list of IP addresses of the next router in the routing path (192.168.11.3 format); more than one IP address in the list is used to configure ECMP (multiple paths) with same weightage using "ip route add" command    |
| ``opx_route_v4.state`` | string: present,absent | Specifies whether to add or remove an entry; if unspecified, the value is set to *present* by default  |
| ``opx_route_v6`` | list        | Configures add/delete parameters for static entries to the IPv6 routing table (see ``opx_route_v6.*``)    |
| ``opx_route_v6.ipv6_and_mask`` | string (required)        | Configures an IPv6 address for route operation (2001:4898:5808:ffa2::1/126 format)    |
| ``opx_route_v6.interface`` | string         | Specifies the interface name to be used for route add operation    |
| ``opx_route_v6.state`` | string: present,absent | Specifies whether to add or remove an entry; if unspecified, the value is set to *present* by default  |
| ``opx_arp`` | list       | Configures add/delete parameters for static entries to the ARP table (see ``opx_arp.*``)    |
| ``opx_arp.ipv4_address`` | string (required)        | Configures an IPv4 address     |
| ``opx_arp.mac_address`` | string        | Configures a MAC address   |
| ``opx_arp.state`` | string: present,absent | Specifies whether to add or remove an entry; if unspecified, the value is set to *present* by default  |
| ``opx_neigh`` | list         | Configures add/delete parameters for static entries to the neighbor table (see ``neigh_config.*``)    |
| ``opx_neigh.ipv6_address`` | string (required)       | Configures an IPv6 address    |
| ``opx_neigh.interface`` | string (required)        | Configures an interface name of the IPv6 address provided    |
| ``opx_neigh.mac_address`` | string        | Configures a MAC address   |
| ``opx_neigh.state`` | string: present,absent | Specifies whether to add or remove an entry; if unspecified, the value is set to *present* by default  |
| ``opx_stp`` | list         | Configures STP on/off on the specified bridge names (see ``opx_stp.*``)  |
| ``opx_stp.bridge`` | string (required)       | Specifies the bridge name    |
| ``opx_stp.state`` | string: present,absent | Enables/disables STP on a bridge; if unspecified, the value is set to *present* by default |

> **NOTE**: Asterisk (\*) denotes the default value if none is specified. 

Dependencies
------------

The *ansible-role-opx-system* role is built on modules included in the core Ansible code. These modules were added in Ansible version 2.4.0.

Example playbook
----------------

This example uses the *open-switch.ansible-role-opx-system* role to setup LLDP, IPv4/IPv6 static routes, ARP and neighbor table static entries, ECMP, and STP. It creates a *hosts* file with the switch details and corresponding variables. The hosts file should define the *ansible_net_os_name* variable "openswitch". 

It writes a simple playbook that only references the *ansible-role-opx-system* role. By including the role, you automatically get access to all of the tasks to configure Linux features. 

**Sample hosts file**

    leaf1 ansible_host= <ip_address> ansible_net_os_name="openswitch" ansible_ssh_user=<login> ansible_ssh_pass=<pwd> 
    
**Sample host_vars/leaf1**

    opx_lldp:
        tx-interval: 30
        tx-hold: 2
        fast-start-enable: true
        fast-start-tx-interval: 2
    opx_route_v4:
        - ip_and_mask: 10.18.0.0/24
          interface: e101-001-0
          nexthop_ip:
            - 10.16.1.3
            - 10.17.1.3
        - ip_and_mask: 10.18.0.0/24
          interface: e101-001-0
          state: absent
    opx_route_v6:
        - ipv6_and_mask: 0::0/0
          interface: eth0
        - ipv6_and_mask: 0::0/0
          state: absent
    opx_arp:
        - ipv4_address: 10.16.204.2
          mac_address: 00:0c:29:c0:94:bb
        - ipv4_address: 10.16.204.2
          state: absent
    opx_neigh:
        - ipv6_address: fec0::3
          mac_address: 02:01:02:03:04:03
          interface: eth0
        - ipv6_address: fec0::3
          interface: eth0
          state: absent
    opx_stp:
        - bridge: br100
        - bridge: br100
          state: absent
 
**Simple playbook to setup system - leaf.yaml**

    - hosts: leaf1
      roles:
         - { role: open-switch.ansible-role-opx-system, when: ansible_net_os_name is defined and ansible_net_os_name == "openswitch" }

**Run**

    ansible-playbook -i hosts leaf.yaml

(c) 2017 Dell EMC
