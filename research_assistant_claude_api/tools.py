import collections.abc
import collections


# Provide backward compatibility for the package (To mitigate import error with Mappings)
if not hasattr(collections, 'Mapping'):
    collections.Mapping = collections.abc.Mapping
if not hasattr(collections, 'MutableMapping'):
    collections.MutableMapping = collections.abc.MutableMapping
if not hasattr(collections, 'Callable'):
    collections.Callable = collections.abc.Callable

import wikipedia

# Define tool
def generate_wikipedia_reading_list(research_topic, article_titles):
    wikipedia_articles = []
    for t in article_titles:
        results = wikipedia.search(t)
        try:
            page = wikipedia.page(results[0])
            title = page.title
            url = page.url
            wikipedia_articles.append({"title": title, "url": url})
        except:
            continue
    add_to_research_reading_file(wikipedia_articles, research_topic)

def add_to_research_reading_file(articles, topic):
    with open("output/research_reading.md", "a", encoding="utf-8") as file:
        file.write(f"## {topic} \n")
        for article in articles:
            title = article["title"]
            url = article["url"]
            file.write(f"* [{title}]({url}) \n")
        file.write(f"\n\n")


# Claude tool structure:
generate_reading_list = {
    "name": "generate_wikipedia_reading_list",
    "description": "The tool connects to the real Wikipedia API and generates a list of URLs of real Wiki articles for a given research topic.",
    "input_schema": {
        "type": "object",
        "properties": {
            "research_topic": {
                "type": "string",
                "description": "The research topic of interest provided by user."
            },
            "article_titles": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "List of a certain number of article titles that might be relevant for the given research topic."
            }
        },
        "required": ["research_topic", "article_titles"]
    }
}