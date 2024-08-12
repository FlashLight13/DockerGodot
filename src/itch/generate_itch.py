import generate_core as GenerateCore

from model.generation_result import GenerationResult


def generate(release, is_debug):
    return GenerationResult(
        job_name=get_job_name(release),
        job=__job_template(__steps_for_release(release)),
        dependencies=[GenerateCore.get_job_name(release)],
    )


def get_job_name(release):
    return "publish-itch-" + release.version


def __job_template(steps):
    return {
        "docker": [
            {"image": GenerateCore.CIRCLE_CI_JOB_IMAGE},
        ],
        "steps": steps,
    }


def __steps_for_release(release):
    docker_tag = GenerateCore.DOCKER_NAMESPACE + "/" + GenerateCore.DOCKER_REPOSITORY + ":" + release.version
    return [
        # checkout code
        "checkout",
        {
            "setup_remote_docker": {
                "version": GenerateCore.CIRCLE_CI_REMOTE_DOCKER_VERSION,
                "docker_layer_caching": True,
            }
        },
        # Login to the Docker
        {
            "run": "echo "
            + GenerateCore.DOCKER_PASS_ENV_CONST
            + " | docker login -u "
            + GenerateCore.DOCKER_LOGIN_ENV_CONST
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
            + GenerateCore.DOCKER_FILE
            + " "
            + "."
        },
        # Push the base image
        {"run": "docker push " + docker_tag},
    ]
