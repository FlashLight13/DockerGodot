from model.godot_release_entity import GodotRelease
from packaging.version import Version
import requests
import json
import subprocess


FIRST_SUPPORTED_MAJOR_VERSION = 3
SUPPORTED_CHANNELS = ["stable"]
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


def load_releases(use_gh, debug):
    if debug:
        page_size = 25
    else:
        page_size = 100
    releases = []
    page = 1
    # Load a single page for debug builds
    while not debug or page == 1:
        if use_gh:
            release = json.loads(
                subprocess.run(
                    [
                        "gh",
                        "api",
                        "--method",
                        "GET",
                        "repos/godotengine/godot-builds/releases",
                        "-F",
                        "per_page=" + str(page_size),
                        "-F",
                        "page=" + str(page),
                    ],
                    stdout=subprocess.PIPE,
                ).stdout
            )
        else:
            page_url = (
                "https://api.github.com/repos/godotengine/godot-builds/releases?per_page="
                + str(page_size)
                + "&page=%s"
            )
            headers = {}
            response = requests.get(page_url % page, headers=headers)
            release = json.loads(response.content)
            if response.status_code != 200:
                raise Exception(
                    "Failed to load releases "
                    + str(response)
                    + " "
                    + str(response.content)
                )
        if len(release) == 0:
            break
        releases += release
        page += 1
    releases = map(lambda release: __build_release_model(release=release), releases)
    return filter(lambda release: release, releases)


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
