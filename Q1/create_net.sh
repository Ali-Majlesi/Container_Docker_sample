# Creating hosts and router
ip netns add node1
ip netns add node2
ip netns add node3
ip netns add node4
ip netns add router

# Creating bridges
ip link add br1 type bridge
ip link add br2 type bridge
ip link set br1 up
ip link set br2 up

# Creating links
ip link add veth-1 type veth peer name eth0-node1 netns node1
ip link add veth-2 type veth peer name eth0-node2 netns node2
ip link add veth-3 type veth peer name eth0-node3 netns node3
ip link add veth-4 type veth peer name eth0-node4 netns node4
ip link add veth-br1 type veth peer name eth1 netns router
ip link add veth-br2 type veth peer name eth2 netns router

# Attaching links to bridges
ip link set veth-1 master br1
ip link set veth-2 master br1
ip link set veth-br1 master br1
ip link set veth-3 master br2
ip link set veth-2 master br2
ip link set veth-br2 master br2

# Setting links in the root namespace up
ip link set veth-1 up
ip link set veth-2 up
ip link set veth-3 up
ip link set veth-4 up
ip link set veth-br1 up
ip link set veth-br2 up

# Setting links in other nameapces up
ip netns exec node1 ip link set dev lo up
ip netns exec node2 ip link set dev lo up
ip netns exec node3 ip link set dev lo up
ip netns exec node4 ip link set dev lo up
ip netns exec router ip link set dev lo up

ip netns exec node1 ip link set dev eth0-node1 up
ip netns exec node2 ip link set dev eth0-node2 up
ip netns exec node3 ip link set dev eth0-node3 up
ip netns exec node4 ip link set dev eth0-node4 up
ip netns exec router ip link set dev eth1 up
ip netns exec router ip link set dev eth2 up


# Assign ip to nodes
ip netns exec node1 ip address add 172.0.0.2/24 dev eth0-node1
ip netns exec node2 ip address add 172.0.0.3/24 dev eth0-node2
ip netns exec node3 ip address add 10.10.0.2/24 dev eth0-node3
ip netns exec node4 ip address add 10.10.0.3/24 dev eth0-node4
ip netns exec router ip address add 172.0.0.1/24 dev eth1
ip netns exec router ip address add 10.10.0.1/24 dev eth2

# Add default gateway
ip netns exec node1 ip route add default via 172.0.0.1
ip netns exec node2 ip route add default via 172.0.0.1
ip netns exec node3 ip route add default via 10.10.0.1
ip netns exec node4 ip route add default via 10.10.0.1

ip netns exec node1 ip route

