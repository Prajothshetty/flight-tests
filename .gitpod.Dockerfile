# .gitpod.Dockerfile
FROM gitpod/workspace-full

USER root
RUN apt-get update && \
    apt-get install -y chromium-browser chromium-chromedriver && \
    apt-get clean

USER gitpod
