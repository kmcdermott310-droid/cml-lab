CCNP Encor Automation Training/Coding

This was all done on the CML ubuntu VM. Arguablly annoying, no VS-Code, but you could set that up. This is really just to learn the basics so better to get hands on.

This git repository shows the inside of my only directory "cml-lab", there is all my work for:
-JWT -> CatC/DNAC (public dnac from cisco)
-Automate with ansible, python, netconf/restconf
-Other
-no SDWan because you need anyconnect now

Lab Replication Steps: CML 2.7.2 Automation Environment
1. Topology & Connectivity
CML Version: 2.7.2.
External Access: Add an External Connector node set to NAT mode.
Network Backbone: Connect the External Connector to an unmanaged switch, then connect your Ubuntu node and CSR1000v's (these have netconf capability).
Management VRF: Configure a dedicated Management VRF on the CSR1000v nodes to isolate automation traffic from data plane traffic. This will use the NAT network. See step 2.

2. Ubuntu Node Persistence
IP Addressing: Use "ip a" to identify the dynamically assigned interface address.
Static Reservation: Configure netplan on the Ubuntu node to ensure the IP address remains persistent across lab reboots. Mine was 192.168.255.10, after setting it permenantly, I made my routers .20 and .21.
Tip: Test connectivity by pinging 8.8.8.8 to verify the External Connector cloud is routing traffic correctly.
Use AI to help, and once setup make sure you start stop lab to verify its persitent before putting in alot of work.

4. Software Stack & Environment
Tooling: Update the local package index and install the core automation suite. Use AI for this. You need ansible, python3, and pip a bunch of network auto tools like requests, netmiko, ssh stuff, and ncclient. THIS TAKES A LONG TIME ON CML must be patient.


4. Node Configuration
The router configurations I put one example in the notes folder, this is just an barebones startup to make it work. 

All scripts have read me's

<img width="511" height="815" alt="image" src="https://github.com/user-attachments/assets/49b8fd03-9a13-4c0e-bd32-f3dcb9332259" />
