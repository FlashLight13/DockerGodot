import yaml
import circle_ci_config

# Docker file to build an image with
DOCKER_FILE = "src/base/godot.dockerfile"
# https://hub.docker.com/repository/docker/flashlight13/godot
DOCKER_NAMESPACE = "flashlight13"
DOCKER_REPOSITORY = "godot"
# Setup in CI
DOCKER_LOGIN_ENV_CONST = "$DOCKERHUB_LOGIN"
DOCKER_PASS_ENV_CONST = "$DOCKERHUB_PASSWORD"


def create(generation_results, output_file):
    json_config = __config_template()
    if generation_results:
        for generation_result in generation_results:
            json_config["jobs"][
                generation_result.get_safe_job_name()
            ] = generation_result.job
            json_config["workflows"]["publish"]["jobs"].append(
                generation_result.get_safe_job_name()
            )
            if generation_result.dependencies:
                for dependency in generation_result.dependencies:
                    json_config["workflows"]["publish"]["jobs"][
                        generation_result.get_safe_job_name()
                    ]["requires"].append(dependency)
    else:
        job_name = "empty_job"
        json_config["jobs"][job_name] = __job_template(
            [
                {"run": "echo nothing to do here"},
            ]
        )
        json_config["workflows"]["publish"]["jobs"].append(job_name)
        print("Nothing to include. An empty config created")
    yaml.safe_dump(
        json_config, output_file, indent=2, default_style=None, default_flow_style=False
    )


def __config_template():
    return {
        "version": circle_ci_config.CONFIG_VERSION,
        "jobs": {},
        "workflows": {
            "publish": {
                "jobs": [],
            },
        },
    }


def __job_template(steps):
    return {
        "docker": [
            {"image": circle_ci_config.JOB_IMAGE},
        ],
        "steps": steps,
    }
