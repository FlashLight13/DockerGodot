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

    def printable_version(self):
        return self.version + "-" + self.channel