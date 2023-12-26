import argparse


def setup_parser():
    parser = argparse.ArgumentParser(
        prog='Godot Docker autoloader',
        description='Automatically crawles existing Godot versions of the engine and creates corresponding Docker images',
        epilog='by Anton Potapov @flashlight13')

    parser.add_argument('-i', '--is_incremental', action="store_true",
                        help="True to reupload existing docker images")
    parser.add_argument('-d', '--debug', action="store_true",
                        help="Enables debug mode (reduced page size and disabled images uploading)")
    parser.add_argument(
        '--is_debug', help="Enables debug mode (reduced page size and disabled images uploading)")

    parser.add_argument(
        '--trigger_branch', help="Docker pass to use when uploading the images")

    return parser
