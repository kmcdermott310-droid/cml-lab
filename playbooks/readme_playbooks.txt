This is the ansible playbooks folder, to run these here is what I have so far:

Note: Ansible playbooks are written in YAML. They are useful but you can also kind of just run python scripts with netconf/restconf functions or netmiko.

1. Show interfaces

ansible-playbook -i inventory/lab_devices.ini playbooks/show_interfaces.yml


2. This one is not a playbook but its an ansible function that will test connectiviy to all nodes. In this case just "routers" which is denoted in the ini file.

ansible routers -i inventory/lab_devices.ini -m ping
