from dotenv import load_dotenv
from anthropic import Anthropic
from tools import generate_wikipedia_reading_list, generate_reading_list


load_dotenv()
client = Anthropic()


def get_research_help(topic, num_articles, model):

    # Define prompts
    system_prompt = "You are a helpful research assistant, that gets a research topic of interest from user along with a number of relevant article topics. Your goal is to generate these topics in a required quantity. In your response give me only the topics as a list of strings."
    user_prompt = {"role": "user", "content": f"My topic of interest is {topic}, I need {num_articles} related article topics."}

    # Step 3: call model with tool
    response = client.messages.create(
        model=model,
        system=system_prompt,
        messages=[user_prompt],
        max_tokens=400,
        tools=[generate_reading_list]
    )
    research_topic = response.content[0].input['research_topic']
    article_titles = response.content[0].input['article_titles']

    return generate_wikipedia_reading_list(research_topic, article_titles)