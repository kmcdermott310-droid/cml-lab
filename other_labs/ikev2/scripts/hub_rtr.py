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

# Downlink interfaces (Non-VRF)
CORE_IF_1, CORE_IP_1 = "G0/2", "100.100.100.6"
CORE_IF_2, CORE_IP_2 = "G0/3", "100.100.100.10"
CORE_MASK = "255.255.255.252"

# --- Tunnel & Area Mapping ---
# Tunnel 1 -> Area 20
T1_NAME, T1_IP, T1_PEER, T1_AREA = "Tunnel10", "172.16.10.1", "10.0.0.2", "20"
# Tunnel 2 -> Area 30
T2_NAME, T2_IP, T2_PEER, T2_AREA = "Tunnel20", "172.16.20.1", "10.0.0.3", "30"
# Tunnel 3 -> Area 40
T3_NAME, T3_IP, T3_PEER, T3_AREA = "Tunnel30", "172.16.30.1", "10.0.0.4", "40"

TUNNEL_MASK = "255.255.255.0"

for device in node:
    print(f"\n{'='*25} Connecting to {device['host']} {'='*25}")
    try:
        with ConnectHandler(**device) as net_connect:
            config_commands = [
                # 1. Non-VRF Physical Core Links
                f"interface {CORE_IF_1}",
                f" description Downlink-Core-1",
                f" ip address {CORE_IP_1} {CORE_MASK}",
                f" ip ospf {OSPF_PROCESS} area 0",
                " no shutdown",

                f"interface {CORE_IF_2}",
                f" description Downlink-Core-2",
                f" ip address {CORE_IP_2} {CORE_MASK}",
                f" ip ospf {OSPF_PROCESS} area 0",
                " no shutdown",

                # 2. VRF Setup
                f"vrf definition {VRF}",
                " address-family ipv4",
                " exit-address-family",
                f"interface {INTERFACE}",
                f" vrf forwarding {VRF}",
                f" ip address {IP_ADDR} {NETMASK}",
                " no shutdown",

                # 3. IKEv2 Proposal & Policy
                "crypto ikev2 proposal IKEV2_PROP",
                " encryption aes-cbc-256",
                " integrity sha256",
                " group 14",
                "crypto ikev2 policy IKEV2_POL",
                f" match fvrf {VRF}",
                " proposal IKEV2_PROP",

                # 4. IKEv2 Keyring with Symmetrical Keys
                "crypto ikev2 keyring IKEV2_KR",
                f" peer peer1", 
                f"  address {T1_PEER}", 
                f"  pre-shared-key local {PSK}",
                f"  pre-shared-key remote {PSK}",
                f" peer peer2", 
                f"  address {T2_PEER}", 
                f"  pre-shared-key local {PSK}",
                f"  pre-shared-key remote {PSK}",
                f" peer peer3", 
                f"  address {T3_PEER}", 
                f"  pre-shared-key local {PSK}",
                f"  pre-shared-key remote {PSK}",

                # 5. IKEv2 Profile
                "crypto ikev2 profile IKEV2_PROF",
                f" match fvrf {VRF}",
                f" match identity remote address {T1_PEER} 255.255.255.255",
                f" match identity remote address {T2_PEER} 255.255.255.255",
                f" match identity remote address {T3_PEER} 255.255.255.255",
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

                # 7. Tunnels
                f"interface {T1_NAME}",
                f" tunnel vrf {VRF}",
                f" ip address {T1_IP} {TUNNEL_MASK}",
                f" tunnel source {INTERFACE}",
                f" tunnel destination {T1_PEER}",
                " tunnel mode gre ip",
                " tunnel protection ipsec profile IPSEC_PROFILE",
                f" ip ospf {OSPF_PROCESS} area {T1_AREA}",

                f"interface {T2_NAME}",
                f" tunnel vrf {VRF}",
                f" ip address {T2_IP} {TUNNEL_MASK}",
                f" tunnel source {INTERFACE}",
                f" tunnel destination {T2_PEER}",
                " tunnel mode gre ip",
                " tunnel protection ipsec profile IPSEC_PROFILE",
                f" ip ospf {OSPF_PROCESS} area {T2_AREA}",

                f"interface {T3_NAME}",
                f" tunnel vrf {VRF}",
                f" ip address {T3_IP} {TUNNEL_MASK}",
                f" tunnel source {INTERFACE}",
                f" tunnel destination {T3_PEER}",
                " tunnel mode gre ip",
                " tunnel protection ipsec profile IPSEC_PROFILE",
                f" ip ospf {OSPF_PROCESS} area {T3_AREA}",
                
                "router ospf 1",
                " default-information originate",
                "end",
                "write memory"
            ]

            print(f"Pushing configuration to {device['host']}...")
            output = net_connect.send_config_set(config_commands)
            print(output)

    except Exception as e:
        print(f"Error: {e}")
