from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models.schemas import MetricsResponse, MetricItem, CampaignDataPoint, SlackAlert, SlackTestRequest, SlackTestResponse
from ..database import get_db
from ..models.models import Content
from ..config import settings
from ..utils.slack import send_slack_notification, send_slack_report
import random

router = APIRouter()

def get_current_metrics():
    """Helper to return current snapshot of metrics"""
    return [
        {"label": 'Total Reach', "value": f"{round(40 + random.random() * 10, 1)}K", "change": '+12%'},
        {"label": 'Engagement Rate', "value": f"{round(7.5 + random.random() * 2, 1)}%", "change": '+5.3%'},
        {"label": 'Conversions', "value": f"{random.randint(1100, 1400)}", "change": '+18%'},
        {"label": 'ROI', "value": f"{random.randint(310, 360)}%", "change": '+25%'}
    ]

@router.get("/", response_model=MetricsResponse)
async def get_metrics_data():
    """
    Get dynamic performance metrics and integration data
    """
    slack_status = "Connected" if settings.SLACK_WEBHOOK_URL else "Not Configured"
    metrics = get_current_metrics()
    
    return MetricsResponse(
        key_metrics=[
            MetricItem(label=m['label'], value=m['value'], change=m['change'], icon=i, color=c)
            for m, i, c in zip(metrics, ['Users', 'Heart', 'Target', 'DollarSign'], ['blue', 'pink', 'emerald', 'yellow'])
        ],
        campaign_performance=[
            CampaignDataPoint(label=str(i+1), value=random.randint(60, 100)) for i in range(12)
        ],
        slack_alerts=[
            SlackAlert(msg='Daily performance report scheduled', time='Just now', type='info'),
            SlackAlert(msg='New campaign reached 10K views', time='2m ago', type='success'),
            SlackAlert(msg='A/B test results ready', time='15m ago', type='info'),
            SlackAlert(msg='Low engagement alert', time='2h ago', type='warning')
        ],
        integration_status=[
            {"name": "Campaign Data", "status": "Synced"},
            {"name": "Engagement Metrics", "status": "Synced"},
            {"name": "Slack Bot", "status": slack_status},
            {"name": "A/B Test Results", "status": "Synced"}
        ]
    )

@router.post("/send-report", response_model=SlackTestResponse)
async def trigger_slack_report(db: Session = Depends(get_db)):
    """
    Send a comprehensive multi-module report to Slack
    """
    if not settings.SLACK_WEBHOOK_URL:
        raise HTTPException(status_code=400, detail="Slack Webhook URL is not configured")
    
    # 1. Collect Metrics
    metrics = get_current_metrics()
    
    # 2. Collect Sentiment (Dynamic/Mock)
    sentiment_data = {
        "score": round(7.0 + random.random() * 2.5, 1),
        "topics": random.sample(['AI Tech', 'Sustainability', 'Marketing', 'Remote Work', 'Web3'], 3),
        "viral": random.randint(85, 98)
    }
    
    # 3. Collect A/B Testing (Dynamic/Mock)
    ab_data = [
        {"name": "Headline Variation", "variantA": random.randint(60, 75), "variantB": random.randint(75, 90), "status": "running"},
        {"name": "CTA Button Color", "variantA": random.randint(70, 80), "variantB": random.randint(65, 75), "status": "running"}
    ]
    
    # 4. Collect Content History (Actual DB Query)
    content_history = db.query(Content).order_by(Content.created_at.desc()).limit(3).all()
    history_data = [
        {"platform": c.platform, "topic": c.topic, "score": c.quality_score} 
        for c in content_history
    ]
    
    # Combine into full report data
    report_data = {
        "metrics": metrics,
        "sentiment": sentiment_data,
        "ab_testing": ab_data,
        "content": history_data
    }
    
    success = send_slack_report("TrendForgeAI - Comprehensive Performance Intelligence", report_data)
    
    if success:
        return SlackTestResponse(success=True, message="Comprehensive report sent to Slack!")
    else:
        raise HTTPException(status_code=500, detail="Failed to send Slack report")

@router.post("/slack-test", response_model=SlackTestResponse)
async def test_slack(request: SlackTestRequest):
    """
    Send a test notification to Slack
    """
    if not settings.SLACK_WEBHOOK_URL:
        raise HTTPException(status_code=400, detail="Slack Webhook URL is not configured in credentials.py")
    
    success = send_slack_notification(request.message)
    if success:
        return SlackTestResponse(success=True, message="Test notification sent successfully!")
    else:
        raise HTTPException(status_code=500, detail="Failed to send Slack notification")
