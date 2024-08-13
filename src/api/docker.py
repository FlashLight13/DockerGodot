import requests
import json


def load_existing_versions(coorinates_list, debug):
    result = {}
    for coordinates in coorinates_list:
        result[coordinates] = __load_existing_versions(
            coordinates=coordinates, debug=debug
        )
    return result


def __load_existing_versions(coordinates, debug):
    if debug:
        page_size = 5
    else:
        page_size = 100
    existing_versions = []
    url = (
        "https://hub.docker.com/v2/namespaces/"
        + coordinates.namespace
        + "/repositories/"
        + coordinates.repository
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
