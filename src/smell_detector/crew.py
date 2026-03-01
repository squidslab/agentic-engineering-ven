from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from smell_detector.tools.custom_tool import CloneRepoTool
from smell_detector.tools.custom_tool import ListRepoFilesTool
from smell_detector.tools.custom_tool import ReadRepoFileTool

@CrewBase
class SmellDetector():
    """SmellDetector crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


    @agent
    def repo_cloner(self) -> Agent:
        return Agent(
            config=self.agents_config['repo_cloner'],
            tools=[CloneRepoTool()],
            verbose=True,
            max_iter=3,
        )

    @agent
    def code_smell_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_smell_analyzer'], 
            tools=[ListRepoFilesTool(), ReadRepoFileTool()],
            verbose=True
        )
    
    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'], 
            verbose=True
        )
    
    @task
    def clone_repo_task(self) -> Task:
        return Task(
            config=self.tasks_config['clone_repo_task'],
        )
    
    @task
    def smell_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['smell_analysis_task'],
        )
    
    @task
    def report_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_generation_task'],
            output_file='report.md'
        )
    


    @crew
    def crew(self) -> Crew:
        """Creates the SmellDetector crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
