from model.generation_result import GenerationResult
from model.docker_coordinates import DockerCoordinates
import circle_ci_config

# Docker file to build an image with
DOCKER_FILE = "src/godot.dockerfile"
# https://hub.docker.com/repository/docker/flashlight13/godot
DOCKER_COORDINATES = DockerCoordinates(namespace="flashlight13", repository="godot")


def generate(release):
    return {
        "docker": [
            {"image": circle_ci_config.JOB_IMAGE},
        ],
        "steps": __steps_for_release(release),
    }


def docker_tag(release):
    return release.version


def __steps_for_release(release):
    return [
        # checkout code
        "checkout",
        {
            "setup_remote_docker": {
                "version": circle_ci_config.REMOTE_DOCKER_VERSION,
                "docker_layer_caching": circle_ci_config.DOCKER_LAYER_CACHING,
            }
        },
        # Login to the Docker
        {
            "run": "echo "
            + circle_ci_config.DOCKER_PASS
            + " | docker login -u "
            + circle_ci_config.DOCKER_LOGIN
            + " --password-stdin",
        },
        # Build the base image
        {
            "run": "docker build"
            + " "
            + "--tag "
            + (DOCKER_COORDINATES.path() + ":" + docker_tag(release))
            + " "
            + ("--build-arg godotVersion=" + release.version)
            + " "
            + ("--build-arg engineUrl=" + release.engine_url)
            + " "
            + ("--build-arg engineArchiveName=" + release.engine_archive_name)
            + " "
            + ("--build-arg engineFileName=" + release.engine_file_name)
            + " "
            + ("--build-arg templatesUrl=" + release.templates_url)
            + " "
            + ("--build-arg templatesArchiveName=" + release.templates_archive_name)
            + " "
            + (
                "--build-arg templatesDirectory="
                + release.version
                + "."
                + release.channel
            )
            + " "
            + ("-f " + DOCKER_FILE)
            + " "
            + "."
        },
        # Push the base image
        {"run": "docker push " + docker_tag(release)},
    ]
