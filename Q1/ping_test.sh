#!/bin/bash

# Check if both node names are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <source_node> <destination_node>"
    exit 1
fi

source_node=$1
destination_node=$2

# Define the IP addresses for each node
declare -A nodes=(
    ["node1"]="172.0.0.2"
    ["node2"]="172.0.0.3"
    ["node3"]="10.10.0.2"
    ["node4"]="10.10.0.3"
)

# Define the router IP addresses for each network
declare -A router_ips=(
    ["172.0.0.2"]="172.0.0.1"
	["172.0.0.3"]="172.0.0.1"
    ["10.10.0.2"]="10.10.0.1"
	["172.0.0.3"]="172.0.0.1"
)

# Get the IP addresses of the source and destination nodes
source_ip=${nodes[$source_node]}
if [ "$destination_node" == "router" ]; then
    destination_ip=${router_ips[$source_ip]}
else
    destination_ip=${nodes[$destination_node]}
fi

# Start pinging the destination node from the source node
ip netns exec $source_node ping $destination_ip -c 4
