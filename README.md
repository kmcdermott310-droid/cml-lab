CCNP Encor Automation Training/Coding

This is all done in CML, even the ubuntu automation machine.

Reference the notes folder for setting up the ubuntu and routers. 
Note: my nat network for the cml external connector was 192.168.255.0/24 so I made my machine static .10 (and routers 20/21).
That is done in the #cloud config bootstrap  seen in CML by clicking on the node, going to config. 

Seen in the diagram, I made the above part a vrf for mgmt, which can reach internet.
Below is just play area in global routing context.

This repository contains:
-ansible playbooks
-netconf
-restconf
-Catalyst Center / JWT json web token
-Netmiko
-and more

Feel free to play around or just copy code from here.

In the readme's everything has steps an explanations.
AI wrote alot of this I used it to teach me.

<img width="511" height="815" alt="image" src="https://github.com/user-attachments/assets/49b8fd03-9a13-4c0e-bd32-f3dcb9332259" />
