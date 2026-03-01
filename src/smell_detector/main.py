#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from smell_detector.crew import SmellDetector
from smell_detector.tools.custom_tool import CloneRepoTool

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """
    inputs = {
        "repo_url": "https://github.com/nerdschoolbergen/code-smells",
    }


    try:
        # CloneRepoTool().run(repo_url=inputs["repo_url"])
        SmellDetector().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

