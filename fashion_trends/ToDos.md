# To-DO

we have a problem with crawl agent: she gets too much content for crawling, 
i.e. 1) high token consumption, 2) some models (gpt4) cannot digest the volume
I need to find out how to filter website content down before exposure (e.g. article title + 1000 characters after)

## Possible solutions:

1. try `css_extraction_map` by *Spider API*:
    json_data = {"limit":5,"return_format":"markdown","css_extraction_map":{"/blog":[{"name":"headers","selectors":["h1","h2","h3"]},{"name":"news","selectors":["article"]}]},"url":"https://spider.cloud"}

2. try [tavily extract](https://docs.tavily.com/documentation/api-reference/endpoint/extract) instead of *Spider*
particularily `"include_images": True` and `"extract_depth": Basic`
3. In Spider API try `filter_output_main_only: True`. Filter the nav, aside, and footer from the output.

@tru 
@solazola
@kait 