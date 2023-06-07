import os
import sys
import subprocess

def create_container(hostname):
    # Create namespaces directory if it doesn't exist
    namespaces_dir = "./namespace"
    os.makedirs(namespaces_dir, exist_ok=True)

    # Find the next available container ID
    container_id = 1
    while os.path.exists(os.path.join(namespaces_dir, str(container_id))):
        container_id += 1

    # Create container's namespace folder
    container_dir = os.path.join(namespaces_dir, str(container_id))
    os.makedirs(container_dir)

    # Create net, mnt, and uts files inside container's folder
    net_file = os.path.join(container_dir, "net")
    mnt_file = os.path.join(container_dir, "mnt")
    uts_file = os.path.join(container_dir, "uts")
    open(net_file, 'a').close()
    open(mnt_file, 'a').close()
    open(uts_file, 'a').close()

    # Mount namespaces directory and make it private
    subprocess.run(['mount', '--bind', namespaces_dir, namespaces_dir], check=True)
    subprocess.run(['mount', '--make-private', namespaces_dir], check=True)

    # Enter the namespaces using unshare
    unshare_command = ['unshare -pfr', f'--net={net_file}', f'--uts={uts_file}', f'--mount={mnt_file}', f'hostname {hostname}']
    subprocess.run(unshare_command, check=True)

    # Change hostname within the container
    subprocess.run(['hostname', hostname], check=True)
    
    # TODO : Correct lines after this line
    print("Container successfully created with ID:", container_id)
    # Mount the Ubuntu 20.04 root filesystem
    rootfs_dir = '/path/to/ubuntu/rootfs'  # Replace with the actual path to the Ubuntu root filesystem
    subprocess.run(['mount', '--bind', rootfs_dir, '/'], check=True)

    # Change root to the new root filesystem
    os.chdir('/')
    os.chroot('.')

    # Start bash as the init process
    subprocess.run(['/bin/bash'], check=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python container_runtime.py <hostname>')
        sys.exit(1)

    hostname = sys.argv[1]
    create_container(hostname)
