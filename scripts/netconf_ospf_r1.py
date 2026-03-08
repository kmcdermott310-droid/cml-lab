from ncclient import manager

router = [{"host": "192.168.255.20", "user": "cisco", "password": "cisco"}]

#This structure uses the 'native' root but ensures the namespaces are exactly where Cisco expects them
#The first <config> line needed (xmlns="urn:ietf:params:xml:ns:netconf:base:1.0") from the top output of the netconf_get_config.py script
ospf_config = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
<router>
        <router-ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
          <ospf>
            <process-id>
              <id>1</id>
              <network>
                <ip>10.10.10.0</ip>
                <wildcard>0.0.0.255</wildcard>
                <area>0</area>
              </network>
            </process-id>
          </ospf>
        </router-ospf>
        <ospf xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf">
          <id>1</id>
          <auto-cost>
            <reference-bandwidth>100</reference-bandwidth>
          </auto-cost>
          <timers>
            <throttle>
              <spf>
                <delay>50</delay>
                <min-delay>200</min-delay>
                <max-delay>5000</max-delay>
              </spf>
            </throttle>
          </timers>
          <compatible>
            <rfc1583/>
          </compatible>
        </ospf>
</router>
</native>
</config>
"""

for device in router:
    try:
        with manager.connect(host=device["host"], 
                             port=830, 
                             username=device["user"], 
                             password=device["password"], 
                             hostkey_verify=False) as m:
            
            # The 'nc:config' wrapper is handled by the library, we just pass the inner XML
            m.edit_config(target='running', config=ospf_config)
            print(f"Success! OSPF Configured on {device['host']}")
            
    except Exception as e:
        print(f"Failed on {device['host']}: {e}")


