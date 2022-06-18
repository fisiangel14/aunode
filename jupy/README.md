# A1G JupyterHub Docker
Implementation multi-user environment for Jupyter Notebooks. 

Documentation on [Confluence](https://tasktrack.telekom.at/confluence/pages/viewpage.action?pageId=291751826).

## Install Docker

1. Docker is part of RHEL repository so installatation comes down to exeuting (as *root*):
```bash
yum install docker
```

2. In order to be able to manage containers with a "normal" user (e.g. *iris*) you need to create group named *docker* and add requred users in the group:
```bash
sudo groupadd docker
usermod -aG docker iris
```

3. Configure Docker default data directory. Since this directory will contain all docker data as images, volumes and containers it should be located in a directory with enough storage. It will be accessible only by root. 

> Create the file:
```bash
vi /etc/docker/daemon.json
```

> with following content:
```json
{
    "graph": "/opt/cra/docker"
}
```

4. Docker should have access to Dockerhub in order to download the standard images, therefore (if needed) http/https proxy should be configured. Following is example for A1 Hub, change analog for other countries if necessary:

> create following dir and file:
```
mkdir -p /etc/systemd/system/docker.service.d
vi /etc/systemd/system/docker.service.d/https-proxy.conf
```

> add following content:
```text
[Service]
Environment="HTTPS_PROXY=http://proxy.austria.local:8080/"
```

5. Enable docker service and start it as such:
```bash
systemctl enable docker.service
systemctl start docker.service
```

6. Install **docker-compose** - a tool for defining and running multi-container Docker applications (this is exactly such case):
```bash
# set proxies for the current session if needed. For A1 Hub:
export HTTP_PROXY=http://proxy.austria.local:8080
export HTTPS_PROXY=https://proxy.austria.local:8080

# download docker-compose
curl -L "https://github.com/docker/compose/releases/download/1.23.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# set execute flag
chmod +x /usr/local/bin/docker-compose

# test
docker-compose --version
```

## Build Docker images from included files
```bash
# clone this repository e.g. in directory /opt/cra
cd /opt/cra
git clone https://tasktrack.telekom.at/bitbucket/scm/tagra/a1g-jupyterhub-docker.git

# go to directory git just created 
cd /opt/cra/a1g-jupyterhub-docker

# build the Docker containers defined in the 'docker-compose.yml' file
docker-compose build --build-arg https_proxy=https://proxy.austria.local:8080 --build-arg http_proxy=http://proxy.austria.local:8080
```

## Start JupyterHub container
```bash
# Start JupyterHub container
docker-compose up -d

# Stop container
docker-compose down
```

## Monitor Docker containers
```bash
# Show running containers
docker ps

# Show RAM and CPU consumption 
docker stats

# Show container logs
docker logs jupyterhub
```
