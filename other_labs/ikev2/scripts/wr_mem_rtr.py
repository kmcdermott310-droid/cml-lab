from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoTimeoutException, NetmikoAuthenticationException

# List of last octets for your routers
nodes = ["20", "21", "22", "23"]

for last_octet in nodes:
    ip = f"192.168.255.{last_octet}"
    
    device = {
        "device_type": "cisco_ios",
        "host": ip,
        "username": "cisco",
        "password": "cisco",
        "secret": "cisco", # Added in case you are in enable mode
    }

    print(f"--- Connecting to {ip} ---")
    try:
        with ConnectHandler(**device) as net_connect:
            # Enter enable mode if necessary
            net_connect.enable()
            
            # Send the save command
            output = net_connect.send_command("write memory")
            print(f"Response from {ip}: {output.strip()}")
            
    except (NetmikoTimeoutException, NetmikoAuthenticationException) as e:
        print(f"Failed to save config on {ip}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred on {ip}: {e}")

print("\n--- Save operations complete ---")
