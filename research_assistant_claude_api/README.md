# Research Assistant Agent with Claude API

## Project Overview
This project creates a simple research assistant powered by the Claude API, which:
* Takes a topic of interest from the user along with a desired number of related articles
* Provides a list of relevant article titles based on the research topic
* Uses a custom tool (function) to verify availability of suggested topics on Wikipedia
* Returns matched articles with URLs
* Stores the research reading list in a structured Markdown format

## Key Components
* **main.py**: Core application logic and Claude API interactions
* **tools.py**: Definition of custom tools/functions for the agent
* **functions.py**: Helper functions for managing output and data processing

## Technical Implementation
The agent leverages the Claude API to generate relevant article topics, then connects to Wikipedia to validate and retrieve the actual articles, creating a curated reading list for research purposes.

## Skills & Knowledge Gained
* AI agent core principles when working with Claude API
* Tool definition and implementation for Claude client
* Prompt engineering for research assistance
* Python-based AI agent engineering
* Handling compatibility issues between libraries and Python versions

## Libraries Used
```
dotenv
anthropic
wikipedia
collections
```

## Note
This project was developed as part of the Anthropic course on [Claude API](https://github.com/anthropics/courses/blob/master/tool_use/02_your_first_simple_tool.ipynb). It demonstrates practical implementation of AI agent capabilities for research assistance tasks.