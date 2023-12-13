ARG ubuntuVersion

ARG godotVersion

ARG engineUrl
ARG engineArchiveName
ARG engineFileName

ARG templatesUrl
ARG templatesArchiveName

FROM ubuntu:$ubuntuVersion AS base

# Setup apt-get
RUN apt-get update

# Install basics
RUN apt-get install -y \
    wget \
    unzip

# Install Godot
RUN wget engineUrl \
    && unzip engineFileName \
    && rm engineArchiveName \
    && mv engineFileName godot \
    && mv godot /usr/bin/

# Install Godot deps
RUN apt-get install -y \
    libfontconfig

# Install Godot templates
ENV GODOT_TEMPLATES_DIR="/root/.local/share/godot/export_templates"
RUN wget templatesUrl \
    && mkdir -p ${GODOT_TEMPLATES_DIR} \
    && unzip templatesArchiveName \
    && rm templatesArchiveName \
    && mv templates ${GODOT_TEMPLATES_DIR} \
    && mv ${GODOT_TEMPLATES_DIR}/templates ${GODOT_TEMPLATES_DIR}/$godotVersion.stable

CMD godot
