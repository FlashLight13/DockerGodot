<img src="https://github.com/FlashLight13/DockerGodot/blob/main/logo/icon.png" width="20%"/>

![CircleCI](https://img.shields.io/circleci/build/github/FlashLight13/DockerGodot/main)
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/flashlight13/godot)
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/flashlight13/godot/4.0.2)

# Docker Godot
Docker image to build  projects

This Docker image contains everything you need to run [Godot Engine](https://godotengine.org/) inside a container. It includes Godot and it's corresponding export templates.
It may come in handy when setting up a CI or Godot server.

# Supported versions
https://hub.docker.com/r/flashlight13/godot/tags

# Getting Started
There're two primary usecases for this image:
1) Use it as a part of game CI pipeline
2) Run it directly to start godot

In any case, the first thing you have to do is to have [Docker](https://www.docker.com/) up and running.

### Starting point of your image
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
