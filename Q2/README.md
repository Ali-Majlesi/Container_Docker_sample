## Container Runtime Documentation

### Introduction
The Container Runtime is a command-line interface (CLI) tool that allows you to create and manage containers. It provides a simplified version of Docker, enabling the creation of isolated environments with separate namespaces and filesystems. This documentation will guide you through the usage, and available features of the Container Runtime.

### Usage

#### Create a Container
To create a new container, use the following command:
```
python3 my-cli.py create <hostname>
```
Replace `<hostname>` with the desired hostname for the container. This command will create a new container with separate namespaces and a root filesystem based on the Ubuntu 20.04 image.

#### List Containers
To list the currently running containers, execute the following command:
```
python3 my-cli.py list
```

This command will display a list of the containers along with their respective container IDs.

#### Connect to a Container
To connect to a specific container and access its shell, use the following command:
```
python3 my-cli.py connect <container_id>
```
Replace `<container_id>` with the ID of the container you want to connect to. This command will open a shell session within the selected container.

