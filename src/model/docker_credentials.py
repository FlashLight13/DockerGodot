class DockerCredentials:

    def __init__(
        self,
        login_env,
        pass_env,
    ):
        self.login_env = login_env
        self.pass_env = pass_env
