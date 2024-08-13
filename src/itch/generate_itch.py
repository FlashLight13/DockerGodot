import generate_core as GenerateCore

from model.generation_result import GenerationResult
from model.docker_tag import DockerTag
import circle_ci_config

# Latest from https://github.com/itchio/butler/releases
BUTLER_VERSION = "v15.21.0"

# Docker file to build an image with
DOCKER_FILE = "src/itch/itch.dockerfile"


def generate(release):
    return GenerationResult(
        job_name=get_job_name(release),
        job=__job_template(__steps_for_release(release)),
        dependencies=[GenerateCore.get_job_name(release)],
    )


def get_job_name(release):
    return "publish-itch-" + release.version.replace('.', "_") 


def get_docker_tag():
    return DockerTag(namespace="flashlight13", repository="godot-itch")


def __job_template(steps):
    return {
        "docker": [
            {"image": circle_ci_config.JOB_IMAGE},
        ],
        "steps": steps,
    }


def __steps_for_release(release):
    docker_tag = (
        get_docker_tag().namespace
        + "/"
        + get_docker_tag().repository
        + ":"
        + release.version
    )
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
            + "--tag "
            + docker_tag
            + " "
            + "--build-arg godotVersion="
            + release.version
            + " "
            + "--build-arg butlerVersion="
            + BUTLER_VERSION
            + " "
            + "-f "
            + DOCKER_FILE
            + " "
            + "."
        },
        # Push the base image
        {"run": "docker push " + docker_tag},
    ]
