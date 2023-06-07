import os
import sys
import subprocess


        
def download_ubuntu_root(ubuntu_root_dir):
    # Run debootstrap command to download Ubuntu 20.04 root filesystem
    subprocess.run(['debootstrap', '--variant=minbase', 'focal', ubuntu_root_dir, 'http://archive.ubuntu.com/ubuntu/'])

    print("Ubuntu 20.04 root filesystem downloaded successfully.")

def list_containers():
    # Specify the root directory where the containers are stored
    root_dir = "./root"

    # Get a list of directory names in the root directory
    container_dirs = os.listdir(root_dir)

    # Print the directory names
    for container_dir in container_dirs:
        print(container_dir)

def connect_to_container(container_id):
    namespaces_dir = f"./namespace/{container_id}"
    
    # Create net, mnt, and uts files inside container's folder
    net_file = os.path.join(container_dir, "net")
    mnt_file = os.path.join(container_dir, "mnt")
    uts_file = os.path.join(container_dir, "uts")
    usr_file = os.path.join(container_dir, "usr")
    
    root_dir = f'./root/{container_id}'
    
    nsenter_command = f'nsenter --net={net_file} --uts={uts_file} --mount={mnt_file} --user={usr} unshare pf chroot {root_dir} bash
    
def create_container(hostname):
    ubuntu_root_dir = "./ubuntu_root"
    # Check if the 'ubuntu_root' directory already exists
    if not os.path.exists(ubuntu_root_dir):
        # If it doesn't exist, download the Ubuntu root filesystem
        download_ubuntu_root(ubuntu_root_dir)
    else:
        print("Ubuntu 20.04 root filesystem already exists.")
    
    # Find the next available container ID
    container_id = 1
    while os.path.exists(os.path.join(namespaces_dir, str(container_id))):
        container_id += 1
        
    # Create namespaces directory if it doesn't exist
    namespaces_dir = f"./namespace/{container_id}"
    os.makedirs(namespaces_dir, exist_ok=True)
    
    
    
    root_dir = f'./root/{container_id}'
    os.makedirs(root_dir, exist_ok=True)
    subprocess.run('cp -r {ubuntu_root_dir}/* {root_dir}/*')
    
    

    # Create container's namespace folder
    container_dir = os.path.join(namespaces_dir, str(container_id))
    os.makedirs(container_dir)

    # Create net, mnt, and uts files inside container's folder
    net_file = os.path.join(container_dir, "net")
    mnt_file = os.path.join(container_dir, "mnt")
    uts_file = os.path.join(container_dir, "uts")
    usr_file = os.path.join(container_dir, "usr")
    open(net_file, 'a').close()
    open(mnt_file, 'a').close()
    open(uts_file, 'a').close()
    open(usr_file, 'a').close()


    # Mount namespaces directory and make it private
    subprocess.run(['mount', '--bind', namespaces_dir, namespaces_dir], check=True)
    subprocess.run(['mount', '--make-private', namespaces_dir], check=True)

    # Enter the namespaces using unshare
    unshare_command = ['unshare -pfr', f'--net={net_file}', f'--uts={uts_file}', f'--mount={mnt_file}', f'hostname {hostname}']
    subprocess.run(unshare_command, check=True)
    print("Container successfully created with ID:", container_id)
    
    # Enter to the created namespaces
    nsenter_command = f'nsenter --net={net_file} --uts={uts_file} --mount={mnt_file} --user={usr} unshare pf chroot {root_dir} bash -c "mount -t proc proc /proc && bash"'
    subprocess.run(nsenter_command, check=True)

def delete_container(container_id):
    pass
    
if __name__ == '__main__':
    usage_str = 'Usage: python my-cli.py (create <hostname>|list|connect <container_id>|del <container id>)'
    if len(sys.argv) < 2:
        print(usage_str)
        sys.exit(1)
    else:
        command = sys.argv[1]
        if command == 'create':
            if len(sys.argv < 3):
                print('Usage: python my-cli.py create <hostname>')
                sys.exit(1)
            else:
                hostname = sys.argv[2]
                create_container(hostname)
                
        elif command == 'list':
            if len(sys.argv > 3):
                print('Usage: python my-cli.py list')
                sys.exit(1)
            else:
                list_containers()
                
        elif command == 'connnect':
            if len(sys.argv < 3):
                print('Usage: python my-cli.py connect <container id>')
                sys.exit(1)
            else:
                container_id = sys.argv[2]
                connect_to_container(container_id)
                
        elif command == 'del':
            if len(sys.argv < 3):
                print('Usage: python my-cli.py del <container id>')
                sys.exit(1)
            else:
                container_id = sys.argv[2]
                delete_container(container_id)
        else:
            print(usage_str)
