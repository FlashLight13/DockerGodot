from model.generation_result import GenerationResult
import argparse
import create_config_yaml
import api.docker as docker
import api.github as github
import core.generate_core as generate_core
import itch.generate_itch as generate_itch
import graphlib


class JobsGenerator:

    def __init__(
        self,
        key,
        module,
        coordinates,
        dependencies,
    ):
        self.key = key
        self.module = module
        self.coordinates = coordinates
        self.dependencies = dependencies


GENERATED_CONFIG_PATH = ".circleci/images.yml"
GENERATORS = [
    JobsGenerator(
        key="itch",
        module=generate_itch,
        dependencies=["core"],
        coordinates=generate_itch.DOCKER_COORDINATES,
    ),
    JobsGenerator(
        key="core",
        module=generate_core,
        dependencies=[],
        coordinates=generate_core.DOCKER_COORDINATES,
    ),
]


def crawl(args) -> None:
    is_debug = args.is_debug or args.debug
    incremental = args.is_incremental in ["True", "true", 1]
    use_gh = args.use_gh
    print("===========    ARGS    ===========")
    print("is_debug=" + str(is_debug))
    print("is_incremental=" + str(incremental))
    print("use_gh=" + str(use_gh))
    print("==================================")

    generators = list(__topological_generators())
    releases = list(github.load_releases(use_gh=use_gh, debug=is_debug))
    existing_tags = docker.load_existing_versions(
        coorinates_list=map(lambda generator: generator.coordinates, GENERATORS),
        debug=is_debug,
    )
    print("Generators:")
    print("  " + str([*map(lambda generator: generator.key, generators)]))
    print("Releases to process:")
    print("  " + str([*map(lambda release: release.version, releases)]))
    print("Existing tags:")
    for coordinate in existing_tags.keys():
        print("  " + str(coordinate) + ": " + str(existing_tags[coordinate]))
    print("==================================")

    generation_results = []
    for release in releases:
        print("Processing release=" + str(release.version))
        generation_results_for_release = {}
        for jobs_generator in generators:
            if (
                incremental
                and jobs_generator.module.docker_tag(release)
                in existing_tags[jobs_generator.coordinates]
            ):
                print(
                    "  Skipping "
                    + str(release.version)
                    + " for "
                    + str(jobs_generator.key)
                )
                continue
            dependencies_to_add = filter(
                lambda dependency_key: dependency_key in generation_results_for_release,
                jobs_generator.dependencies,
            )
            dependencies_to_add = map(
                lambda dependency_key: generation_results_for_release[dependency_key].job_name,
                dependencies_to_add,
            )
            generation_result = GenerationResult(
                job_name=__job_name(jobs_generator, release),
                job=jobs_generator.module.generate(release),
                dependencies=list(dependencies_to_add),
            )
            print(
                "  Adding " + str(generation_result) + " for " + str(jobs_generator.key)
            )
            generation_results_for_release[jobs_generator.key] = generation_result
        generation_results = generation_results + list(
            generation_results_for_release.values()
        )

    with open(GENERATED_CONFIG_PATH, "w+") as outfile:
        create_config_yaml.create(generation_results, outfile)


def __job_name(generator, release):
    return "publish-" + generator.key + "-" + release.version.replace(".", "_")


def __topological_generators():
    sorter = graphlib.TopologicalSorter()
    for generator in GENERATORS:
        sorter.add(generator.key, *generator.dependencies)
    return map(
        lambda generator_key: next(
            filter(lambda generator: generator.key == generator_key, GENERATORS)
        ),
        sorter.static_order(),
    )


def __setup_parser():
    parser = argparse.ArgumentParser(
        prog="Godot Docker autoloader",
        description="Automatically crawles existing Godot versions of the engine and creates corresponding Docker images",
        epilog="by Anton Potapov @flashlight13",
    )

    parser.add_argument(
        "--is_incremental",
        help="True to reupload existing docker images",
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
        "--use_gh",
        default=False,
        action="store_true",
        help="Use GitHub cli for API request instead of rest",
    )

    return parser


def main():
    parser = __setup_parser()
    args = parser.parse_args()
    crawl(args)


if __name__ == "__main__":
    main()
