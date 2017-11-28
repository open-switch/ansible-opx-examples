# Ansible module and roles examples

This information contains sample Ansible playbook examples to understand how the Openswitch OPX Ansible module & roles works.

1. Install [Ansible](http://docs.ansible.com/ansible/intro_installation.html).

2. Clone this repository in the Control Machine.

3. Update the inventory.yaml to configure the device IP.

4. Update the corresponding host variables (use hosts_vars/opx.yaml to update the respective configurations).

5. Run the Ansible playbook using  ``ansible-playbook -i inventory.yaml datacenter.yaml``
