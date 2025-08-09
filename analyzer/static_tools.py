import subprocess
from typing import List


def run_flake8(path: str) -> List[str]:
    """runs flake8 on the given path and returns an output of strings """

    result = subprocess.run(["flake8", path, "--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s"],
                            capture_output=True,
                            text=True
                            )
    
    # stdout = standard output
    
    # subprocess actually returns a class, in which you access stdout from

    if result.stdout:
        return result.stdout.strip().split("\n")
    else:
        return []
    
def run_pylint(path: str) -> List[str]:
    """runs pylint on the given path and returns an output of strings"""

    result = subprocess.run(["pylint", path, "-rn", "--output-format=text"],
                            capture_output=True,
                            text=True)
    
    if result.stdout:
        return result.stdout.strip().split("\n")
    else:
        return []
    


