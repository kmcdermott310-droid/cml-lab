from netmiko import ConnectHandler

node = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.255.20",
        "username": "cisco",
        "password": "cisco",
    },

]

# --- Configuration Parameters (customize these) ---
VRF = "front-door"
INTERFACE = "Gi2"
DESCRIPTION = "Configured by Netmiko"
IP_ADDR = "10.0.0.1"
NETMASK = "255.255.255.0"

OSPF_PROCESS = "1"
OSPF_AREA = "0"

TUNNEL_INTERFACE = "Tunnel0"
TUNNEL_DESCRIPTION = "GRE over IPsec to peer"
TUNNEL_IP = "172.16.0.1"
TUNNEL_MASK = "255.255.255.0"
TUNNEL_SRC = INTERFACE

PEER_IP = "10.0.0.2"
PEER_NAME = "peer1"
PSK = "Cisco123!"

IKEV2_PROPOSAL = "IKEV2_PROP"
IKEV2_POLICY = "IKEV2_POL"
IKEV2_KEYRING = "IKEV2_KR"
IKEV2_PROFILE = "IKEV2_PROF"

IPSEC_TS = "IPSEC_TS"
IPSEC_PROFILE = "IPSEC_PROFILE"

for device in node:
    print(f"\n{'='*25} Connecting to {device['host']} {'='*25}")
    try:
        with ConnectHandler(**device) as net_connect:
            # Build a full configuration set: VRF, interface, IKEv2, IPsec, tunnel, OSPF
            config_commands = [
                # Create VRF using modern syntax and enable IPv4 address family
                f"vrf definition {VRF}",
                " address-family ipv4",
                " exit-address-family",

                # Physical interface in VRF
                f"interface {INTERFACE}",
                f"vrf forwarding {VRF}",
                f"description {DESCRIPTION}",
                f"ip address {IP_ADDR} {NETMASK}",
                f"ip ospf {OSPF_PROCESS} area {OSPF_AREA}",
                "no shutdown",

                # IKEv2 proposal and policy
                f"crypto ikev2 proposal {IKEV2_PROPOSAL}",
                "encryption aes-cbc-256",
                "integrity sha256",
                "group 14",
                f"crypto ikev2 policy {IKEV2_POLICY}",
                f"proposal {IKEV2_PROPOSAL}",

                # IKEv2 keyring and profile (PSK)
                f"crypto ikev2 keyring {IKEV2_KEYRING}",
                f"peer {PEER_NAME}",
                f"address {PEER_IP}",
                f"pre-shared-key local {PSK}",
                f"pre-shared-key remote {PSK}",

                f"crypto ikev2 profile {IKEV2_PROFILE}",
                f"match identity remote address {PEER_IP} 0.0.0.0",
                f"identity local address {IP_ADDR}",
                "authentication remote pre-share",
                "authentication local pre-share",
                f"keyring local {IKEV2_KEYRING}",

                # IPsec transform-set and profile
                f"crypto ipsec transform-set {IPSEC_TS} esp-aes 256 esp-sha256-hmac",
                "mode tunnel",
                f"crypto ipsec profile {IPSEC_PROFILE}",
                f"set transform-set {IPSEC_TS}",
                f"set ikev2-profile {IKEV2_PROFILE}",

                # Tunnel interface (GRE) attached to the VRF for lookup
                f"interface {TUNNEL_INTERFACE}",
                f"tunnel vrf {VRF}",
                f"description {TUNNEL_DESCRIPTION}",
                f"ip address {TUNNEL_IP} {TUNNEL_MASK}",
                f"tunnel source {TUNNEL_SRC}",
                f"tunnel destination {PEER_IP}",
                "tunnel mode gre ip",
                f"tunnel protection ipsec profile {IPSEC_PROFILE}",
                # OSPF on tunnel will use the global OSPF process (configured below)
                f"ip ospf {OSPF_PROCESS} area {OSPF_AREA}",
                "no shutdown",

                # Ensure global OSPF process exists (not VRF-scoped)
                f"router ospf {OSPF_PROCESS}",

                # Persist configuration
                "end",
                "write memory",
            ]

            print("Applying configuration:")
            for cmd in config_commands:
                print(f"  {cmd}")

            output = net_connect.send_config_set(config_commands)
            print(output)

    except Exception as e:
        print(f"Failed to connect: {e}")
