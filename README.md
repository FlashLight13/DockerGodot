![image](https://github.com/FlashLight13/DockerGodot/blob/main/logo/landscape.png?raw=true)

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/FlashLight13/DockerGodot/tree/main.svg?style=svg)](https://dl.circleci.com/status-badge/redirect/gh/FlashLight13/DockerGodot/tree/main)

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
