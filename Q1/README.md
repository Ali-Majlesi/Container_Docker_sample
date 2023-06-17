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
