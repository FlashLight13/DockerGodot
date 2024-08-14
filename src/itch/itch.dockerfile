ARG godotVersion
FROM flashlight13/godot:$godotVersion AS base

ARG butlerVersion
# Versions before 4.1 have problems importing a project via CLI
# https://github.com/godotengine/godot/issues/69511
ARG needsWorkaround=true

RUN apt-get install zip

# Install Itch.io butler
ENV BUTLER_HOME=/opt/butler
RUN wget https://broth.itch.ovh/butler/linux-amd64/${butlerVersion}/archive/default \
    && unzip default -d ${BUTLER_HOME}
ENV PATH="$PATH:$BUTLER_HOME"
RUN butler --version

# Setup exporter
RUN mkdir -p /opt/exporter/
COPY src/itch/exporter.sh /opt/exporter/exporter
ENV PATH="$PATH:/opt/exporter/"
RUN exporter --version

ENTRYPOINT ["exporter"]