FROM jupyterhub/jupyterhub:1.0.0

COPY jupyterhub_config.py .

# COPY cull_idle_servers.py .
RUN wget -q https://raw.githubusercontent.com/jupyterhub/jupyterhub/1.0.0/examples/cull-idle/cull_idle_servers.py

RUN pip install --no-cache-dir \
    dockerspawner==0.10.0 \
    jupyterhub-jwtauthenticator