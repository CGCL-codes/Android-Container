## backend

The backend service program module is used to implement cross-architecture migration of containers. Migrate the container from the ubuntu operating system to the Android operating system, and the migrated container will have the state when the container was migrated.

#### how to use

First need to install related dependencies

```shell
sudo apt-get install python3
sudo apt-get install python3-pip
pip3 install flask
pip3 install docker
```

Modify the IP in backend.py according to your own IP address, and then directly execute the terminal:

```shell
python3 backend.py
```

