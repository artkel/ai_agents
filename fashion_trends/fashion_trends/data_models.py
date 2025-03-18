from pydantic import BaseModel, Field
from typing import Type, Optional


# Custom Spider Crawler Tool
class SpiderCrawlerInput(BaseModel):
    url: str = Field(..., description="The URL of the fashion article to crawl")
    trend_name: str = Field(..., description="The exact name of the trend to extract from the article")
    chars_to_extract: int = Field(1000, description="Number of characters to extract after finding the trend")
    limit: int = Field(1, description="The number of pages to crawl")
    readability: bool = Field(True, description="Whether to extract the readable content")
    return_format: str = Field("markdown", description="The format to return the content in")


class UltraMinimalInput(BaseModel):
    url: str = Field(..., description="The URL of the fashion article to crawl")
    trend_name: str = Field(..., description="The exact name of the trend to extract from the article")