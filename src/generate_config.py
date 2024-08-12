from model.godot_release_entity import GodotRelease
from model.docker_credentials import DockerCredentials
from model.docker_tag import DockerTag
import argparse
import create_config_yaml
import importlib
from packaging.version import Version
import requests
import json

FIRST_SUPPORTED_MAJOR_VERSION = 3
SUPPORTED_CHANNELS = ["stable"]
GENERATED_CONFIG_PATH = ".circleci/images.yml"
# File templates for the Godot engine
ENGINE_TEMPLATES = [
    {
        "archive_name": "Godot_v%s-%s_x11.64.zip",
        "file_name": "Godot_v%s-%s_x11.64",
    },
    {
        "archive_name": "Godot_v%s-%s_linux.x86_64.zip",
        "file_name": "Godot_v%s-%s_linux.x86_64",
    },
    {
        "archive_name": "Godot_v%s-%s_linux.64.zip",
        "file_name": "Godot_v%s-%s_linux.64",
    },
    {
        "archive_name": "Godot_v%s_%s_x11.64.zip",
        "file_name": "Godot_v%s-%s_x11.64",
    },
]
# File template for Godot export templates
EXPORT_TEMPLATES_TEMPLATE = "Godot_v%s-%s_export_templates.tpz"

DOCKER_CREDENTIALS = DockerCredentials(
    login_env="$DOCKERHUB_LOGIN", pass_env="$DOCKERHUB_PASSWORD"
)


def crawl(args) -> None:
    is_debug = args.is_debug or args.debug
    incremental = args.is_incremental in ["True", "true", "1"]
    print("is_debug=" + str(is_debug))
    print("is_incremental=" + str(incremental))
    if incremental:
        existing_versions = __load_existing_versions(is_debug, DockerTag("", ""))
        print("Existing releases: " + ", ".join(existing_versions))
    else:
        existing_versions = []
        print("Force updating images")

    releases = map(__build_release_model, __load_releases(is_debug))
    releases = filter(lambda release: release, releases)
    releases = list(releases)
    releases_log = map(lambda release: release.version, releases)
    print("Loaded releases: " + ", ".join(releases_log))

    releases = filter(
        lambda release: release.version not in existing_versions, releases
    )

    releases = list(releases)

    generation_results = []
    for generation_module_path in args.generation_scripts:
        generation_module = importlib.import_module(generation_module_path)
        for release in releases:
            generation_results.append(generation_module.generate(release, DOCKER_CREDENTIALS))

    with open(GENERATED_CONFIG_PATH, "w+") as outfile:
        create_config_yaml.create(generation_results, outfile)


def __build_release_model(release):
    version = release["tag_name"].split("-")[0]
    channel = release["tag_name"].split("-")[1]

    if Version(version).major < FIRST_SUPPORTED_MAJOR_VERSION:
        return None
    if channel not in SUPPORTED_CHANNELS:
        return None

    engine_url = None
    engine_file_name = None
    engine_archive_name = None

    templates_url = None
    templates_archive_name = None

    for asset in release["assets"]:
        if engine_url is None:
            for engine_template in ENGINE_TEMPLATES:
                file_name = engine_template["archive_name"] % (version, channel)
                if asset["name"] == file_name:
                    engine_url = asset["browser_download_url"]
                    engine_archive_name = file_name
                    engine_file_name = engine_template["file_name"] % (version, channel)
        if templates_url is None:
            file_name = EXPORT_TEMPLATES_TEMPLATE % (version, channel)
            if asset["name"] == file_name:
                templates_url = asset["browser_download_url"]
                templates_archive_name = file_name
    if engine_url is None:
        raise Exception(release["tag_name"] + " has no engine")
    if templates_url is None:
        raise Exception(release["tag_name"] + " has no templates")

    return GodotRelease(
        version=version,
        channel=channel,
        engine_url=engine_url,
        engine_archive_name=engine_archive_name,
        engine_file_name=engine_file_name,
        templates_url=templates_url,
        templates_archive_name=templates_archive_name,
    )


def __load_releases(debug):
    if debug:
        page_size = 5
    else:
        page_size = 100
    releases = []
    page = 1
    while not debug or page == 1:
        page_url = (
            "https://api.github.com/repos/godotengine/godot-builds/releases?per_page="
            + str(page_size)
            + "&page=%s"
        )
        headers = {}
        response = requests.get(page_url % page, headers=headers)
        release = json.loads(response.content)
        if len(release) == 0:
            break
        releases += release
        page += 1
    return releases


# Setup in CI
DOCKER_LOGIN_ENV_CONST = "$DOCKERHUB_LOGIN"
DOCKER_PASS_ENV_CONST = "$DOCKERHUB_PASSWORD"


def __load_existing_versions(debug, tag):
    if debug:
        page_size = 5
    else:
        page_size = 100
    existing_versions = []
    url = (
        "https://hub.docker.com/v2/namespaces/"
        + tag.namespace
        + "/repositories/"
        + tag.repository
        + "/tags"
        + "?page_size="
        + str(page_size)
    )
    while url:
        response = requests.get(url)
        response = json.loads(response.content)
        existing_versions += map(lambda result: result["name"], response["results"])
        url = response["next"]
        # load only the first page for debugging
        if debug:
            return existing_versions

    return existing_versions


def __setup_parser():
    parser = argparse.ArgumentParser(
        prog="Godot Docker autoloader",
        description="Automatically crawles existing Godot versions of the engine and creates corresponding Docker images",
        epilog="by Anton Potapov @flashlight13",
    )

    parser.add_argument(
        "-i",
        "--incremental",
        action="store_true",
        help="True to reupload existing docker images",
    )
    parser.add_argument(
        "--is_incremental", help="True to reupload existing docker images"
    )

    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Enables debug mode (reduced page size and disabled images uploading)",
    )
    parser.add_argument(
        "--is_debug",
        help="Enables debug mode (reduced page size and disabled images uploading)",
    )

    parser.add_argument(
        "--generation_scripts",
        help="Which script to load to generate the config. generate(existing_tags, is_debug) will be called on that script to proceed",
    )

    return parser


def main():
    parser = __setup_parser()
    args = parser.parse_args()
    crawl(args)


if __name__ == "__main__":
    main()
