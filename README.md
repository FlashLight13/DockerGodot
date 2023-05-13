![image](https://github.com/FlashLight13/DockerGodot/blob/main/logo/landscape.png?raw=true)

![CircleCI](https://img.shields.io/circleci/build/github/FlashLight13/DockerGodot/main)
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/flashlight13/godot)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/flashlight13/godot/4.0.2)

# Docker godot
Docker image to build  projects

Godot CI Docker Image
This Docker image contains everything you need to build and export [Godot Engine](https://godotengine.org/) games on with ubuntu base image. It includes Godot and it's corresponding export templates.

### Supported versions
https://hub.docker.com/r/flashlight13/godot/tags

# Getting Started

0) Make sure you're running it as a `root` user.
1) In your container:
```
FROM flashlight13/godot:<version> AS base

...

RUN  godot --headless --export-release ...
```
