from dotenv import load_dotenv
import os
import pandas as pd
import openai
from llama_index.llms.openai import OpenAI
from llama_index.experimental.query_engine import PandasQueryEngine
# from llama_index.core.query_engine import PandasQueryEngine
from prompts import new_prompt, instruction_str

load_dotenv()

population_path = os.path.join("data", "population.csv")
df = pd.read_csv(population_path)

# print(population_df.head())

llm = OpenAI(model="gpt-4o-mini")

population_query_engine = PandasQueryEngine(
                                df=df, 
                                verbose=True,
                                instruction_str=instruction_str,
                                llm=llm)

#population_query_engine.update_prompts({"pandas_prompt": new_prompt})
population_query_engine.query("Compare population in Australia in 2023 and 2024")




