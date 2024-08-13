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


    def get_safe_job_name(self):
        return self.job_name.replace('.', "_") 