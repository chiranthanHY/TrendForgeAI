from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

# Request Schemas
class ContentGenerateRequest(BaseModel):
    topic: str = Field(..., description="Content topic or angle")
    platform: str = Field(..., description="Platform (LinkedIn, YouTube, Twitter)")
    product_info: str = Field(..., description="Product information")
    num_variations: int = Field(default=1, ge=1, le=5, description="Number of variations to generate")

class ContentUpdateRequest(BaseModel):
    status: Optional[str] = None
    published_at: Optional[datetime] = None

# Response Schemas
class ContentResponse(BaseModel):
    id: UUID
    user_id: UUID
    topic: str
    platform: str
    product_info: str
    final_content: str
    original_draft: Optional[str] = None
    quality_score: Optional[float] = None
    critique_notes: Optional[str] = None
    status: str
    created_at: datetime
    published_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class JobStatusResponse(BaseModel):
    job_id: str
    status: str  # queued, processing, completed, failed
    progress: int = 0
    result: Optional[ContentResponse] = None
    error: Optional[str] = None
    estimated_time: Optional[int] = None

class ContentListResponse(BaseModel):
    total: int
    items: list[ContentResponse]
    page: int
    page_size: int

# Sentiment & Trend Schemas
class SentimentTopic(BaseModel):
    topic: str
    change: str

class PlatformSentiment(BaseModel):
    platform: str
    sentiment: str
    score: float

class PredictedPerformance(BaseModel):
    label: str
    value: str
    progress: int

class SentimentResponse(BaseModel):
    sentiment_score: float
    trending_topics: list[SentimentTopic]
    viral_potential: int
    platform_reactions: list[PlatformSentiment]
    predicted_performance: list[PredictedPerformance]

# Performance Metrics Schemas
class MetricItem(BaseModel):
    label: str
    value: str
    change: str
    icon: str
    color: str

class CampaignDataPoint(BaseModel):
    value: int
    label: str

class SlackAlert(BaseModel):
    msg: str
    time: str
    type: str

class MetricsResponse(BaseModel):
    key_metrics: list[MetricItem]
    campaign_performance: list[CampaignDataPoint]
    slack_alerts: list[SlackAlert]
    integration_status: list[dict]

# A/B Testing Schemas
class ABTestVariant(BaseModel):
    name: str
    value: int

class ABTestItem(BaseModel):
    name: str
    variantA: int
    variantB: int
    status: str

class PerformanceForecastItem(BaseModel):
    label: str
    value: str
    confidence: Optional[str] = None

class TestResultHistory(BaseModel):
    name: str
    winner: str
    improvement: str
    date: str

class ABTestingResponse(BaseModel):
    active_tests: list[ABTestItem]
    recommendation: dict
    performance_forecast: list[PerformanceForecastItem]
    quick_insights: list[str]
    recent_results: list[TestResultHistory]
# Slack Integration Schemas
class SlackTestRequest(BaseModel):
    message: str = Field(default="Test notification from TrendForgeAI Dashboard!")

class SlackTestResponse(BaseModel):
    success: bool
    message: str
