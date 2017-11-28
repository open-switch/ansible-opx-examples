Sample Linux Role for OpenSwitch OPX
=============================================

This sample role facilitates the configuration of Quality Of Service(QOS) parameters using CPS API in OPX.
The ansible-role-opx-qos role requires an SSH connection for connectivity to a Dell EMC OPX device.

Installation
------------

    ansible-galaxy install open-switch.ansible-role-opx-qos

Role Variables
--------------

- Role is abstracted using the *ansible_net_os_name* variable that needs the value "openswitch".
- Any role variable with a corresponding state variable set to absent negates the configuration of that variable
- Setting an empty value for any variable negates the corresponding configuration
- Variables and values are case-sensitive

**ansible-role-opx-qos keys**

| Key        | Type                      | Description                                             |
|------------|---------------------------|---------------------------------------------------------|
| ``opx_qos`` | list        | Configures create/delete QOS parameters. See the following opx_qos.*   |
| ``opx_qos.qos_wred_attr_data``| dict  | Configures the WRED entry                                  |
| ``opx_qos.qos_wred_attr_data.green-enable``| Integer  | Enable/Disable Green WRED entry. 1 for Enable 0 for Disable. If unspecified, the value is set to *0* by default                                  |
| ``opx_qos.qos_wred_attr_data.green-min-threshold``| Integer | Minimum threshold in bytes after which packets will be dropped based on the drop probability|
| ``opx_qos.qos_wred_attr_data.green-max-threshold``| Integer | Maximum threshold in bytes after which packets will be tail dropped|
| ``opx_qos.qos_wred_attr_data.green-drop-probability``| Integer |Percentage probability with which packets will be dropped when minimum threshold is reached. If unspecified, the value is set to *100* by default|
| ``opx_qos.qos_wred_attr_data.yellow-enable``| Integer  | Enable/Disable Yellow WRED entry 1 for Enable 0 for Disable. If unspecified, the value is set to *0* by default |
| ``opx_qos.qos_wred_attr_data.yellow-min-threshold``| Integer | Minimum threshold in bytes after which packets will be dropped based on the drop probability|
| ``opx_qos.qos_wred_attr_data.yellow-max-threshold``| Integer | Maximum threshold in bytes after which packets will be tail dropped|
| ``opx_qos.qos_wred_attr_data.yellow-drop-probability``| Integer |Percentage probability with which packets will be dropped when minimum threshold is reached. If unspecified, the value is set to *100* by default|
| ``opx_qos.qos_wred_attr_data.weight``|Integer | The average queue size depends on the previous average as well as the current size of the queue. The Weight indicates the importance of previous average queue length compared to the current queue size. If unspecified, the value is set to *0* by default |
| ``opx_qos.qos_wred_attr_data.npu-id-list``| list| list of NPU Id's|
| ``opx_qos.qos__scheduler``| dict  | Configures the scheduler profile entry|
| ``opx_qos.qos__scheduler.algorithm``| Integer | The parameter gets the type of scheduling algorithm. 1 for Strict priority, 2 for WDD and 3 for WDRR. If unspecified, the value is set to *3* (WDRR) by default |
| ``opx_qos.qos__scheduler.weight``| Integer | Scheduling weight |
| ``opx_qos.qos__scheduler.meter-type``| Integer | The parameter get the meter type. 1 for Packet and 2 for Byte |
| ``opx_qos.qos__scheduler.min-rate``| long  | Guaranteed bandwidth shape rate [bytes/sec or PPS]|
| ``opx_qos.qos__scheduler.min-burst``| long  | Guaranteed burst for bandwidth shape rate [Bytes or Packets]|
| ``opx_qos.qos__scheduler.max-rate``| long  | Maximum bandwidth shape rate [bytes/sec or PPS] |
| ``opx_qos.qos__scheduler.max-burst``| long  | Maximum burst for bandwidth shape rate [Bytes or Packets] |
| ``opx_qos.qos_dscp_map_id`` | dict  | Configures attibutes to be set in CPS for dscp map ID entry.                                                                                                                                     |
| ``opx_qos.qos_dscp_map_id.name``| string| Optional user-provided name for the map |
| ``opx_qos.qos_dscp_map_entry`` | dict  | Configures attibutes to be set in CPS for dscp map entry.                                                                                                                                     |
| ``opx_qos.qos_dscp_map_entry.tc``| Integer | Traffic class|
| ``opx_qos.qos_dscp_map_entry.color`` | Integer | Packet color that given dscp is mapped to |
 | ``opx_qos.qos_dscp_map_entry.dscp``  | Integer | Incoming dscp value |
| ``opx_qos.qos_tc_map_id`` | dict  | Configures attibutes to be set in CPS for traffic class map ID entry.                                                                                                                              |
| ``opx_qos.qos_tc_map_id.name``| string| Optional user-provided name for the map |
| ``opx_qos.qos_tc_map_entry`` | dict  | Configures attibutes to be set in CPS traffic class map entry.                                                                                                                                  |
| ``opx_qos.qos_tc_map_entry.tc``| Integer | Traffic class |
| ``opx_qos.qos_tc_map_entry.color`` | Integer | Packet color |
| ``opx_qos.qos_tc_map_entry.dscp`` | Integer | egress dscp value for this traffic class and color|
| ``opx_qos.qos_policer_meter`` | dict  | Configures attibutes to be set in CPS meter entry                                                                                                                                              |
| ``opx_qos.qos_policer_meter.peak-rate``| long | Peak rate in byte-per-second or packets. Only valid for Two Rate Tri Color Meter |
| ``opx_qos.qos_policer_meter.type`` | Integer | The parameter get the meter type. 1 for Packet and 2 for Byte |
| ``opx_qos.qos_policer_meter.mode`` | Integer | The meter mode type. 1 for Single-Rate, 2 for Two-Rate, 3 for Two-Color and 4 for storm control |
| ``opx_qos.qos_queue_set_data``| dict  | Configures attibutes to be set in CPS for queue entry.                                                                                                                                         |
| ``opx_qos.qos_queue_set_data.queue-number`` | Integer| locally unique id within a port and a specific queue type |
| ``opx_qos.qos_queue_set_data.type`` | Integer | 1 for UNICAST Queue 2 for Multicast queue | 
| ``opx_qos.qos_queue_set_data.port-id`` | Integer | port number|
| ``opx_qos.qos_queue_set_data.buffer-profile-id``  | Integer | buffer profile ID |
| ``opx_qos.qos_queue_unset_data``| dict  | Configures attibutes to be unset in CPS for queue entry.                                                                                                                                     |
| ``opx_qos.qos_queue_unset_data.queue-number`` | Integer| locally unique id within a port and a specific queue type |
| ``opx_qos.qos_queue_unset_data.type`` | Integer | 1 for Unicast Queue 2 for Multicast queue | 
| ``opx_qos.qos_queue_unset_data.port-id`` | Integer | port number|
| ``opx_qos.qos_queue_unset_data.buffer-profile-id``  | Integer | buffer profile ID |
| ``opx_qos.qos_queue_unset_data.wred``   | Integer | WRED profile ID |
| ``opx_qos.qos_ing_port``| dict  | Configures attibutes to be set in CPS for port ingress entry.                                                                                                                                        |
| ``opx_qos.qos_ing_port.port-id`` | Integer | port number|
| ``opx_qos.qos_egr_port``| dict  | Configures attibutes to be set in CPS for port egress entry.                                                                                                                                        |
| ``opx_qos.qos_egr_port.port-id`` | Integer | port number|

> **NOTE**: Asterisk (\*) denotes the default value if none is specified.

Dependencies
------------

The *ansible-role-opx-qos* role is built on modules included in the core Ansible code. These modules were added in Ansible version 2.4.0.

Example Playbook
----------------

This example uses the *open-switch.ansible-role-opx-qos* role to setup QOS using CPS Generic module. It creates a *hosts* file with the switch details and corresponding variables. The hosts file should define the *ansible_net_os_name* variable "openswitch".

It writes a simple playbook that only references the *ansible-role-opx-qos* role. By including the role, you automatically get access to all of the tasks to configure QOS features.


**Sample hosts file**

    leaf1 ansible_host= <ip_address> ansible_net_os_name="openswitch" ansible_ssh_user=<login> ansible_ssh_pass=<pwd>
    
**Sample host_vars/leaf1**
 
	opx_qos:
	  - operation: create
	    qos_wred_attr_data:
	      green-enable: 1
	      green-min-threshold: 10
	      green-max-threshold: 20
	      green-drop-probability: 1
	      yellow-enable: 1
	      yellow-min-threshold: 10
	      yellow-max-threshold: 20
	      yellow-drop-probability: 3
	      weight: 8
	      ecn-enable: 1
	      npu-id-list: [0]
	    qos_scheduler:
	      name: strict priority
	      algorithm: 1
	      weight: 2
	      meter-type: 1
	      min-rate: 256
	      min-burst: 300
	      max-rate: 1000
	      max-burst: 1200
	    qos_dscp_map_id:
	      switch-id: 0
	      name: dscp_map
	    qos_dscp_map_entry:
	      base-qos/dscp-to-tc-color-map/entry/tc: 0
	      base-qos/dscp-to-tc-color-map/entry/color: 1
	      base-qos/dscp-to-tc-color-map/entry/dscp: 40
	    qos_tc_map_id:
	      switch-id: 0
	      name: dscp_map
	    qos_tc_map_entry:
	      base-qos/tc-color-to-dscp-map/entry/tc: 0
	      base-qos/tc-color-to-dscp-map/entry/color: 1
	      base-qos/tc-color-to-dscp-map/entry/dscp: 40
	    qos_policer_meter:
	      type: 1
	      peak-rate: 10
	      mode: 4
	  - operation: set
	    qos_queue_set_data:
	      port-id: 17
	      queue-number: 4
	      type: 2
	      buffer-profile-id: 4
	    qos_queue_unset_data:
	      port-id: 17
	      queue-number: 4
	      type: 2
	      buffer-profile-id: 0
	      wred-id: 0
	    qos_ing_port:
	      port-id: 16
	    qos_egr_port:
	      port-id: 17
	  - operation: delete
	    qos_wred_attr_data:

	 
**Simple playbook to setup system - leaf.yaml**

    - hosts: leaf1
      roles:
         - { role: open-switch.ansible-role-opx-qos, when: ansible_net_os_name is defined and ansible_net_os_name == "openswitch" }


**Run**

    ansible-playbook -i hosts leaf.yaml
    
(c) 2017 Dell EMC
