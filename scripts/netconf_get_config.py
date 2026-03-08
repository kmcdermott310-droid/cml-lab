from ncclient import manager
import xml.dom.minidom

#1 Define the device connection details
router = {
    "host": "192.168.255.20", # Use your Sandbox or CML Router IP
    "port": 830,
    "username": "cisco",
    "password": "cisco",
    "hostkey_verify": False
}

#2 Open the NETCONF connection
with manager.connect(**router) as m:
    #3 Request the running configuration
    netconf_response = m.get_config(source='running')
    
    #4 Convert the raw XML to a "pretty" readable format
    xml_data = xml.dom.minidom.parseString(netconf_response.xml)
    print(xml_data.toprettyxml(indent="  "))
