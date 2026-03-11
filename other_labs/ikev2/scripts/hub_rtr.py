from netmiko import ConnectHandler

node = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.255.20",
        "username": "cisco",
        "password": "cisco",
    },
]

# --- Core/Infrastructure Parameters ---
VRF = "front-door"
INTERFACE = "G0/1"
IP_ADDR = "10.0.0.1"
NETMASK = "255.255.255.0"
OSPF_PROCESS = "1"
PSK = "Cisco123!"

# --- Adjusted Tunnel & Area Mapping ---
# Spoke 1 -> Area 15 (Stub)
T1_NAME, T1_IP, T1_PEER, T1_AREA = "Tunnel15", "172.16.15.1", "10.0.0.2", "15"
# Spoke 2 -> Area 25 (Totally Stubby)
T2_NAME, T2_IP, T2_PEER, T2_AREA = "Tunnel25", "172.16.25.1", "10.0.0.3", "25"
# Spoke 3 -> Area 35 (NSSA)
T3_NAME, T3_IP, T3_PEER, T3_AREA = "Tunnel35", "172.16.35.1", "10.0.0.4", "35"

TUNNEL_MASK = "255.255.255.0"

for device in node:
    print(f"\n{'='*25} Connecting to {device['host']} {'='*25}")
    try:
        with ConnectHandler(**device) as net_connect:
            config_commands = [
                # 1. VRF & Physical Interface
                f"vrf definition {VRF}",
                " address-family ipv4",
                " exit-address-family",
                f"interface {INTERFACE}",
                f" vrf forwarding {VRF}",
                f" ip address {IP_ADDR} {NETMASK}",
                " no shutdown",

                # 2. Crypto Setup (Proposal, Policy, Keyring, Profile)
                "crypto ikev2 proposal IKEV2_PROP",
                " encryption aes-cbc-256",
                " integrity sha256",
                " group 14",
                "crypto ikev2 policy IKEV2_POL",
                f" match fvrf {VRF}",
                " proposal IKEV2_PROP",
                "crypto ikev2 keyring IKEV2_KR",
                f" peer peer1", f"  address {T1_PEER}", f"  pre-shared-key local {PSK}", f"  pre-shared-key remote {PSK}",
                f" peer peer2", f"  address {T2_PEER}", f"  pre-shared-key local {PSK}", f"  pre-shared-key remote {PSK}",
                f" peer peer3", f"  address {T3_PEER}", f"  pre-shared-key local {PSK}", f"  pre-shared-key remote {PSK}",
                "crypto ikev2 profile IKEV2_PROF",
                f" match fvrf {VRF}",
                f" match identity remote address {T1_PEER} 255.255.255.255",
                f" match identity remote address {T2_PEER} 255.255.255.255",
                f" match identity remote address {T3_PEER} 255.255.255.255",
                f" identity local address {IP_ADDR}",
                " authentication remote pre-share",
                " authentication local pre-share",
                " keyring local IKEV2_KR",

                # 3. IPsec
                "crypto ipsec transform-set IPSEC_TS esp-aes 256 esp-sha256-hmac",
                " mode tunnel",
                "crypto ipsec profile IPSEC_PROFILE",
                " set transform-set IPSEC_TS",
                " set ikev2-profile IKEV2_PROF",

                # 4. Tunnel Interfaces
                f"interface {T1_NAME}",
                f" tunnel vrf {VRF}", f" ip address {T1_IP} {TUNNEL_MASK}",
                f" tunnel source {INTERFACE}", f" tunnel destination {T1_PEER}",
                " tunnel protection ipsec profile IPSEC_PROFILE",
                f" ip ospf {OSPF_PROCESS} area {T1_AREA}",
                
                f"interface {T2_NAME}",
                f" tunnel vrf {VRF}", f" ip address {T2_IP} {TUNNEL_MASK}",
                f" tunnel source {INTERFACE}", f" tunnel destination {T2_PEER}",
                " tunnel protection ipsec profile IPSEC_PROFILE",
                f" ip ospf {OSPF_PROCESS} area {T2_AREA}",

                f"interface {T3_NAME}",
                f" tunnel vrf {VRF}", f" ip address {T3_IP} {TUNNEL_MASK}",
                f" tunnel source {INTERFACE}", f" tunnel destination {T3_PEER}",
                " tunnel protection ipsec profile IPSEC_PROFILE",
                f" ip ospf {OSPF_PROCESS} area {T3_AREA}",

                # 5. OSPF Process with Specific Area Types
                f"router ospf {OSPF_PROCESS}",
                # Area 15: Stub (Blocks External Type 5 LSAs)
                f" area {T1_AREA} stub",
                # Area 25: Totally Stubby (Blocks External and Inter-area LSAs)
                f" area {T2_AREA} stub no-summary",
                # Area 35: NSSA (Allows redistribution into the area but blocks Type 5s)
                f" area {T3_AREA} nssa",
                " default-information originate",
                "end",
                "write memory"
            ]

            print("Applying Hub Configuration with Multi-Type OSPF Areas...")
            output = net_connect.send_config_set(config_commands)
            print(output)

    except Exception as e:
        print(f"Error: {e}")
