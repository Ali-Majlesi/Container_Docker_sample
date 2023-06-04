ip netns add node1
ip netns add node2
ip netns add node3
ip netns add node4

ovs-vsctl add-br br1
ovs-vsctl add-br br2

ip link add veth-1 type veth peer name eth0 netns node1
ip link add veth-2 type veth peer name eth0 netns node2

ovs-vsctl add-port br1 veth-1
ovs-vsctl add-port br1 veth-2

ip link set veth-1 up
ip link set veth-2 up

ip netns exec node1 ip link set dev lo up
ip netns exec node2 ip link set dev lo up
ip netns exec node1 ip link set dev eth0 up
ip netns exec node2 ip link set dev eth0 up

ip netns exec node1 ip address add 172.0.0.2/24 dev eth0
ip netns exec node2 ip address add 172.0.0.3/24 dev eth0

ip netns exec node1 ip route

