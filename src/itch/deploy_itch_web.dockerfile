ARG godotVersion
FROM flashlight13/godot:godotVersion AS base

ARG butlerVersion
# Versions before 4.1 have problems importing a project via CLI
# https://github.com/godotengine/godot/issues/69511
ARG needsWorkaround=true

RUN apt-get install zip

# Install Itch.io butler
ENV BUTLER_HOME=/opt/butler
RUN wget https://broth.itch.ovh/butler/linux-amd64/${butlerVersion}/archive/default \
    && unzip default -d ${BUTLER_HOME} \
    && export PATH="$BUTLER_HOME:$PATH"

# Prepare a script to export the file
ENV EXPORT_SCRIPT=/opt/exporter/export_to_itch
RUN mkdir -p /opt/exporter/

RUN printf '#!/bin/bash \n\
# Check the environment \n\
[ -z "$artifactName" ] && echo "Need to set ARTIFACT_NAME. This is the name of the file that will be uploaded" && exit 1; \n\
[ -z "$BUILD_PRESET" ] && echo "Need to set BUILD_PRESET. See export_presets.cfg for one" && exit 1; \n\

mkdir -p out/intermediates/${BUILD_PRESET} \n\
godot --headless --export-release "${BUILD_PRESET}" out/intermediates/${BUILD_PRESET}/index.html \n\
if $needsWorkaround \n\
then \n\
    godot --headless --export-release "${BUILD_PRESET}" out/intermediates/${BUILD_PRESET}/index.html \n\
fi \n\

# Prepare the archive \n\
mkdir -p out/artifacts/ \n\
zip -rj out/artifacts/${artifactName} out/intermediates/${BUILD_PRESET} \n\

# Upload \n\
butler push out/artifacts/${artifactName} flashlight13/test-project:html \n\
' >> $EXPORT_SCRIPT \
    && chmod +x $EXPORT_SCRIPT \
    && export PATH="$EXPORT_SCRIPT:$PATH"


CMD $EXPORT_SCRIPT