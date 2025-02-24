import os
import json
import requests
from pydantic import BaseModel, Field
from openai import OpenAI, pydantic_function_tool

client = OpenAI(api_key="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")

# define data model
class GetWeather(BaseModel):
    location: str = Field(
        ...,
        description="City and country e.g. Bogotá, Colombia"
    )


# Step 1: Define get_weather tool and get the schema with pydantic_function_tool
def get_weather(latitude, longitude):
    """
    Retrieves current weather for the given Latitude & Longitude.
    """
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']

tools = pydantic_function_tool(GetWeather)

system_prompt = "You are a helpful weather assistant."

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's the weather like in Sacramento today?"}
]


# Step 2: Call model with get_weather tool defined
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=messages, # memory component
    tools=[tools]
)

# Step 3: model decides to call function(s) and provides parameters to do it
completion.model_dump()

# Step 4: Execute get_weather function (AI does not do it, it only provides parameters)
def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)

for tool_call in completion.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion.choices[0].message)

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )

print(result)

# Step 5: Supply result and call model again

class WeatherResponse(BaseModel): # provide data model for response structure consistency
    temperature: float = Field(
        description="The current temperature in celsius for the given location."
    )
    response: str = Field(
        description="A natural language response to the user's question."
    )


completion_2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages, # memory component
    tools=tools,
    response_format=WeatherResponse, # response structure from our defined data model
)

# Step 5: Check model response
final_response = completion_2.choices[0].message.parsed
final_response.temperature
print(final_response.response)