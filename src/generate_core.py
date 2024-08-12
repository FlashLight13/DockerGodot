from model.generation_result import GenerationResult

CIRCLE_CI_CONFIG_VERSION = 2.1
CIRCLE_CI_JOB_IMAGE = "cimg/python:3.12.1"
CIRCLE_CI_REMOTE_DOCKER_VERSION = "20.10.18"

# Docker file to build an image with
DOCKER_FILE = "src/godot.dockerfile"
# https://hub.docker.com/repository/docker/flashlight13/godot
DOCKER_NAMESPACE = "flashlight13"
DOCKER_REPOSITORY = "godot"


def generate(release, credentials):
    return GenerationResult(
        job_name=get_job_name(release),
        job=__job_template(__steps_for_release(release, credentials)),
        dependencies=[],
    )


def get_job_name(release):
    return "publish-core-" + release.version


def __job_template(steps):
    return {
        "docker": [
            {"image": CIRCLE_CI_JOB_IMAGE},
        ],
        "steps": steps,
    }


def __steps_for_release(release, credentials):
    docker_tag = DOCKER_NAMESPACE + "/" + DOCKER_REPOSITORY + ":" + release.version
    return [
        # checkout code
        "checkout",
        {
            "setup_remote_docker": {
                "version": CIRCLE_CI_REMOTE_DOCKER_VERSION,
                "docker_layer_caching": True,
            }
        },
        # Login to the Docker
        {
            "run": "echo "
            + credentials.pass_env
            + " | docker login -u "
            + credentials.login_env
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
