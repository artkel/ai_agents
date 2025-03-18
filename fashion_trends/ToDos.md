## Challenges

* The main challenge right now is our search agent
* He adds unnecesary words in search queries no matter how I adjust the task instructions
* He often finds URLs where articles about trends are posted, or low quality articles
* Expand search list (now 10 results, should be at least 20)
* Make agent pick up different websites (URL versatility), also from lower part of the search results list
* Make agent to select search queries from a given list randomly
* Cost monitoring ```(specific_model_mln_tokens_price * (crew.usage_metrics_prompt_tokens + crew.usage_metrics.completion_tokens)```)

## Possible solution
* Add manager, who will be validating search agent output (see CrewAI course on DeepLearning platform)
* (what queries he used, what urls he provided)
* Develop a Flow
* Add human in the loop (check URL list before passing it to the next agent)
* Adjust instructions for the search agent, so that he only uses provided queries