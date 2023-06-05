# Creating hosts and router
ip netns add node1
ip netns add node2
ip netns add node3
ip netns add node4
ip netns add router

# Creating bridges
ip link add br1 type bridge
ip link add br2 type bridge

# Creating links
ip link add veth-1 type veth peer name eth0 netns node1
ip link add veth-2 type veth peer name eth0 netns node2
ip link add veth-3 type veth peer name eth0 netns node3
ip link add veth-4 type veth peer name eth0 netns node4
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
ip link set veth-br1 up

# Setting links in other nameapces up
ip netns exec node1 ip link set dev lo up
ip netns exec node2 ip link set dev lo up
ip netns exec node3 ip link set dev lo up
ip netns exec node4 ip link set dev lo up
ip netns exec router ip link set dev lo up

ip netns exec node1 ip link set dev eth0 up
ip netns exec node2 ip link set dev eth0 up
ip netns exec node3 ip link set dev eth0 up
ip netns exec node4 ip link set dev eth0 up
ip netns exec router ip link set dev eth1 up
ip netns exec router ip link set dev eth2 up


# Assign ip to nodes
ip netns exec node1 ip address add 172.0.0.2/24 dev eth0
ip netns exec node2 ip address add 172.0.0.3/24 dev eth0
ip netns exec node3 ip address add 10.0.0.2/24 dev eth0
ip netns exec node4 ip address add 10.0.0.3/24 dev eth0
ip netns exec router ip address add 172.0.0.1/24dev eth0
ip netns exec router ip address add 10.0.0.1/24 dev eth0

ip netns exec node1 ip route
