import yaml
from model.godot_release_entity import GodotRelease


CIRCLE_CI_CONFIG_VERSION = 2.1
CIRCLE_CI_JOB_IMAGE = "cimg/python:3.12.1"
CIRCLE_CI_REMOTE_DOCKER_VERSION = "20.10.18"

# Docker file to build an image with
DOCKER_FILE = "src/base/godot.dockerfile"
SNAPSHOT_TAG = "snapshot"
# https://hub.docker.com/repository/docker/flashlight13/godot
DOCKER_NAMESPACE = "flashlight13"
DOCKER_REPOSITORY = "godot"
# Setup in CI
DOCKER_LOGIN_ENV_CONST = "$DOCKERHUB_LOGIN"
DOCKER_PASS_ENV_CONST = "$DOCKERHUB_PASSWORD"


def create(releases, output_file, is_snapshot):
    json_config = config_template()
    if releases:
        releases_log = []
        for release in releases:
            releases_log.append(release.printable_version())
            job_name = "publish-" + \
                release.version.replace('.', "_")
            json_config["jobs"][job_name] = job_template(
                steps_for_release(release, is_snapshot))
            json_config["workflows"]["publish"]["jobs"].append(job_name)
        print("Included in the config: " + ", ".join(releases_log))
    else:
        job_name = "empty_job"
        json_config["jobs"][job_name] = job_template(
            [
                {
                    "run": "echo nothing to do here"
                },
            ]
        )
        json_config["workflows"]["publish"]["jobs"].append(job_name)
        print("Nothing to include. An empty config created")
    yaml.safe_dump(
        json_config,
        output_file,
        indent=2,
        default_style=None,
        default_flow_style=False
    )


def config_template():
    return {
        "version": CIRCLE_CI_CONFIG_VERSION,
        "jobs": {

        },
        "workflows": {
            "publish": {
                "jobs": [],
            },
        },
    }


def job_template(steps):
    return {
        "docker": [
            {"image": CIRCLE_CI_JOB_IMAGE},
        ],
        "steps": steps,
    }


def steps_for_release(release, is_snapshot):
    if is_snapshot:
        docker_tag = SNAPSHOT_TAG
    else:
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
            "run": "echo " + DOCKER_PASS_ENV_CONST + " | docker login -u "
            + DOCKER_LOGIN_ENV_CONST + " --password-stdin",
        },

        # Build image
        {
            "run": "docker build" + " "
            + "--tag " + docker_tag + " "
            + "--build-arg godotVersion=" + release.version + " "

            + "--build-arg engineUrl=" + release.engine_url + " "
            + "--build-arg engineArchiveName=" + release.engine_archive_name + " "
            + "--build-arg engineFileName=" + release.engine_file_name + " "

            + "--build-arg templatesUrl=" + release.templates_url + " "
            + "--build-arg templatesArchiveName=" + release.templates_archive_name + " "
            + "--build-arg templatesDirectory=" + \
            release.version + "." + release.channel + " "

            + "-f " + DOCKER_FILE + " "
            + "."
        },

        # Push the image
        {
            "run": "docker push " + docker_tag
        },
    ]
