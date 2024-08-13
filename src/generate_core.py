from model.generation_result import GenerationResult
from model.docker_tag import DockerTag
import circle_ci_config

# Docker file to build an image with
DOCKER_FILE = "src/godot.dockerfile"
# https://hub.docker.com/repository/docker/flashlight13/godot


def generate(release):
    return GenerationResult(
        job_name=get_job_name(release),
        job=__job_template(__steps_for_release(release)),
        dependencies=[],
    )


def get_job_name(release):
    return "publish-core-" + release.version.replace('.', "_") 


def get_docker_tag():
    return DockerTag(namespace="flashlight13", repository="godot")


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
            + docker_tag
            + " "
            + "--build-arg godotVersion="
            + release.version
            + " "
            + "--build-arg engineUrl="
            + release.engine_url
            + " "
            + "--build-arg engineArchiveName="
            + release.engine_archive_name
            + " "
            + "--build-arg engineFileName="
            + release.engine_file_name
            + " "
            + "--build-arg templatesUrl="
            + release.templates_url
            + " "
            + "--build-arg templatesArchiveName="
            + release.templates_archive_name
            + " "
            + "--build-arg templatesDirectory="
            + release.version
            + "."
            + release.channel
            + " "
            + "-f "
            + DOCKER_FILE
            + " "
            + "."
        },
        # Push the base image
        {"run": "docker push " + docker_tag},
    ]
