from fastapi import APIRouter
from ..models.schemas import SentimentResponse, SentimentTopic, PlatformSentiment, PredictedPerformance
import random
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=SentimentResponse)
async def get_sentiment_data():
    """
    Get dynamic sentiment and trend analysis data
    """
    # Simulate dynamic data
    topics = ['AI Technology', 'Sustainability', 'Digital Marketing', 'Remote Work', 'Web3', 'Creator Economy']
    random.shuffle(topics)
    
    return SentimentResponse(
        sentiment_score=round(7.0 + random.random() * 2.5, 1),
        trending_topics=[
            SentimentTopic(topic=topics[0], change=f"↑ {random.randint(80, 95)}%"),
            SentimentTopic(topic=topics[1], change=f"↑ {random.randint(70, 85)}%"),
            SentimentTopic(topic=topics[2], change=f"↑ {random.randint(60, 75)}%"),
            SentimentTopic(topic=topics[3], change=f"↑ {random.randint(50, 65)}%")
        ],
        viral_potential=random.randint(85, 98),
        platform_reactions=[
            PlatformSentiment(platform="LinkedIn", sentiment="Positive", score=8.7),
            PlatformSentiment(platform="Twitter", sentiment="Neutral", score=7.2),
            PlatformSentiment(platform="Facebook", sentiment="Positive", score=8.1),
            PlatformSentiment(platform="Instagram", sentiment="Very Positive", score=9.3)
        ],
        predicted_performance=[
            PredictedPerformance(label="Expected Engagement", value=f"+{random.randint(30, 50)}%", progress=75),
            PredictedPerformance(label="Predicted Reach", value=f"{random.randint(10, 15)}K", progress=85),
            PredictedPerformance(label="Conversion Rate", value=f"{round(3.0 + random.random(), 1)}%", progress=65)
        ]
    )
