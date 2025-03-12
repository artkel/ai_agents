import os
import yaml
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if required API keys are present
if not os.getenv("SERPER_API_KEY"):
    raise ValueError("SERPER_API_KEY environment variable is missing. Please add it to your .env file.")
if not os.getenv("ANTHROPIC_API_KEY"):
    raise ValueError("ANTHROPIC_API_KEY environment variable is missing. Please add it to your .env file.")

# Load configurations from YAML
def load_config(config_path):
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

# Load agents and tasks config
agents_config = load_config('config/agents.yaml')
tasks_config = load_config('config/tasks.yaml')

# Create a search tool - using SerperDev for more reliable results
search_tool = SerperDevTool()
image_search_tool = SerperDevTool()

# Create the trend researcher agent
trend_researcher = Agent(
    config=agents_config['trend_researcher'],
    tools=[search_tool],
    verbose=True
)

# Create the image curator agent
image_curator = Agent(
    config=agents_config['image_curator'],
    tools=[image_search_tool],
    verbose=True
)

# Define research task
research_task = Task(
    description=tasks_config['research_task']['description'],
    expected_output=tasks_config['research_task']['expected_output'],
    agent=trend_researcher
)

image_task = Task(
    description=tasks_config['image_curation_task']['description'],
    expected_output=tasks_config['image_curation_task']['expected_output'],
    agent=image_curator,
    context=[research_task]  # This connects the tasks by using the research output
)

fashion_crew = Crew(
        agents=[trend_researcher, image_curator],
        tasks=[research_task, image_task],
        process=Process.sequential,
        verbose=True
    )

# Run the crew
result = fashion_crew.kickoff()

# Save results
with open('complete_fashion_report.md', 'w') as f:
    f.write(str(result))
print(f"\nComplete report saved to: complete_fashion_report.md")

# # The image curation task will be defined after the research task runs
# # because it needs the research results as input
# # Create a unified crew with both agents and tasks
# if __name__ == "__main__":
#     print("Starting fashion trend analysis and image curation...")
#
#     fashion_crew = Crew(
#         agents=[trend_researcher, image_curator],
#         tasks=[research_task, image_task],
#         process=Process.sequential,
#         verbose=True
#     )
#
#     # Run the crew
#     result = fashion_crew.kickoff()
#
#     # Save results
#     with open('complete_fashion_report.md', 'w') as f:
#         f.write(str(result))
#     print(f"\nComplete report saved to: complete_fashion_report.md")