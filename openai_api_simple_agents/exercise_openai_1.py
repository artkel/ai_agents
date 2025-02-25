import os
import json
import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from openai import OpenAI

load_dotenv()
client = OpenAI()

# Step 1: define get_weather tool
def get_weather(latitude, longitude):
    response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m")
    data = response.json()
    return data['current']

# OpenAI tool structure:
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather", # it is name of the tool function defined above
        "description": "Get current temperature for provided coordinates in celsius.",
        "parameters": {
            "type": "object",
            "properties": {
                "latitude": {"type": "number"},
                "longitude": {"type": "number"}
            },
            "required": ["latitude", "longitude"],
            "additionalProperties": False
        },
        "strict": True
    }
}]

# Step 2: Define your prompts
system_prompt = "You are a helpful weather assistant."
messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "What's the weather like in Bogota today?"}
]

# Step 3: Call model with get_weather tool defined
completion_1 = client.chat.completions.create(
    model="gpt-4o",
    messages=messages, # memory component
    tools=tools
)

# Step 4: model decides to use our get_weather tool and provides parameters to do it
completion_1.model_dump()


# Step 5: Execute get_weather function (AI does not do it, it only provides parameters)
def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)

for tool_call in completion_1.choices[0].message.tool_calls:
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    messages.append(completion_1.choices[0].message) # memory - storing all user's and agent's messages

    result = call_function(name, args)
    messages.append(
        {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result)}
    )

print(result)

# Step 6: Supply result and call model again
class WeatherResponse(BaseModel): # provide data model for response structure consistency
    temperature: float = Field(description="The current temperature in celsius for the given location.")
    response: str = Field(description="A natural language response to the user's question.")

completion_2 = client.beta.chat.completions.parse(
    model="gpt-4o",
    messages=messages, # memory component
    tools=tools,
    response_format=WeatherResponse # response structure from our defined data model
)

# Step 7: Check model response
final_response = completion_2.choices[0].message.parsed
final_response.temperature
print(final_response.response)