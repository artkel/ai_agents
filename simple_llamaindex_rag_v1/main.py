from dotenv import load_dotenv
import os
import pandas as pd
import openai
from llama_index.llms.openai import OpenAI
from llama_index.experimental.query_engine import PandasQueryEngine
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core.agent import ReActAgent
from note_engine import note_engine
from prompts import new_prompt, instruction_str, context
from pdf import germany_engine


load_dotenv()

population_path = os.path.join("data", "population.csv")
df = pd.read_csv(population_path)

llm = OpenAI(model="gpt-4o-mini")

population_query_engine = PandasQueryEngine(
                                df=df, 
                                verbose=True,
                                instruction_str=instruction_str,
                                llm=llm)

population_query_engine.update_prompts({"pandas_prompt": new_prompt})

# specify various tools the agent has an access to
tools = [
    note_engine,
    QueryEngineTool(
        query_engine=population_query_engine,
        metadata=ToolMetadata(
            name="population_data",
            description="this tool provides information about the world population & demographics"
        )
    ),
    QueryEngineTool(
        query_engine=germany_engine,
        metadata=ToolMetadata(
            name="germany_data",
            description="this tool provides detailed information about Germany the country"
    )
    )
]

agent = ReActAgent.from_tools(tools, llm=llm, verbose=True, context=context)

while (prompt := input("Enter a prompt (q to quit): ")) != "q":
    result = agent.query(prompt)
    print(result)