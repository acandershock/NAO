import psutil

def get_ethernet_ipv4():
    for name, addrs in psutil.net_if_addrs().items():
        if name.startswith("Ethernet"):
            for snic in addrs:
                if snic.family.name == "AF_INET":
                    return name, snic.address
    return None, None

adapter, ip = get_ethernet_ipv4()

if ip:
    print(f"IPv4 of '{adapter}': {ip}")
else:
    print("No Ethernet IPv4 address found.")