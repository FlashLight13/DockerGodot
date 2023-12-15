<img src="https://github.com/FlashLight13/DockerGodot/blob/main/logo/icon.png" width="20%"/>

![CircleCI](https://img.shields.io/circleci/build/github/FlashLight13/DockerGodot/release)
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/flashlight13/godot)

# Docker Godot
Docker image to use in the CI to build Godot projects

This Docker image contains everything you need to run [Godot Engine](https://godotengine.org/) inside a Docker container. It includes both engine and export templates ready for exporting

Instead of having a docker file for every image, this repo focuses on automatic support of every published godot version. It contains a CircleCI pipeline that crawls all existing versions and incrementally uploads images to the DockerHub. Each image uses the same Docker file located in images/godot.dockerfile.

# Supported versions
Provides all the versions starting with the Godot 3. A list of available images is available here:
https://hub.docker.com/r/flashlight13/godot/tags

# Getting Started
There're two primary usecases for this image:
1) Use it as a part of game CI pipeline
2) Run it directly to start godot

In any case, the first thing you have to do is to have [Docker](https://www.docker.com/) up and running.

### Using it in your CI image
0) Make sure you're running it as a `root` user.
1) In your container:
```
FROM flashlight13/godot:<version> AS base

...

RUN  godot ...
```
### Executable docker image
```
docker pull flashlight13/godot:<version>
docker run flashlight13/godot:<version>
```
