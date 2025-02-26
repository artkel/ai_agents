from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client = Anthropic()

# Step 1: Define tool

def calculator(operation, operand1, operand2):
    if operation == "add":
        return operand1 + operand2
    elif operation == "subtract":
        return operand1 - operand2
    elif operation == "multiply":
        return operand1 * operand2
    elif operation == "divide":
        if operand2 == 0:
            raise ValueError("Cannot divide by zero.")
        return operand1 / operand2
    else:
        raise ValueError(f"Unsupported operation: {operation}")

# Claude tool structure:
calculator_tool = {
    "name": "calculator",
    "description": "Simple calculator that performs basic arithmetic operations [such as add, subtract, multiply, divide] with two operands (operand1 & operand2)",
    "input_schema": {
        "type": "object",
        "properties": {
            "operation": {
                "type": "string",
                "enum": ["add", "subtract", "multiply", "divide"],
                "description": "The arithmetic operation to perform between two operands."
            },
            "operand1": {
                "type": "number",
                "description": "First operand for arithmetic operation."
            },
            "operand2": {
                "type": "number",
                "description": "Second operand for arithmetic operation."
            }
        },
        "required": ["operation", "operand1", "operand2"]
    }
}

# Step 2: define prompts
system_prompt = "You have access to tools, but only use them when necessary.  If a tool is not required, respond as normal."
user_prompt = {"role": "user", "content": "Multiply 1984135 by 9343116. Only respond with the result."}

# Step 3: call model with tool
response = client.messages.create(
    model="claude-3-haiku-20240307",
    system=system_prompt,
    messages=[user_prompt],
    max_tokens=200,
    tools=[calculator_tool]
)

# Step 4: Get tool inputs
tool_name = response.content[0].name
operand1 = response.content[0].input['operand1']
operand2 = response.content[0].input['operand2']
operation = response.content[0].input['operation']

# Step 5: put inputs into the tool to get result
result = calculator(operation, operand1, operand2)
# print(result)

# Test with not math-related query (no tool required)
response = client.messages.create(
    model="claude-3-haiku-20240307",
    system=system_prompt,
    messages=[{"role": "user", "content": "What color are emeralds?"}],
    max_tokens=200,
    tools=[calculator_tool]
)

print(response.content[0].text)