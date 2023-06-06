import os
import sys
import subprocess

def create_container(hostname):
    # Create new namespaces
    namespaces = ['net', 'mnt', 'pid', 'uts']
    for ns in namespaces:
        subprocess.run(['unshare', '--' + ns], check=True)

    # Set hostname
    subprocess.run(['hostnamectl', 'set-hostname', hostname], check=True)

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
