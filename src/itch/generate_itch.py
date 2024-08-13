from model.generation_result import GenerationResult
from model.docker_coordinates import DockerCoordinates
import circle_ci_config

# Latest from https://github.com/itchio/butler/releases
BUTLER_VERSION = "v15.21.0"

# Docker file to build an image with
DOCKER_FILE = "src/itch/itch.dockerfile"
DOCKER_COORDINATES = DockerCoordinates(
    namespace="flashlight13", repository="godot-itch"
)


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
    tag = DOCKER_COORDINATES.path() + ":" + docker_tag(release)
    return [
        # checkout code
        "checkout",
        {
            "setup_remote_docker": {
                "version": circle_ci_config.REMOTE_DOCKER_VERSION,
                "docker_layer_caching": True,
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
            + ("--tag " + tag)
            + " "
            + ("--build-arg godotVersion=" + release.version)
            + " "
            + ("--build-arg butlerVersion=" + BUTLER_VERSION)
            + " "
            + ("-f " + DOCKER_FILE)
            + " "
            + "."
        },
        # Push the base image
        {"run": "docker push " + tag},
    ]
