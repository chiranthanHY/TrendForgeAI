from fastapi import APIRouter
from ..models.schemas import ABTestingResponse, ABTestItem, PerformanceForecastItem, TestResultHistory
import random

router = APIRouter()

@router.get("/", response_model=ABTestingResponse)
async def get_ab_testing_data():
    """
    Get dynamic A/B testing and prediction coach data
    """
    insights_pool = [
        "Best posting time: 2-4 PM EST",
        "Optimal content length: 150-200 words",
        "Include 2-3 relevant hashtags",
        "Video content performs 2x better",
        "Engagement peaks on Tuesdays",
        "User testimonials increase CTR by 15%",
        "Emoji usage improves open rates"
    ]
    
    return ABTestingResponse(
        active_tests=[
            ABTestItem(name='Headline Variation Test', variantA=random.randint(60, 75), variantB=random.randint(75, 90), status='running'),
            ABTestItem(name='CTA Button Color', variantA=random.randint(70, 80), variantB=random.randint(65, 75), status='running'),
            ABTestItem(name='Image Style Test', variantA=88, variantB=85, status='completed')
        ],
        recommendation={
            "title": "Recommendation",
            "content": f"Based on current trends, Variant B is predicted to outperform by {random.randint(10, 20)}% in the next 48 hours."
        },
        performance_forecast=[
            PerformanceForecastItem(label="Expected CTR", value=f"{round(3.5 + random.random() * 1.5, 1)}%"),
            PerformanceForecastItem(label="Predicted Conversions", value=f"+{random.randint(250, 450)}"),
            PerformanceForecastItem(label="Confidence Level", value=f"{random.randint(80, 95)}%")
        ],
        quick_insights=random.sample(insights_pool, 3),
        recent_results=[
            TestResultHistory(
                name='Email Subject Line', 
                winner=random.choice(['Variant A', 'Variant B']), 
                improvement=f"+{random.randint(15, 35)}%", 
                date='Dec 25'
            ),
            TestResultHistory(
                name='Landing Page Layout', 
                winner=random.choice(['Variant A', 'Variant B']), 
                improvement=f"+{random.randint(10, 25)}%", 
                date='Dec 23'
            ),
            TestResultHistory(
                name='Ad Copy Test', 
                winner=random.choice(['Variant A', 'Variant B']), 
                improvement=f"+{random.randint(20, 40)}%", 
                date='Dec 20'
            )
        ]
    )
