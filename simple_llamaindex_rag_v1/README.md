# simple_llama_index_rag_v1

## Overview
This is my first AI Agents project using the **LlamaIndex** framework to enable an agent to retrieve information from structured and unstructured data sources. The project explores fundamental AI Agent concepts, such as **Agent-Tool Interaction, RAG (Retrieval-Augmented Generation), Vector Storage, System Instructions, and Prompt Templating**.

The project inspired by **Tech by Tim** YT Video: https://youtu.be/ul0QsodYct4?si=MRjvvN1f5lHuUdc1

## Features
- **PDF Retrieval**: The agent was designed to extract information from a Wikipedia PDF about Germany using **VectorStoreIndex** and **PDFReader** from LlamaIndex.
- **CSV Querying**: The agent can query a **World Population Dataset** (sourced from Kaggle) via **PandasQueryEngine** and **pandas**.
- **GPT-4o-mini Model**: The agent is powered by OpenAI's **GPT-4o-mini** model.
- **Note-Taking Tool**: A custom tool allows the agent to store notes in a text file using LlamaIndex's **FunctionTool**.

## Challenges
- While the agent successfully interacted with the CSV and note-taking tool, it failed to properly retrieve and utilize information from the PDF, despite user prompts explicitly directing it to do so.

## Learnings
This project was a hands-on exploration of AI Agent fundamentals, focusing on:
- Agent-Tool interaction
- RAG methodology
- Vector storage
- System instruction tuning
- Prompt templating

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/artkel/ai_agents.git
   cd ai_agents/simple_llama_index_rag_v1
   ```
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv ai
   source ai/bin/activate  # (Windows: ai\Scripts\activate, if not working, try cmd - ai\Scripts\activate.bat)
   pip install -r requirements.txt
   ```
3. Set up your **OpenAI API key** in a `.env` file:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the main script:
   ```bash
   python main.py
   ```

## Future Improvements
- Debug PDF retrieval issues to ensure proper document-based responses.
- Experiment with additional tools to enhance the agent’s reasoning and retrieval abilities.
- Optimize prompt templates and system instructions for better performance.

---
This project serves as my first step into AI Agents, providing hands-on experience in integrating external knowledge sources and tools into an LLM-powered system.

