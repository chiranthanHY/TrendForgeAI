from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
import uuid
from datetime import datetime
from celery.result import AsyncResult

from ..database import get_db
from ..models.models import Content, User
from ..models.schemas import (
    ContentGenerateRequest,
    ContentResponse,
    ContentListResponse,
    ContentUpdateRequest,
    JobStatusResponse
)

# Import Celery tasks
from ..tasks.content_tasks import generate_content_task, generate_multiple_variations_task
from ..celery_app import celery_app

router = APIRouter()

def get_default_user(db: Session) -> UUID:
    """Get or create default user for testing"""
    # Use a consistent UUID for the default user
    DEFAULT_EMAIL = "default@trendforgeai.com"
    
    user = db.query(User).filter(User.email == DEFAULT_EMAIL).first()
    
    if not user:
        # Create default user
        user = User(
            id=uuid.uuid4(),
            email=DEFAULT_EMAIL,
            name="Default User",
            hashed_password="not-used-yet"  # TODO: Hash properly when auth is implemented
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user.id


@router.post("/generate", response_model=JobStatusResponse)
async def generate_content(
    request: ContentGenerateRequest,
    db: Session = Depends(get_db),
    use_async: bool = Query(True, description="Use async processing (Celery)")
):
    """
    Generate marketing content based on topic and platform
    
    Args:
        request: Content generation request
        use_async: If True, use Celery for async processing. If False, run synchronously.
    """
    try:
        if use_async:
            # Use Celery for async processing
            if request.num_variations > 1:
                # Generate multiple variations
                task = generate_multiple_variations_task.delay(
                    topic=request.topic,
                    platform=request.platform,
                    product_info=request.product_info,
                    num_variations=request.num_variations
                )
            else:
                # Generate single content
                task = generate_content_task.delay(
                    topic=request.topic,
                    platform=request.platform,
                    product_info=request.product_info
                )
            
            return JobStatusResponse(
                job_id=task.id,
                status="queued",
                progress=0,
                estimated_time=60 * request.num_variations  # Estimate 60s per variation
            )
        
        else:
            # Synchronous processing (for testing or when Celery is not available)
            from src.engine.content_engine import ContentEngine
            engine = ContentEngine()
            
            results = []
            
            for i in range(request.num_variations):
                result = engine.run_pipeline(
                    topic=request.topic,
                    platform=request.platform,
                    product_info=request.product_info
                )
                
                if result:
                    # Save to database
                    content = Content(
                        id=uuid.uuid4(),
                        user_id=get_default_user(db),
                        topic=result['topic'],
                        platform=result['platform'],
                        product_info=request.product_info,
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
                    
                    # Track and Alert via Slack
                    try:
                        from ..utils.slack import send_slack_notification
                        send_slack_notification(
                            f"✅ *New Content Generated*\n*Topic:* {result['topic']}\n*Platform:* {result['platform']}\n*Quality Score:* {result['quality_score']}/10",
                            username="TrendForgeAI Tracker"
                        )
                    except Exception as e:
                        print(f"Slack alert failed: {e}")
                    
                    results.append(content)
            
            # Return the first result
            if results:
                return JobStatusResponse(
                    job_id=str(results[0].id),
                    status="completed",
                    progress=100,
                    result=ContentResponse.from_orm(results[0])
                )
            else:
                raise HTTPException(status_code=500, detail="Content generation failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    db: Session = Depends(get_db)
):
    """
    Check the status of an async content generation job
    
    Args:
        job_id: Celery task ID
        
    Returns:
        Job status with progress and result if completed
    """
    try:
        # Get task result
        task = AsyncResult(job_id, app=celery_app)
        
        if task.state == 'PENDING':
            return JobStatusResponse(
                job_id=job_id,
                status="queued",
                progress=0
            )
        elif task.state == 'PROCESSING':
            # Get progress from task meta
            meta = task.info if task.info else {}
            return JobStatusResponse(
                job_id=job_id,
                status="processing",
                progress=meta.get('progress', 0)
            )
        elif task.state == 'SUCCESS':
            result = task.result
            
            # If result contains a content_id, fetch from database
            if isinstance(result, dict) and 'id' in result:
                content = db.query(Content).filter(Content.id == uuid.UUID(result['id'])).first()
                if content:
                    return JobStatusResponse(
                        job_id=job_id,
                        status="completed",
                        progress=100,
                        result=ContentResponse.from_orm(content)
                    )
            
            return JobStatusResponse(
                job_id=job_id,
                status="completed",
                progress=100
            )
        elif task.state == 'FAILURE':
            error = str(task.info) if task.info else "Unknown error"
            return JobStatusResponse(
                job_id=job_id,
                status="failed",
                progress=0,
                error=error
            )
        else:
            return JobStatusResponse(
                job_id=job_id,
                status=task.state.lower(),
                progress=0
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/history", response_model=ContentListResponse)
async def get_content_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    platform: str = Query(None),
    db: Session = Depends(get_db)
):
    """
    Get content generation history with pagination
    """
    # Build query
    user_id = get_default_user(db)
    query = db.query(Content).filter(Content.user_id == user_id)
    
    if platform:
        query = query.filter(Content.platform == platform)
    
    # Get total count
    total = query.count()
    
    # Apply pagination
    offset = (page - 1) * page_size
    items = query.order_by(Content.created_at.desc()).offset(offset).limit(page_size).all()
    
    return ContentListResponse(
        total=total,
        items=[ContentResponse.from_orm(item) for item in items],
        page=page,
        page_size=page_size
    )


@router.get("/{content_id}", response_model=ContentResponse)
async def get_content(
    content_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Get specific content by ID
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    return ContentResponse.from_orm(content)


@router.patch("/{content_id}", response_model=ContentResponse)
async def update_content(
    content_id: UUID,
    request: ContentUpdateRequest,
    db: Session = Depends(get_db)
):
    """
    Update content status or publish date
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    if request.status:
        content.status = request.status
    
    if request.published_at:
        content.published_at = request.published_at
    
    db.commit()
    db.refresh(content)
    
    return ContentResponse.from_orm(content)


@router.delete("/{content_id}")
async def delete_content(
    content_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Delete content by ID
    """
    content = db.query(Content).filter(Content.id == content_id).first()
    
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    
    db.delete(content)
    db.commit()
    
    return {"message": "Content deleted successfully"}


@router.post("/regenerate/{content_id}", response_model=JobStatusResponse)
async def regenerate_content(
    content_id: UUID,
    db: Session = Depends(get_db)
):
    """
    Regenerate content based on existing content's parameters
    """
    # Get original content
    original = db.query(Content).filter(Content.id == content_id).first()
    
    if not original:
        raise HTTPException(status_code=404, detail="Content not found")
    
    try:
        # Regenerate using original parameters
        result = engine.run_pipeline(
            topic=original.topic,
            platform=original.platform,
            product_info=original.product_info
        )
        
        if result:
            # Create new content entry
            content = Content(
                id=uuid.uuid4(),
                user_id=original.user_id,
                topic=result['topic'],
                platform=result['platform'],
                product_info=original.product_info,
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
            
            return JobStatusResponse(
                job_id=str(content.id),
                status="completed",
                progress=100,
                result=ContentResponse.from_orm(content)
            )
        else:
            raise HTTPException(status_code=500, detail="Content regeneration failed")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
