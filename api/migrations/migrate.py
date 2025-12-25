"""
Database Migration Script for TrendForgeAI
Creates all necessary tables in PostgreSQL (Neon DB)
"""

import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.database import engine, Base
from api.models import (
    User,
    Content,
    ABTest,
    ABVariant,
    Metrics,
    SentimentAnalysis,
    CuratedExample
)

def create_tables():
    """Create all tables in the database"""
    print("Creating database tables...")
    
    try:
        # Create all tables
        Base.metadata.create_all(bind=engine)
        print("✅ Successfully created all tables:")
        print("  - users")
        print("  - content")
        print("  - ab_tests")
        print("  - ab_variants")
        print("  - metrics")
        print("  - sentiment_analysis")
        print("  - curated_examples")
        print("\nDatabase migration completed!")
        
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False
    
    return True

def drop_tables():
    """Drop all tables (use with caution!)"""
    print("⚠️  WARNING: This will drop all tables!")
    confirm = input("Type 'yes' to confirm: ")
    
    if confirm.lower() == 'yes':
        try:
            Base.metadata.drop_all(bind=engine)
            print("✅ All tables dropped successfully")
        except Exception as e:
            print(f"❌ Error dropping tables: {e}")
    else:
        print("Aborted.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Database Migration Script')
    parser.add_argument('action', choices=['create', 'drop'], help='Action to perform')
    
    args = parser.parse_args()
    
    if args.action == 'create':
        create_tables()
    elif args.action == 'drop':
        drop_tables()
