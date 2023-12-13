import requests
import subprocess
import json

# Page sisze when loading existing versions from the Docker
PAGE_SIZE = 100

DOCKER_FILE = "images/godot.dockerfile"

# https://hub.docker.com/repository/docker/flashlight13/godot 
DOCKER_NAMESPACE = "flashlight13"
DOCKER_REPOSITORY = "godot"

# Version of Ubuntu to use for the image
UBUNTU_VERSION = "23.04"


def login(args):
	print("Logging in to Docker")
	result = subprocess.run(
		"echo " + args.docker_pass + " | docker login -u " + args.docker_login + " --password-stdin",
		shell = True,
		stderr = subprocess.PIPE,
		check = True,
	)


def load_existing_versions():
	existing_versions = []
	url = "https://hub.docker.com/v2/namespaces/" + DOCKER_NAMESPACE + "/repositories/" + DOCKER_REPOSITORY + "/tags" + "?page_size=" + str(PAGE_SIZE)
	while url:
		response = requests.get(url)
		response = json.loads(response.content)
		existing_versions += map(lambda result: result["name"], response["results"])
		url = response["next"]

	return existing_versions


def upload_docker(release, debug):
	docker_tag = DOCKER_NAMESPACE + "/" + DOCKER_REPOSITORY + ":" + release.version + "-" + release.channel
	_run_command(
		[
			'docker', 'build',
			"--tag", docker_tag,
			"--build-arg", "ubuntuVersion=" + UBUNTU_VERSION,
			
			"--build-arg", "godotVersion=" + release.version,
			
			"--build-arg", "engineUrl=" + release.engine_url,
			"--build-arg", "engineArchiveName=" + release.engine_archive_name,
			"--build-arg", "engineFileName=" + release.engine_file_name,

			"--build-arg", "templatesUrl=" + release.templates_url,
			"--build-arg", "templatesArchiveName=" + release.templates_archive_name,

			"-f", DOCKER_FILE,
			".",
		],
		debug,
		)

	_run_command(['docker', 'push', docker_tag], debug)


def _run_command(command, debug):
	if debug:
		print(' '.join(command))
	else:
		try:
			result = subprocess.run(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, check = True)
		except subprocess.CalledProcessError as exc:
			print("Status : FAIL", exc.returncode, exc.output)
		else:
			print("Output: \n{}\n".format(output))
		