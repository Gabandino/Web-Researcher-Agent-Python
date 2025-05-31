# Let's define a web_researcher agent using our google_search_tools toolspec
# Importing required libraries/modules
import os
from dotenv import load_dotenv
from smolagents import (
    ToolCallingAgent,
    OpenAIServerModel,
)
from google_search_tools import GoogleSearchTool, GoogleSiteSearchTool

#load environment variables
load_dotenv()

# 1. Define LLM our agent will use
model = OpenAIServerModel(model_id='gpt-3.5-turbo')

# 2. Instantiate both search tools
general_google_search_tool = GoogleSearchTool()
site_search_tool = GoogleSiteSearchTool()

# 3. Wrap both GoogleSearchTools in a ToolCallingAgent
web_researcher_agent = ToolCallingAgent(
    name='web_researcher',
    description='Answers questions that require grounding in unknown information through search on web sites and other online resources.',
    tools=[general_google_search_tool, site_search_tool],
    model=model,
    planning_interval=1,
    max_steps=9,
)

# 4. Run test queries (you may delete this after testing the agent's functionality)
if __name__ == '__main__':
    question_1 = "Reddit says GPT-4 hallucinates less, but arxiv papers say otherwise. Who’s right?"
    # question_2 = "How to know if my dog likes its food?"

    print(f"\n📥 Question 1:\n{question_1}")
    answer_1 = web_researcher_agent.run(question_1)
    print("\n📤 Final Answer 1:")
    print(answer_1)

    # print(f"\n📥 Question 2:\n{question_2}")
    # answer_2 = web_researcher_agent.run(question_2)
    # print("\n📤 Final Answer 2:")
    # print(answer_2)