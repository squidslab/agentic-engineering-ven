from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from smell_detector.tools.custom_tool import CloneRepoTool
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class SmellDetector():
    """SmellDetector crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def github_reader(self) -> Agent:
        return Agent(
            config=self.agents_config['github_reader'], # type: ignore[index]
            tool=[CloneRepoTool()],
            verbose=True
        )

    @agent
    def code_smell_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config['code_smell_analyzer'], # type: ignore[index]
            verbose=True
        )
    
    @agent
    def report_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['report_generator'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def github_fetch_task(self) -> Task:
        return Task(
            config=self.tasks_config['github_fetch_task'], # type: ignore[index]
        )
    
    @task
    def smell_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['smell_analysis_task'], # type: ignore[index]
        )
    
    @task
    def report_generation_task(self) -> Task:
        return Task(
            config=self.tasks_config['report_generation_task'], # type: ignore[index]
            output_file='report.md'
        )
    


    @crew
    def crew(self) -> Crew:
        """Creates the SmellDetector crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
