from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field



class CloneRepoToolInput(BaseModel):
    """Input schema for CloneRepoTool."""
    repo_url: str = Field(..., description="GitHub repository URL to clone.")
    dest_dir: str = Field("cloned_repo", description="Destination directory for the cloned repo.")


import os
from git import Repo

class CloneRepoTool(BaseTool):
    name: str = "Clone GitHub Repository"
    description: str = (
        "Clones a GitHub repository to a local directory and returns the path to the cloned repository. "
    )
    args_schema: Type[BaseModel] = CloneRepoToolInput

    def _run(self, repo_url: str, dest_dir: str = "cloned_repo") -> str:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
        Repo.clone_from(repo_url, dest_dir, depth=1)
        return os.path.abspath(dest_dir)

