#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2017, Ansible by Red Hat, inc
# Copyright (c) 2017 Dell Inc.
#
# This file is part of Ansible by Red Hat
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
---
module: opx_generic_cps
version_added: "2.4"
short_description: To configure OPX switch programatically using
                   generic CPS API
description:
  - This module shall be used to configure OPX switch
  programatically
options:
  module_name:
    description:
      - name of CPS module
  attr_data:
    description:
      - data to be configured
  operation:
    description:
      - Operation of the configuration.
    default: create 
    choices: ['create', 'delete', 'set']
  qualifier:
    description:
      - CPS qualifier
    default: target
    choices: ['target','observed','proposed','realtime']
"""

EXAMPLES = """
- name: configure VLAN ID
  opx_generic_cps:
    module_name: 20
    attr_data: {
         "base-if-vlan/if/interfaces/interface/id": 103,
         "if/interfaces/interface/type": "ianaift:l2vlan"
    }
    state: present
- name: To Configure ACL entry
  opx_generic_cps:
    - module_name: "base-acl/entry"
      attr_data: {
         "table-id": 21,
         "match,0,type": 3,
         "match,0,SRC_MAC_VALUE,addr": '50:10:6e:00:00:00'
      }
"""

RETURN = """
"""

from ansible.module_utils.basic import *   # NOQA

import sys
import cps_object
import cps
import cps_utils

RESULT = {}

CREATE = 'create'
ID = 'id'
CPS_CHANGE = 'change'

def configure(qualifier, operation, module_name, attr_type, attr_data):
    """
    Perform create or delete or set of the specific module
    """
    if attr_type:
        for key, val in attr_type.iteritems():
            cps_utils.cps_attr_types_map.add_type(key,   val)

    cps_obj = cps_object.CPSObject(module=module_name, qual=qualifier)
    for key, val in attr_data.iteritems():
        """
        check if the key is a simple or embedded attrribute
        """
        if isinstance(key, str):
            if key.count(','):
                key = key.split(',')
                key_length = len(key)
                num_of_attr = key_length - 2
                cps_obj.add_embed_attr(key, val, num_of_attr)
            else:
                cps_obj.add_attr(key, val)
        
    if not cps_obj:
        return ValueError

    """
    Execute cps transaction
    """
    updates = (operation, cps_obj.get())
    cps_resp = cps_utils.CPSTransaction([updates]).commit()
    if not cps_resp:
        error_msg = "Transaction error while " + operation
        raise RuntimeError(error_msg)

    RESULT["response"] = str(cps_resp)

    """
    Extract the key value from the cps response
    """
    if operation == CREATE:
        try:
            cps_resp = cps_object.CPSObject(module=module_name,
                                        obj=cps_resp[0][CPS_CHANGE])
            if cps_resp:
                id_key = module_name + "/" + ID
                cps_resp_id = cps_resp.get_attr_data(id_key)
                RESULT["response_id"] = str(cps_resp_id)
        except:
            print("ID does not exist")

def run(module):
    qualifier = module.params['qualifier']
    module_name = module.params['module_name']
    attr_type = module.params["attr_type"]
    attr_data = module.params["attr_data"]
    operation = module.params['operation']

    configure(module_name=module_name, attr_type=attr_type, attr_data=attr_data, operation=operation, qualifier=qualifier)
    changed = True

    RESULT["changed"] = changed

def main():
    """
    main entry point for module execution
    """
    argument_spec = dict(
	qualifier = dict(required=False,
	                 default='target',
			 type='str',
			 choices=['target','observed','proposed','realtime']),
        module_name = dict(required=True, type='str'),
        attr_type= dict(required=False, type='dict'),
        attr_data = dict(required=True, type='dict'),
        operation = dict(required=False,
                     default='create',
                     type='str',
                     choices=['create', 'delete', 'set'])
    )

    module = AnsibleModule(argument_spec=argument_spec,
                           supports_check_mode=False)
    try:
        # TODO:: Need to convert as variable from module
        run(module)
    except Exception as e:
        RESULT["failed"] = True
        RESULT["msg"] = str(type(e).__name__) + ": " + str(e)

    module.exit_json(**RESULT)

if __name__ == '__main__':
    main()
	
