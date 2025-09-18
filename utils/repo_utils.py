import tempfile
import subprocess
from pathlib import Path


class RepoUtils:
    @staticmethod
    def clone_and_list(repo_url: str):
        """
        Clone a GitHub repo into a temp directory and return list of .py files.
        """
        temp_dir = tempfile.mkdtemp()
        subprocess.run(["git", "clone", repo_url, temp_dir], check=True)

        py_files = list(Path(temp_dir).rglob("*.py"))
        return py_files