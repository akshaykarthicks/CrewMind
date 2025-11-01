from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Crewmind():
    """Goal Tracker Crew - Helps users set goals and create actionable schedules"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'
   
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def goal_tracker_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['goal_tracker_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def planner_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['planner_agent'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def goal_setting_task(self) -> Task:
        return Task(
            config=self.tasks_config['goal_setting_task'], # type: ignore[index]
        )

    @task
    def progress_monitoring_task(self) -> Task:
        return Task(
            config=self.tasks_config['progress_monitoring_task'], # type: ignore[index]
        )

    @task
    def weekly_schedule_task(self) -> Task:
        return Task(
            config=self.tasks_config['weekly_schedule_task'], # type: ignore[index]
        )

    @task
    def daily_planning_task(self) -> Task:
        return Task(
            config=self.tasks_config['daily_planning_task'], # type: ignore[index]
            output_file='daily_plan.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Goal Tracker Crew"""
        # Goal Tracker Crew: Two agents working together to help users achieve their goals
        # 🎯 Goal Tracker Agent - Sets and monitors goals
        # 📅 Planner Agent - Creates schedules and daily plans

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
