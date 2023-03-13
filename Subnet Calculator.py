# Subnet-Calculator
#Automation Subnet calculation

import ipaddress

# ask for network address in CIDR notation
network_str = input("Enter the network address in CIDR notation (e.g. 192.168.1.0/24): ")

# parse the network address
network = ipaddress.ip_network(network_str)

# print some information about the network
print(f"Network address: {network.network_address}")
print(f"Netmask: {network.netmask}")
print(f"Broadcast address: {network.broadcast_address}")
print(f"Number of hosts per subnet: {network.num_addresses - 2}")

# calculate the maximum number of subnets that can be created
max_subnets = 2 ** (network.max_prefixlen - network.prefixlen)

# ask for the number of subnets required
num_subnets = int(input(f"Enter the number of subnets required (max: {max_subnets}): "))

# validate the user input
if num_subnets > max_subnets:
    print(f"Error: Maximum number of subnets that can be created from this network is {max_subnets}.")
else:
    # calculate the prefix length of the subnet mask required for the number of subnets
    prefixlen_diff = network.max_prefixlen - network.prefixlen
    subnet_prefixlen = network.prefixlen + prefixlen_diff.bit_length()

    # create a list of subnets with the desired prefix length
    subnets = list(network.subnets(new_prefix=subnet_prefixlen))

    # calculate the size of each subnet
    subnet_size = network.num_addresses // num_subnets

    # perform subnetting and print the results
    for i in range(num_subnets - 1):
        subnet = subnets[i]
        print(f"Subnet {i+1}: {subnet.network_address}/{subnet_prefixlen}")
        print(f"First usable address: {subnet.network_address + 1}")
        print(f"Last usable address: {subnet.broadcast_address - 1}")
        print(f"Broadcast address: {subnet.broadcast_address}")
        print(f"Number of hosts: {subnet_size - 2}")

    # handle any remaining addresses in the last subnet
    last_subnet = subnets[num_subnets - 1]
    print(f"Subnet {num_subnets}: {last_subnet.network_address}/{subnet_prefixlen}")
    print(f"First usable address: {last_subnet.network_address + 1}")
    print(f"Last usable address: {last_subnet.network_address + subnet_size - 2}")
    print(f"Broadcast address: {last_subnet.network_address + subnet_size - 1}")
    print(f"Number of hosts: {subnet_size - 2}")

