FROM alpine:3.19.0 AS base

ARG engineUrl
ARG engineArchiveName
ARG engineFileName

ARG templatesUrl
ARG templatesArchiveName
ARG templatesDirectory

# Setup apt-get and install basics
RUN apk add --no-cache \
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

RUN apk add libc6-compat \
alsa-lib \
ca-certificates-bundle \
enet \
eudev-libs \
fontconfig \
freetype \
glslang-libs \
harfbuzz \
harfbuzz-icu \
icu-libs \
libgcc \
libogg \
libpcre2-32 \
libpng \
libpulse \
libstdc++ \
libtheora \
libvorbis \
libwebp \
libx11 \
libxcursor \
libxext \
libxi \
libxinerama \
libxrandr \
libxrender \
mbedtls \
miniupnpc \
musl \
wslay \
zlib \
zstd-libs

RUN apk --no-cache add ca-certificates
RUN wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.28-r0/glibc-2.28-r0.apk && apk add glibc-2.28-r0.apk --force-overwrite

ENTRYPOINT ["godot"]