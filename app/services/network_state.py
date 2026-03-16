import ipaddress

class NetworkState:
    def __init__(self, subnet_mask: str = "255.255.255.0", base_ip: str = "10.0.0.0"):
        self.subnet_mask = subnet_mask
        self.base_ip = base_ip
        self.total_ips, self.pool_range = self.calculate_pool(subnet_mask)

    def calculate_pool(self, subnet_mask: str):
        try:
            net = ipaddress.IPv4Network(f"{self.base_ip}/{subnet_mask}", strict=False)
            hosts = list(net.hosts())
            return len(hosts), f"{hosts[0]} - {hosts[-1]}"
        except Exception:
            return 254, f"{self.base_ip}.1 - {self.base_ip}.254"

    def update_subnet(self, subnet_mask: str):
        self.subnet_mask = subnet_mask
        self.total_ips, self.pool_range = self.calculate_pool(subnet_mask)
        
network_state = NetworkState()