# https://pdm-project.org/en/latest/usage/advanced/#use-pdm-in-a-multi-stage-dockerfile
ARG PYTHON_BASE=3.12-slim
# build stage
FROM python:$PYTHON_BASE AS builder

# install PDM
RUN pip install -U pdm

# disable update check
ENV PDM_CHECK_UPDATE=false

# copy files
COPY pyproject.toml pdm.lock /project/
COPY container-scripts/ /project/container-scripts/

# install dependencies and project into the local packages directory
WORKDIR /project
RUN pdm install --check --prod --no-editable


FROM docker.io/steamcmd/steamcmd:ubuntu-24

# Environment variables
ENV USER=starbound
ENV HOME=/home/$USER
ENV STARBOUND_INSTALL_DIR=$HOME/starbound
ENV STARBOUND_MODS_DIR=$STARBOUND_INSTALL_DIR/mods
ENV STARBOUND_APP_ID=211820

# Install dependencies
ARG DEBIAN_FRONTEND=noninteractive
RUN apt update -y \
  && apt install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

# Add starbound user
RUN useradd --create-home --home $HOME starbound

# retrieve packages from build stage
COPY --from=builder --chown=${USER}:${USER} /project/.venv/ ./.venv
ENV PATH="$HOME/.venv/bin:$PATH"

# Copy starbound update/download scripts
COPY --from=builder --chown=${USER}:${USER} /project/container-scripts/ ./

# Copy steam stuff to user folder
RUN cp -r /root/.steam /home/starbound/.steam
RUN chown -R ${USER}:${USER} /home/starbound/.steam

# Set working directory
WORKDIR $HOME/container-scripts

# Run as starbound user
USER starbound

# Ports used by the server
EXPOSE 21025/tcp 21025/udp
# Optional: RCON
EXPOSE 21026/tcp

ENTRYPOINT [ "python", "main.py" ]
