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
  && apt install -y --no-install-recommends curl python3-all python3-venv \
  && rm -rf /var/lib/apt/lists/*

# Add starbound user
RUN useradd --create-home --home $HOME starbound

# Copy scripts and python project files
COPY --chown=${USER}:${USER} pyproject.toml pdm.lock $HOME
COPY --chown=${USER}:${USER} container-scripts $HOME/container-scripts

# Copy steam stuff to user folder
RUN cp -r /root/.steam $HOME/.steam
RUN chown -R ${USER}:${USER} $HOME/.steam

# Run as starbound user
USER starbound

# Go to home directory
WORKDIR $HOME

# Install pdm
RUN curl -sSL https://pdm-project.org/install-pdm.py | python3 -
ENV PATH="$HOME/.local/bin:$PATH"

# disable pdm update check
ENV PDM_CHECK_UPDATE=false

# Setup python environment
RUN pdm install --check --prod --no-editable
ENV PATH="$HOME/.venv/bin:$PATH"

# Set working directory to scripts folder
WORKDIR $HOME/container-scripts

# Ports used by the server
EXPOSE 21025/tcp 21025/udp
# Optional: RCON
EXPOSE 21026/tcp

ENTRYPOINT [ "python3", "main.py" ]
