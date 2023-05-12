ARG ubuntuVersion

FROM ubuntu:$ubuntuVersion AS base

ARG godotVersion

# Setup apt-get
RUN apt-get update

# Install basics
RUN apt-get install -y \
    wget \
    unzip

# Install Godot
RUN wget https://downloads.tuxfamily.org/godotengine/$godotVersion/Godot_v$godotVersion-stable_linux.x86_64.zip \
    && unzip Godot_v$godotVersion-stable_linux.x86_64.zip \
    && rm Godot_v$godotVersion-stable_linux.x86_64.zip \
    && mv Godot_v$godotVersion-stable_linux.x86_64 godot \
    && mv godot /usr/bin/

# Install Godot deps
RUN apt-get install -y \
    libfontconfig

# Install Godot templates
ENV GODOT_TEMPLATES_DIR="/root/.local/share/godot/export_templates"
RUN wget https://downloads.tuxfamily.org/godotengine/$godotVersion/Godot_v$godotVersion-stable_export_templates.tpz \
    && mkdir -p ${GODOT_TEMPLATES_DIR} \
    && unzip Godot_v$godotVersion-stable_export_templates.tpz \
    && rm Godot_v$godotVersion-stable_export_templates.tpz \
    && mv templates ${GODOT_TEMPLATES_DIR} \
    && mv ${GODOT_TEMPLATES_DIR}/templates ${GODOT_TEMPLATES_DIR}/$godotVersion.stable

CMD godot
