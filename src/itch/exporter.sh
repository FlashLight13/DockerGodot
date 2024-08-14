#!/bin/bash

function help {
  echo "
  -h --help            show help
  (m)  --projectPath            path to project.godot
  (m)  --outputPath             uild output directory. Relative to --projectPath
       --artifactPath           path to the archive generated by the script. Relative to --projectPath
                                defaults to the same value as outputPath
       --artifactFileName       name of the archive to be generated by the script
                                defaults to index
  (m)  --buildPreset            name of the preset to use from export_presets.cfg
  (m)  --doubleImport           perform double import to work around 
                                https://github.com/godotengine/godot/issues/69511 for older Godot versions. 
                                Defaults to false
       --butlerPushDestination  destination for butler push command
       --butlerParams           these parameters are passed to the Butler

  (m)  means that the parameter is mandatory.
  "
}

DOUBLE_IMPORT=false

# Parse arguments
for i in "$@"; do
  case $i in
  -h | --help)
    help
    exit
    ;;
  -V | --version)
    echo "Always the best! :)"
    exit
    ;;
  --projectPath=*)
    PROJECT_PATH="${i#*=}"
    shift
    ;;
  --outputPath=*)
    OUTPUT_PATH="${i#*=}"
    shift
    ;;
  --buildPreset=*)
    BUILD_PRESET="${i#*=}"
    shift
    ;;
  --doubleImport)
    DOUBLE_IMPORT=true
    shift 1
    ;;
  --artifactPath=*)
    ARTIFACT_PATH="${i#*=}"
    shift
    ;;
  --artifactFileName=*)
    ARTIFACT_FILE_NAME="${i#*=}"
    shift
    ;;
  --butlerPushDestination=*)
    BUTLER_PUSH_DESTINATION="${i#*=}"
    shift
    ;;
  --butlerParams=*)
    BUTLER_PARAMETERS="${i#*=}"
    shift
    ;;
  *)
    BUTLER_PARAMS="$BUTLER_PARAMS $1"
    shift
    ;;
  esac
done
shift $((OPTIND - 1))

echo "projectPath=$PROJECT_PATH"
echo "outputPath=$OUTPUT_PATH"
echo "buildPreset=$BUILD_PRESET"
echo "butlerPushDestination=$BUTLER_PUSH_DESTINATION"
echo "doubleImport=$DOUBLE_IMPORT"

if [ -z "$PROJECT_PATH" ] || [ -z "$OUTPUT_PATH" ] || [ -z "$BUILD_PRESET" ] || [ -z "$BUTLER_PUSH_DESTINATION" ]; then
  echo "One or more parameter is missing"
  exit 1
fi
if [ -z "$ARTIFACT_PATH" ]; then
  ARTIFACT_PATH=$OUTPUT_PATH
fi
if [ -z "$ARTIFACT_FILE_NAME" ]; then
  ARTIFACT_FILE_NAME="index"
fi

# Export the project
cd "$PROJECT_PATH"
mkdir -p "$OUTPUT_PATH"
godot --headless --export-release "$BUILD_PRESET" "$OUTPUT_PATH/index.html"
echo "BUILD FINISHED"
if [ "$DOUBLE_IMPORT" = true ]; then
  echo "STARTING SECOND WORKAROUND EXPORT"
  godot --headless --export-release "$BUILD_PRESET" "$OUTPUT_PATH/index.html"
fi

echo "PUSHING THE BUILD"
# Prepare the archive
mkdir -p "$ARTIFACT_PATH"
zip -rj "$ARTIFACT_PATH"/"$ARTIFACT_FILE_NAME".zip "$OUTPUT_PATH"/

# Upload
butler push "$ARTIFACT_PATH"/"$ARTIFACT_FILE_NAME".zip "$BUTLER_PUSH_DESTINATION" "$BUTLER_PARAMETERS"
