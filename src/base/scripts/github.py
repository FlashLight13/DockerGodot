import requests
import json

PAGE_SIZE = 100
DEBUG_PAGE_SIZE = 5


def load_releases(debug):
    if debug:
        page_size = DEBUG_PAGE_SIZE
    else:
        page_size = PAGE_SIZE
    releases = []
    page = 1
    while not debug or page == 1:
        page_url = "https://api.github.com/repos/godotengine/godot-builds/releases?per_page=" + \
            str(page_size) + "&page=%s"
        headers = {

        }
        response = requests.get(page_url % page, headers=headers)
        release = json.loads(response.content)
        if len(release) == 0:
            break
        releases += release
        page += 1
    return releases
