from netmiko import ConnectHandler

node = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.255.22",
        "username": "cisco",
        "password": "cisco",
    },
]

# --- Adjusted Configuration Parameters for Spoke 2 ---
VRF = "front-door"
INTERFACE = "G0/1"
IP_ADDR = "10.0.0.3"
NETMASK = "255.255.255.0"

OSPF_PROCESS = "1"
OSPF_AREA = "25"          # Area 25
OSPF_AREA_MODE = "stub"   # Spoke uses 'stub', Hub uses 'stub no-summary'

TUNNEL_INTERFACE = "Tunnel25"
TUNNEL_IP = "172.16.25.2" # Matches Hub Tunnel25 Subnet (.25.1 is Hub)
TUNNEL_MASK = "255.255.255.0"

PEER_IP = "10.0.0.1"      # Hub physical IP
PSK = "Cisco123!"

for device in node:
    print(f"\n{'='*25} Connecting to {device['host']} {'='*25}")
    try:
        with ConnectHandler(**device) as net_connect:
            config_commands = [
                # 1. VRF Setup
                f"vrf definition {VRF}",
                " address-family ipv4",
                " exit-address-family",

                # 2. Physical interface in VRF
                f"interface {INTERFACE}",
                f" vrf forwarding {VRF}",
                f" ip address {IP_ADDR} {NETMASK}",
                " no shutdown",

                # 3. IKEv2 Proposal and Policy
                "crypto ikev2 proposal IKEV2_PROP",
                " encryption aes-cbc-256",
                " integrity sha256",
                " group 14",
                "crypto ikev2 policy IKEV2_POL",
                f" match fvrf {VRF}",
                " proposal IKEV2_PROP",

                # 4. IKEv2 Keyring
                "crypto ikev2 keyring IKEV2_KR",
                " peer hub",
                f"  address {PEER_IP}",
                f"  pre-shared-key local {PSK}",
                f"  pre-shared-key remote {PSK}",

                # 5. IKEv2 Profile
                "crypto ikev2 profile IKEV2_PROF",
                f" match fvrf {VRF}",
                f" match identity remote address {PEER_IP} 255.255.255.255",
                f" identity local address {IP_ADDR}",
                " authentication remote pre-share",
                " authentication local pre-share",
                " keyring local IKEV2_KR",

                # 6. IPsec
                "crypto ipsec transform-set IPSEC_TS esp-aes 256 esp-sha256-hmac",
                " mode tunnel",
                "crypto ipsec profile IPSEC_PROFILE",
                " set transform-set IPSEC_TS",
                " set ikev2-profile IKEV2_PROF",

                # 7. Tunnel interface
                f"interface {TUNNEL_INTERFACE}",
                f" tunnel vrf {VRF}",
                f" ip address {TUNNEL_IP} {TUNNEL_MASK}",
                f" tunnel source {INTERFACE}",
                f" tunnel destination {PEER_IP}",
                " tunnel mode gre ip",
                " tunnel protection ipsec profile IPSEC_PROFILE",
                f" ip ospf {OSPF_PROCESS} area {OSPF_AREA}",
                " no shutdown",

                # 8. OSPF Process
                f"router ospf {OSPF_PROCESS}",
                f" area {OSPF_AREA} {OSPF_AREA_MODE}",
                
                "end",
                "write memory",
            ]

            print(f"Applying Spoke 2 config (Tunnel {TUNNEL_INTERFACE})...")
            output = net_connect.send_config_set(config_commands)
            print(output)

    except Exception as e:
        print(f"Failed to connect: {e}")
