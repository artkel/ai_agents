from dotenv import load_dotenv
from anthropic import Anthropic
import json

load_dotenv()
client = Anthropic()

def translate(phrase: str):
    translate_tool = {
        "name": "translate",
        "description": "The tool translates a given English phrase or word into four different languages.",
        "input_schema": {
            "type": "object",
            "properties": {
                "english": {
                    "type": "string",
                    "description": "Provides original phrase in English."
                },
                "spanish": {
                    "type": "string",
                    "description": "Translates original phrase to Spanish."
                },
                "german": {
                    "type": "string",
                    "description": "Translates original phrase to German."
                },
                "French": {
                    "type": "string",
                    "description": "Translates original phrase to French."
                },
                "japanese": {
                    "type": "string",
                    "description": "Translates original phrase to Japanese."
                },
            },
            "required": ["english", "spanish", "german", "French", "Japanese"]
        }
    }

    # Step 2: define prompts
    system_prompt = "You are an experienced translator who can translate from English to Spanish, German, French, and Japanese."
    user_prompt = {"role": "user", "content": f"Translate '{phrase}' into four different languages."}

    # Step 3: call model with tool
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        system=system_prompt,
        messages=[user_prompt],
        max_tokens=200,
        tools=[translate_tool],
        tool_choice={"type": "tool", "name": "translate"}  # force agent to use the tool
    )

    # Get the model output (API response)
    tool_use_block = response.content[0]

    # Access the input dictionary
    tool_inputs = tool_use_block.input

    return print(json.dumps(tool_inputs, ensure_ascii=False, indent=2))


translate('How old are your parents?')
