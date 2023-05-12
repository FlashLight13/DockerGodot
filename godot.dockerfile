FROM ubuntu:23.04 AS base

ENV GODOT_VERSION "4.0.2"
ENV GODOT_TEMPLATES_DIR="/root/.local/share/godot/export_templates"

# Setup apt-get
RUN apt-get update

# Install basics
RUN apt-get install -y \
    wget \
    unzip

# Install Godot
RUN wget https://downloads.tuxfamily.org/godotengine/${GODOT_VERSION}/Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip \
    && unzip Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip \
    && rm Godot_v${GODOT_VERSION}-stable_linux.x86_64.zip \
    && mv Godot_v4.0.2-stable_linux.x86_64 godot \
    && mv godot /usr/bin/

# Install Godot deps
RUN apt-get install -y \
    libfontconfig

# Install Godot templates
RUN wget https://downloads.tuxfamily.org/godotengine/${GODOT_VERSION}/Godot_v${GODOT_VERSION}-stable_export_templates.tpz \
    && mkdir -p ${GODOT_TEMPLATES_DIR} \
    && unzip Godot_v${GODOT_VERSION}-stable_export_templates.tpz \
    && rm Godot_v${GODOT_VERSION}-stable_export_templates.tpz \
    && mv templates ${GODOT_TEMPLATES_DIR} \
    && mv ${GODOT_TEMPLATES_DIR}/templates ${GODOT_TEMPLATES_DIR}/${GODOT_VERSION}.stable

CMD godot
