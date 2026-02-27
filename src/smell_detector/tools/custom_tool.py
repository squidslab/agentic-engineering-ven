from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import os
from git import Repo


# ── Clone ──────────────────────────────────────────────────────────────────────
class CloneRepoToolInput(BaseModel):
    """Input schema for CloneRepoTool."""
    repo_url: str = Field(..., description="GitHub repository URL to clone.")
    dest_dir: str = Field("cloned_repo", description="Destination directory for the cloned repo.")

class CloneRepoTool(BaseTool):
    name: str = "Clone GitHub Repository"
    description: str = (
        "Clones a GitHub repository to a local directory and returns the path to the cloned repository. "
    )
    args_schema: Type[BaseModel] = CloneRepoToolInput

    def _run(self, repo_url: str, dest_dir: str = "cloned_repo") -> str:
        import shutil
        if os.path.exists(dest_dir):
            shutil.rmtree(dest_dir)
        try:
            Repo.clone_from(repo_url, dest_dir, depth=1)
            return f"SUCCESS: cloned into {os.path.abspath(dest_dir)}"
        except Exception as e:
            return f"ERROR: {str(e)}"
# ── List files ─────────────────────────────────────────────────────────────────
class ListRepoFilesInput(BaseModel):
    repo_dir: str = Field("cloned_repo", description="Path to the cloned repo.")
    extensions: str = Field(
        ".java,.py,.js,.ts,.cs,.cpp,.c",
        description="Comma-separated list of file extensions to include."
    )

class ListRepoFilesTool(BaseTool):
    name: str = "List Repository Files"
    description: str = (
        "Lists all source code files in the cloned repository. "
        "Use this FIRST to discover which files exist before reading them."
    )
    args_schema: Type[BaseModel] = ListRepoFilesInput

    def _run(self, repo_dir: str = "cloned_repo", extensions: str = ".java,.py,.js,.ts,.cs,.cpp,.c") -> str:
        if not os.path.exists(repo_dir):
            return f"ERROR: Repository directory '{repo_dir}' does not exist. Please clone the repository first."
        
        exts = tuple(e.strip() for e in extensions.split(","))
        found = []
        for root, dirs, files in os.walk(repo_dir):
            dirs[:] = [d for d in dirs if not d.startswith('.')]
            for fname in files:
                if fname.endswith(exts):
                    rel = os.path.relpath(os.path.join(root, fname), repo_dir)
                    found.append(rel)
        
        if not found:
            return "No source files found."
        return "\n".join(found)
# ── Read file ──────────────────────────────────────────────────────────────────
class ReadRepoFileInput(BaseModel):
    file_path: str = Field(..., description="Relative path of the file inside the cloned repo.")
    repo_dir: str = Field("cloned_repo", description="Path to the cloned repo root.")

class ReadRepoFileTool(BaseTool):
    name: str = "Read Repository File"
    description: str = (
        "Reads and returns the full content of a source file in the cloned repository."
        "Use the relative path returned by 'List Repository Files'."
    )
    args_schema: Type[BaseModel] = ReadRepoFileInput

    def _run(self, file_path: str, repo_dir: str = "cloned_repo") -> str:
        full_path = os.path.join(repo_dir, file_path)
        if not os.path.exists(full_path):
            return f"ERROR: file '{file_path}' not found."
        try:
            with open(full_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            max_chars = 10000
            if len(content) > max_chars:
                content = content[:max_chars] + f"\n\n[... truncated at {max_chars} chars ...]"
            return content
        except Exception as e:
            return f"ERROR reading file: {e}"