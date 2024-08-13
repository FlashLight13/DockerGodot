class DockerCoordinates:

    def __init__(
        self,
        namespace,
        repository,
    ):
        self.namespace = namespace
        self.repository = repository

    def __str__(self):
        return self.path()

    def path(self):
        return self.namespace + "/" + self.repository
