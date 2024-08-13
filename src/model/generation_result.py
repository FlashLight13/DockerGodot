class GenerationResult:

    def __init__(
        self,
        job_name,
        job,
        dependencies,
    ):
        self.job_name = job_name
        self.job = job
        self.dependencies = dependencies
    

    def __str__(self) -> str:
        return "[job_name=" + self.job_name + ", deps=" + str(self.dependencies) + "]"