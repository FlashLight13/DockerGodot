from model.godot_release_entity import GodotRelease
import docker
import github
import arguments
import create_config_yaml
from packaging.version import Version

FIRST_SUPPORTED_MAJOR_VERSION = 3
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


def crawl(args) -> None:
    debug = args.is_debug or args.debug
    print("Debug enabled: " + str(debug))
    if args.is_incremental:
        existing_versions = docker.load_existing_versions(debug)
        print("Existing releases: " + ', '.join(existing_versions))
    else:
        existing_versions = []
        print("Force updating images")

    releases = map(build_release_model, github.load_releases(debug))
    releases = filter(lambda release: release, releases)
    releases = list(releases)
    releases_log = map(
        lambda release: release.printable_version(), releases)
    print("Loaded releases: " + ", ".join(releases_log))

    releases = filter(
        lambda release: release.version not in existing_versions,
        releases,
    )
    releases = list(releases)

    with open(GENERATED_CONFIG_PATH, 'w+') as outfile:
        create_config_yaml.create(releases, outfile)


def build_release_model(release):
    version = release["tag_name"].split('-')[0]
    channel = release["tag_name"].split('-')[1]

    if Version(version).major < FIRST_SUPPORTED_MAJOR_VERSION:
        print("Skipped " + version + "-" + channel)
        return None

    engine_url = None
    engine_file_name = None
    engine_archive_name = None

    templates_url = None
    templates_archive_name = None

    for asset in release["assets"]:
        if engine_url is None:
            for engine_template in ENGINE_TEMPLATES:
                file_name = engine_template["archive_name"] % (
                    version, channel)
                if asset["name"] == file_name:
                    engine_url = asset["browser_download_url"]
                    engine_archive_name = file_name
                    engine_file_name = engine_template["file_name"] % (
                        version, channel)
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


def main():
    parser = arguments.setup_parser()
    args = parser.parse_args()
    crawl(args)


if __name__ == '__main__':
    main()
