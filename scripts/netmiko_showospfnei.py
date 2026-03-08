from netmiko import ConnectHandler

routers = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.255.20",
        "username": "cisco",
        "password": "cisco",
    },
    {
        "device_type": "cisco_ios",
        "host": "192.168.255.21",
        "username": "cisco",
        "password": "cisco",
    }
]

for device in routers:
    print(f"\n{'='*25} Connecting to {device['host']} {'='*25}")
    try:
        with ConnectHandler(**device) as net_connect:
            output = net_connect.send_command("show ip ospf neighbor")
            
            if not output.strip():
                print("No OSPF neighbors found.")
            else:
                print(output)
                
    except Exception as e:
        print(f"Failed to connect: {e}")
