FROM debian:12.4-slim AS base

ARG engineUrl
ARG engineArchiveName
ARG engineFileName

ARG templatesUrl
ARG templatesArchiveName
ARG templatesDirectory

# Setup apt-get and install basics
RUN apt-get update && apt-get install -y \
    wget \
    unzip

# Install Godot
RUN wget $engineUrl \
    && unzip $engineFileName \
    && rm $engineArchiveName \
    && mv $engineFileName godot \
    && mv godot /usr/bin/

# Install Godot templates
ENV GODOT_TEMPLATES_DIR="/root/.local/share/godot/export_templates"
RUN wget $templatesUrl \
    && mkdir -p ${GODOT_TEMPLATES_DIR} \
    && unzip $templatesArchiveName \
    && rm $templatesArchiveName \
    && mv templates ${GODOT_TEMPLATES_DIR} \
    && mv ${GODOT_TEMPLATES_DIR}/templates ${GODOT_TEMPLATES_DIR}/$templatesDirectory

ENTRYPOINT ["godot"]