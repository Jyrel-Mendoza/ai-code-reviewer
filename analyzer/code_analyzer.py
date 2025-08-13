import subprocess
from typing import List, Dict 
from .parser import flake8_parser_output, pylint_parser_output
from .static_tools import run_flake8, run_pylint


class CodeAnalyzer:
    """CodeAnalyzer is a class that receives a path, and subsequently run flake8, pylint, etc 
    to analyze that path."""
    def __init__(self, path="."):
        self.path = path

    def run_flake8(self):
        raw_output = run_flake8(self.path)  
        return flake8_parser_output(raw_output)   

    def run_pylint(self):
        raw_output = run_pylint(self.path)  
        return pylint_parser_output(raw_output) 

    def analyze(self) -> Dict[str, list]:
        return {
            "flake8": self.run_flake8(),
            "pylint": self.run_pylint()
        }