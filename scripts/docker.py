import requests
import json

PAGE_SIZE = 100
DEBUG_PAGE_SIZE = 5

# https://hub.docker.com/repository/docker/flashlight13/godot
DOCKER_NAMESPACE = "flashlight13"
DOCKER_REPOSITORY = "godot"


def load_existing_versions(debug):
    if debug:
        page_size = DEBUG_PAGE_SIZE
    else:
        page_size = PAGE_SIZE
    existing_versions = []
    url = "https://hub.docker.com/v2/namespaces/" + DOCKER_NAMESPACE + \
        "/repositories/" + DOCKER_REPOSITORY + \
        "/tags" + "?page_size=" + str(page_size)
    while url:
        response = requests.get(url)
        response = json.loads(response.content)
        existing_versions += map(
            lambda result: result["name"], response["results"])
        url = response["next"]
        # load only the first page for debugging
        if debug:
            return existing_versions

    return existing_versions
