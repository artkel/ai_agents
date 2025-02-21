from dotenv import load_dotenv
import os
import pandas as pd
from llama_index.experimental.query_engine import PandasQueryEngine


load_dotenv()

population_path = os.path.join("data", "population.csv")
population_df = pd.read_csv(population_path)

print(population_df.head())

population_query_engine = PandasQueryEngine(df=population_df, verbose=True)


