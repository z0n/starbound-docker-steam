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

# Set working directory
WORKDIR $HOME

# Copy starbound update/download scripts
COPY --chown=${USER}:${USER} ./container-scripts/*.sh ./
RUN chmod +x ./*.sh

# Copy steam stuff to user folder
RUN cp -r /root/.steam /home/starbound/.steam
RUN chown -R starbound:starbound /home/starbound/.steam

# Run as starbound user
USER starbound

# Ports used by the server
EXPOSE 21025/tcp 21025/udp
# Optional: RCON
EXPOSE 21026/tcp


ENTRYPOINT [ "./entrypoint.sh"]
