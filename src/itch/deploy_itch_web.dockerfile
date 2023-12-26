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
    && unzip default -d ${BUTLER_HOME} \
    && export PATH="$BUTLER_HOME:$PATH" \
    && butler -v

# Setup exporter
RUN mkdir -p /opt/exporter/
COPY exporter.sh /opt/exporter/exporter.sh
RUN alias exporter="bash /opt/exporter/exporter.sh" && exporter -v

CMD $EXPORT_SCRIPT