# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Configuration file for JupyterHub
import os
c = get_config()

# JWT Authentication - do not show any login page
# Authentication through A1G Dash token
c.Authenticator.admin_users = {'kostadin.taneski'}
c.JupyterHub.authenticator_class = 'jwtauthenticator.jwtauthenticator.JSONWebTokenAuthenticator'
c.JSONWebTokenAuthenticator.secret = 'FCquG07Wxi9qJADP6f90aHBJHtCZfSbUTdB8EwMV'
c.JSONWebTokenAuthenticator.username_claim_field = 'id' 
c.JSONWebTokenAuthenticator.param_name = 'jwt'

# Do not show buttons
c.Authenticator.auto_login = True
c.JupyterHub.redirect_to_server = True
# c.JupyterHub.data_files_path = '/usr/local/share/jupyterhub/'

# Spawn single-user servers as Docker containers
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'

# Spawn containers from this image
c.DockerSpawner.image = os.environ['DOCKER_NOTEBOOK_IMAGE']

# JupyterHub requires a single-user instance of the Notebook server, so we
# default to using the `start-singleuser.sh` script included in the
# jupyter/docker-stacks *-notebook images as the Docker run command when
# spawning containers.  Optionally, you can override the Docker run command
# using the DOCKER_SPAWN_CMD environment variable.
spawn_cmd = os.environ.get('DOCKER_SPAWN_CMD', "start-singleuser.sh")
c.DockerSpawner.extra_create_kwargs.update({ 'command': spawn_cmd })

# Connect containers to this Docker network
network_name = os.environ['DOCKER_NETWORK_NAME']
c.DockerSpawner.use_internal_ip = True
c.DockerSpawner.network_name = network_name

# Pass the network name as argument to spawned containers
c.DockerSpawner.extra_host_config = { 'network_mode': network_name }

# Explicitly set notebook directory because we'll be mounting a host volume to
# it.  Most jupyter/docker-stacks *-notebook images run the Notebook server as
# user `jovyan`, and set the notebook directory to `/home/jovyan/work`.
# We follow the same convention.
notebook_dir = os.environ.get('DOCKER_NOTEBOOK_DIR') or '/home/jovyan/work'
c.DockerSpawner.notebook_dir = notebook_dir

# Mount the real user's Docker volume on the host to the notebook user's
# notebook directory in the container
c.DockerSpawner.volumes = { 
	'jupyterhub-user-{username}': notebook_dir,
	'/dash/a1g-jupyterhub-docker/shared': '/home/jovyan/shared'
}

# Remove containers once they are stopped
c.DockerSpawner.remove_containers = True

# For debugging arguments passed to spawned containers
c.DockerSpawner.debug = True

# User containers will access hub by container name on the Docker network
c.JupyterHub.hub_ip = os.environ.get('DOCKER_MACHINE_NAME', 'jupyterhub')
c.JupyterHub.hub_port = 8080

# Shutdown user server on logout
# can create issues with container accessed from multiple browsers
# c.JupyterHub.shutdown_on_logout = True

# Shutdown the server after no activity for 2 hours
c.NotebookApp.shutdown_no_activity_timeout = 2 * 60 * 60

# Shutdown kernels after no activity for 1 hour
c.MappingKernelManager.cull_idle_timeout = 60 * 60

# Check for idle kernels every 5 minutes
c.MappingKernelManager.cull_interval = 5 * 60

# User server resources
c.Spawner.cpu_limit = 4
c.Spawner.mem_limit = '10G'

## Services
c.JupyterHub.services = [
    {
        'name': 'cull_idle',
        'admin': True,
        'command': 'python /srv/jupyterhub/cull_idle_servers.py --timeout=3600'.split(),
    },
]
