from smell_detector.tools.custom_tool import CloneRepoTool

tool = CloneRepoTool()
result = tool.run(
    repo_url="https://github.com/nerdschoolbergen/code-smells",
    dest_dir="cloned_repo"
)

print(result)