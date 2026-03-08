from netmiko import ConnectHandler

devices = ["192.168.255.20", "192.168.255.21"]

for ip in devices:
    # Define the device connection parameters
    cisco_device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": "cisco",
        "password": "cisco",
    }

    try:
        # Establish SSH connection
        with ConnectHandler(**cisco_device) as net_connect:
            # Netmiko has a built-in function that sends 'copy running-config startup-config'
            net_connect.save_config()
            
        print(f"Saved: {ip}")

    except Exception as e:
        print(f"Error on {ip}: {e}")
