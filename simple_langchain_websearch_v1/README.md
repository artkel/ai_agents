# AI Agent with LangChain: JSON & Web Search Integration

## Overview
This project demonstrates the creation of an AI agent using LangChain framework that can seamlessly work with local JSON databases and perform web searches. It's my second project in the AI Agents learning journey, focusing on practical implementation of LangChain's capabilities.

## Features
- **Logging System**: Integrated logging functionality to track agent's actions and decisions
- **Local Database Access**: Efficient JSON data querying and analysis
- **Dual Search Capability**: Agent intelligently decides whether to search in local JSON database or on the web
- **Automatic Logging Functionality**: All relevant information is automatically preserved in log.txt

## Technologies Used
- LangChain Framework
- Python
- Components from langchain_community:
  - JsonToolkit
  - JsonSpec
  - create_json_agent
  - DuckDuckGoSearchRun

## Features in Detail
### JSON Database Tool
- Searches and analyzes local JSON files
- Handles both user and product data
- Performs complex queries and data analysis

### Web Search Tool
- Utilizes DuckDuckGo for web searches
- Provides up-to-date information when needed
- Complements local database information

### Logging System
- Records all agent actions and decisions
- Maintains a history of queries and responses
- Helps in debugging and monitoring

## Development Notes
- Built as part of AI Agents learning curriculum
- Utilized Claude AI for code formatting and optimization
- Focused on practical implementation of LangChain features

## Future Improvements
- Add more data sources
- Implement advanced filtering options
- Enhance logging capabilities
- Add error handling and recovery mechanisms

## Contributing
Feel free to fork this project and submit pull requests with improvements.

## License
This project is open source and available under the MIT License.