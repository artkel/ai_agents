from dotenv import load_dotenv
from anthropic import Anthropic
import json
import collections

# Provide backward compatibility for the package (To mitigate import error with Mappings)
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

import wikipedia

load_dotenv()
client = Anthropic()

# define tools
def get_article(search_term):
    results = wikipedia.search(search_term)
    first_result = results[0]
    page = wikipedia.page(first_result, auto_suggest=False)
    return page.content

article_search_tool = {
    "name": "get_article",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


def answer_question(question):
    system_prompt = """
        You are Claude, with extensive knowledge about general topics.
        IMPORTANT: Only use the get_article tool when you genuinely don't have the information needed to answer the question accurately with your existing knowledge.
        Common knowledge questions like animal facts, basic geography, history, and science should be answered directly without using tools.

        If answering the question requires data you were not trained on or involves very recent events, specific statistics, or obscure topics, you can use the get_article tool to get the contents of a Wikipedia article.

        You can make multiple tool calls if you need information about different subjects to fully answer a complex question.

        Examples of when NOT to use the tool:
        - "How many legs does an octopus have?"
        - "What is the capital of France?"
        - "Who wrote Romeo and Juliet?"

        Examples of when to use the tool:
        - "What were the key provisions in the 2023 AI Safety Act?"
        - "What is the current population of Liechtenstein?"
        - "Who won the most recent Olympic gold medal in rowing?"
        - "How many Oscars does Christopher Nolan have compared to Ben Stiller?" (This might require TWO tool calls)

        FINAL REMINDER: Answer directly from your knowledge whenever possible. Only use tools when absolutely necessary.
        IMPORTANT: Using the tool when it's not needed is inefficient and wastes resources. Only use the tool when you truly need additional information beyond what you already know.
        """

    print("Welcome to Research Assistant Chatbot! (Type 'exit' to quit)")
    print("---------------------------------------------------------")

    while True:
        question = input("\nYou: ")

        if question.lower() in ["exit", "quit", "bye"]:
            print("\nThank you for using Research Assistant Chatbot. Goodbye!")
            break

        prompt = f"""
            Answer the following question <question>{question}</question>
            When you can answer the question, keep your answer as short as possible.
            Remember: If you can answer the question without needing to get more information, please do so.
            """

        messages = [{"role": "user", "content": prompt}]

        # Loop to handle multiple tool calls if needed
        while True:
            response = client.messages.create(
                model="claude-3-haiku-20240307",
                messages=messages,
                system=system_prompt,
                max_tokens=1000,
                tools=[article_search_tool],
                tool_choice={"type": "auto"}
            )

            messages.append({"role": "assistant", "content": response.content})

            # Check if Claude wants to use a tool
            if response.stop_reason == "tool_use":
                # Process all tool calls in this response
                tool_calls_processed = False

                for content_item in response.content:
                    if hasattr(content_item, 'name') and content_item.name == "get_article":
                        tool_calls_processed = True
                        tool_id = content_item.id
                        search_term = content_item.input["search_term"]

                        print(f"Claude wants to get an article for: {search_term}")
                        wiki_result = get_article(search_term)

                        # Add the tool result to messages
                        tool_response = {
                            "role": "user",
                            "content": [
                                {
                                    "type": "tool_result",
                                    "tool_use_id": tool_id,
                                    "content": wiki_result
                                }
                            ]
                        }

                        messages.append(tool_response)

                # If no tool calls were processed, break the loop
                if not tool_calls_processed:
                    break
            else:
                # Claude didn't request any tools, we're done
                print("Claude's final answer:")
                print(response.content[0].text)
                break
