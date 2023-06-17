### How can packets routing be done without a router in a VM?

To route packets from one subnet (`br1`) to another subnet (`br2`) in the given Linux network topology, the following steps can be followed:

1. Create a link from `br1` to the root namespace and assign the IP address `172.0.0.1/24` to the link:
   - The link can be created using the following command:
     ```
     ip link add veth-br1 type veth peer name br1-eth
     ```
   - Assign the link to `br1` using the following command:
     ```
     ip link set br1 master veth-br1
     ```

2. Create a link from `br2` to the root namespace and assign the IP address `10.10.0.1/24` to the link:
   - The link can be created using the following command:
     ```
     ip link add veth-br1 type veth peer name br2-eth
     ```
   - Assign the link to `br2` using the following command:
     ```
     ip link set br2 master veth-br1
     ```

3. Add default gateways for each subnet in the root namespace:
   - For the `br1` subnet (`172.0.0.0/24`), add a default gateway using the following command:
     ```
     ip addr add 172.0.0.1/24 dev br1-eth
     ```

   - For the `br2` subnet (`10.10.0.0/24`), add a default gateway using the following command:
     ```
     ip addr add add 10.10.0.1/24 dev br2-eth
     ```

4. Enable IP forwarding by executing the following command:
	```
	sysctl -w net.ipv4.ip_forward=1
	```
By creating links from each bridge (`br1` and `br2`) to the root namespace and assigning the appropriate IP addresses (`172.0.0.1/24` and `10.10.0.1/24`), connectivity is established between the subnets. Additionally, default gateways are added for each subnet, and IP forwarding is enabled, allowing packets to be routed from one subnet to another within the given network topology.


### What if the namespaces are on different servers that can see each other in layer 2 

To route packets between two different VMs connected with a layer 2 connection, you can follow the steps below:

1. Assign an IP address to the bridge in VM1 (Bridge 1):
   - Use the following command to assign an IP address to `br1` in VM1:
     ```
     ip addr add 172.0.0.1/24 dev br1
     ```

2. Set the routing table of VM1 to route packets between the subnets:
   - Use the following commands to configure the routing table in VM1:
     ```
     ip route add 172.0.0.0/24 dev br1
     ip route add 10.10.0.0/24 dev sw-ext-eth
     ```

3. Set the default gateway for each node in VM1 to the IP address of Bridge 1:
   - In each node's network namespace in VM1, use the following command to set the default gateway:
     ```
     ip netns exec node1 ip route add default via 172.0.0.1 dev eth0-node1
     ```

4. Repeat the above steps for VM2 (Bridge 2):
   - Assign an IP address to the bridge in VM2 (Bridge 2), for example:
     ```
     ip addr add 10.10.0.1/24 dev br2
     ```
   - Set the routing table of VM2 to route packets between the subnets, similar to Step 2 in VM1.
   - Set the default gateway for each node in VM2 to the IP address of Bridge 2, similar to Step 3 in VM1.

By following these steps, you can configure routing between the two bridges (br1 and br2) in different VMs. Assigning an IP address to each bridge, configuring the routing tables, and setting the default gateway for the nodes will enable the routing of packets between the subnets.
