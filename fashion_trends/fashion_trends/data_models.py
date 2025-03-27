from pydantic import BaseModel, Field
from typing import Type, Optional, List



class SpiderCrawlerInput(BaseModel):
    url: str = Field(..., description="The URL of the fashion article to crawl")
    trend_name: str = Field(..., description="The exact name of the trend to extract from the article")
    chars_to_extract: int = Field(1000, description="Number of characters to extract after finding the trend")
    limit: int = Field(1, description="The number of pages to crawl")
    readability: bool = Field(True, description="Whether to extract the readable content")
    return_format: str = Field("markdown", description="The format to return the content in")

class FashionTrend(BaseModel):
    trend_name: str = Field(description="The exact name of the fashion trend as mentioned in the article")
    source_url: str = Field(description="URL of the article where the trend was found")

class FashionTrends(BaseModel):
    trends: List[FashionTrend] = Field(description="List of three verified fashion trends from different sources")

class BlocklistInput(BaseModel):
    """Input schema for BlocklistTool."""
    action: str = Field(..., description="Action to perform: 'check' or 'list'")
    url: Optional[str] = Field(None, description="URL to check against the blocklist")

class TrendDatabaseInput(BaseModel):
    """Input schema for TrendDatabaseTool."""
    action: str = Field(..., description="Action to perform: 'check', 'add', or 'list'")
    trend_name: Optional[str] = Field(None, description="Name of the trend to check or add")
    source_url: Optional[str] = Field(None, description="URL source for the trend")

class CrawlerToolInput(BaseModel):
    url: str = Field(..., description="URL of the article to crawl")
    trend_name: str = Field(..., description="Name of the trend to look for")

class CrawledTrendData(BaseModel):
    trend_title: str = Field(
        description="The exact title of the trend as it appears in the article"
    )
    description: str = Field(
        description="The complete description of the trend extracted verbatim from the article"
    )
    image_url: str = Field(
        description="URL of the most relevant image showing people/models wearing the trend"
    )
    source_url: str = Field(
        description="The original URL of the article where this trend was found"
    )

class CrawledTrends(BaseModel):
    trends: List[CrawledTrendData] = Field(
        description="Collection of trend data extracted from the articles"
    )

# class UltraMinimalInput(BaseModel):
#     url: str = Field(..., description="The URL of the fashion article to crawl")
#     trend_name: str = Field(..., description="The exact name of the trend to extract from the article")