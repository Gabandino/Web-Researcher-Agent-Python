from dotenv import load_dotenv
import os

load_dotenv()

from google_search_tools import GoogleSearchTool

tool = GoogleSearchTool()
query = "What is the capital of France?"
print("Running query: ", query)
print("--- Results ---")
print(tool.forward(query))
