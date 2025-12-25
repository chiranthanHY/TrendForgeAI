"""
Celery tasks for content generation
"""

from celery import current_task
import sys
import os
from datetime import datetime
import uuid

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.celery_app import celery_app
from src.engine.content_engine import ContentEngine
from api.database import SessionLocal
from api.models.models import Content, User

# Initialize content engine
engine = ContentEngine()

@celery_app.task(bind=True, name='generate_content')
def generate_content_task(self, topic: str, platform: str, product_info: str, user_email: str = "default@trendforgeai.com"):
    """
    Async task to generate marketing content
    
    Args:
        topic: Content topic
        platform: Platform (LinkedIn, YouTube, Twitter)
        product_info: Product information
        user_email: User email (defaults to demo user)
        
    Returns:
        dict: Generated content data
    """
    try:
        # Update task state to PROCESSING
        self.update_state(
            state='PROCESSING',
            meta={'status': 'Starting content generation...', 'progress': 10}
        )
        
        # Get database session
        db = SessionLocal()
        
        try:
            # Get or create user
            user = db.query(User).filter(User.email == user_email).first()
            if not user:
                user = User(
                    id=uuid.uuid4(),
                    email=user_email,
                    name="Default User",
                    hashed_password="not-used-yet"
                )
                db.add(user)
                db.commit()
                db.refresh(user)
            
            # Update progress
            self.update_state(
                state='PROCESSING',
                meta={'status': 'Retrieving style examples...', 'progress': 30}
            )
            
            # Run content generation pipeline
            result = engine.run_pipeline(
                topic=topic,
                platform=platform,
                product_info=product_info
            )
            
            if not result:
                raise Exception("Content generation failed - no result returned")
            
            # Update progress
            self.update_state(
                state='PROCESSING',
                meta={'status': 'Saving to database...', 'progress': 80}
            )
            
            # Save to database
            content = Content(
                id=uuid.uuid4(),
                user_id=user.id,
                topic=result['topic'],
                platform=result['platform'],
                product_info=product_info,
                final_content=result['final_content'],
                original_draft=result['original_draft'],
                quality_score=result['quality_score'],
                critique_notes=result['critique_notes'],
                status="draft",
                created_at=datetime.utcnow()
            )
            
            db.add(content)
            db.commit()
            db.refresh(content)
            
            # Return success
            return {
                'id': str(content.id),
                'topic': content.topic,
                'platform': content.platform,
                'final_content': content.final_content,
                'quality_score': content.quality_score,
                'critique_notes': content.critique_notes,
                'status': 'completed',
                'progress': 100
            }
            
        finally:
            db.close()
            
    except Exception as e:
        # Update task state to FAILURE
        self.update_state(
            state='FAILURE',
            meta={'status': f'Error: {str(e)}', 'progress': 0}
        )
        raise


@celery_app.task(bind=True, name='generate_multiple_variations')
def generate_multiple_variations_task(self, topic: str, platform: str, product_info: str, num_variations: int = 3, user_email: str = "default@trendforgeai.com"):
    """
    Generate multiple content variations
    
    Args:
        topic: Content topic
        platform: Platform
        product_info: Product info
        num_variations: Number of variations to generate
        user_email: User email
        
    Returns:
        list: List of generated content IDs
    """
    content_ids = []
    
    for i in range(num_variations):
        # Update progress
        progress = int((i / num_variations) * 100)
        self.update_state(
            state='PROCESSING',
            meta={'status': f'Generating variation {i+1}/{num_variations}...', 'progress': progress}
        )
        
        # Generate content
        result = generate_content_task(topic, platform, product_info, user_email)
        content_ids.append(result['id'])
    
    return {
        'content_ids': content_ids,
        'total': num_variations,
        'status': 'completed',
        'progress': 100
    }
