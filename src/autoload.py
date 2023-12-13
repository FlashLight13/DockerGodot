import requests
import argparse
import json
import logging
import subprocess
from http import HTTPStatus

# docker.py
import docker
# arguments.py
import arguments

GIT_PAGE_SIZE = 100
GIT_DEBUG_PAGE_SIZE = 5

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
	]
# File template for Godot export templates
EXPORT_TEMPLATES_TEMPLATE = "Godot_v%s-%s_export_templates.tpz"


class GodotRelease:

	def __init__(
		self,
		version,
		channel,

		engine_url,
		engine_file_name,
		engine_archive_name,

		templates_url,
		templates_archive_name,
	):
		self.version = version
		self.channel = channel

		self.engine_url = engine_url
		self.engine_file_name = engine_file_name
		self.engine_archive_name = engine_archive_name

		self.templates_url = templates_url
		self.templates_archive_name = templates_archive_name


def crawl(args) -> None:
	debug = args.is_debug or args.debug
	print("Debug enabled: " + str(debug))
	if args.is_incremental:
		existing_versions = docker.load_existing_versions()
		print("Loaded existing_versions: " + ', '.join(existing_versions))
	else:
		existing_versions = []
		print("Force updating images")

	releases = map(build_release_model, load_releases(debug))
	releases = filter(lambda release: release.version not in existing_versions, releases)

	docker.login(args)

	for release in releases:
		docker.upload_docker(release, debug)
		print("Uploaded " + release.version + "-" + release.channel)


def build_release_model(release):
	version = release["tag_name"].split('-')[0]
	channel = release["tag_name"].split('-')[1]
	
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
		version = version,
		channel = channel,

		engine_url = engine_url,
		engine_archive_name = engine_archive_name,
		engine_file_name = engine_file_name,

		templates_url = templates_url,
		templates_archive_name = templates_archive_name,
	)


def load_releases(debug):
	if debug:
		page_size = GIT_DEBUG_PAGE_SIZE
	else:
		page_size = GIT_PAGE_SIZE
	releases = []
	page = 1
	while not debug or page == 1:
		page_url = "https://api.github.com/repos/godotengine/godot-builds/releases?per_page=" + str(page_size) + "&page=%s"
		headers = {

		}
		response = requests.get(page_url % page, headers = headers)
		release = json.loads(response.content)
		if len(release) == 0:
			break
		releases += release
		page += 1
	return releases


def main():
	parser = arguments.setup_parser()
	args = parser.parse_args()
	crawl(args)

if __name__ == '__main__':
    main()
