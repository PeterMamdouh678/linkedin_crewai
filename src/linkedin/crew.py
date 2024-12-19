from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

# If you want to run a snippet of code before or after the crew starts, 
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class Linkedin():
	"""Linkedin crew"""

	# Learn more about YAML configuration files here:
	# Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
	# Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	# If you would like to add tools to your agents, you can learn more about it here:
	# https://docs.crewai.com/concepts/agents#agent-tools

	@agent
	def research_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['research_agent'],
			tools=[SerperDevTool()],
			verbose=True
		)

	@agent
	def linkedin_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['linkedin_analyst'],
			verbose=True
		)
	
	@agent
	def content_writer(self) -> Agent:
		return Agent(
			config=self.agents_config['content_writer'],
			verbose=True
		)

	# To learn more about structured task outputs, 
	# task dependencies, and task callbacks, check out the documentation:
	# https://docs.crewai.com/concepts/tasks#overview-of-a-task
	@task
	def internet_research_task(self) -> Task:
		return Task(
			config=self.tasks_config['internet_research_task'],
			agent=self.research_agent(),
		)

	@task
	def linkedin_analysis_task(self) -> Task:
		return Task(
			config=self.tasks_config['linkedin_analysis_task'],
			agent=self.linkedin_analyst(),
			# output_file='report.md'
		)
	
	@task
	def content_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['content_creation_task'],
			agent=self.content_writer(),
			output_file='report.txt'
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the Linkedin crew"""
		# To learn how to add knowledge sources to your crew, check out the documentation:
		# https://docs.crewai.com/concepts/knowledge#what-is-knowledge

		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
