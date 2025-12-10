import pandas as pd
import json
import os
import re

import google.generativeai as genai
import time
import sys

# Add project root to path to import credentials
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

try:
    from credentials import GEMINI_API_KEY
    genai.configure(api_key=GEMINI_API_KEY)
except ImportError:
    print("Warning: GEMINI_API_KEY not found. Embeddings will be skipped.")
    GEMINI_API_KEY = None

def clean_text(text):
    """Removes URLs and excessive whitespace from text."""
    if not isinstance(text, str):
        return ""
    # Remove URLs
    text = re.sub(r'http\S+', '', text)
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_embedding(text):
    """Generates embedding for a given text using Gemini API."""
    if not GEMINI_API_KEY or not text:
        return None
    try:
        # Using text-embedding-004
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=text,
            task_type="retrieval_document",
            title="Viral Post Example"
        )
        time.sleep(0.5) # Rate limit protection
        return result['embedding']
    except Exception as e:
        print(f"  x Error generating embedding: {e}")
        return None

def curate_linkedin_data(filepath):
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found.")
        return []
    
    try:
        df = pd.read_csv(filepath)
        # Ensure numeric
        df['total_engagement'] = pd.to_numeric(df['total_engagement'], errors='coerce').fillna(0)
        
        # Sort by engagement
        df_sorted = df.sort_values(by='total_engagement', ascending=False)
        
        # Take top 10% or at least top 10
        top_n = max(10, int(len(df) * 0.1))
        top_posts = df_sorted.head(top_n)
        
        examples = []
        print(f"   Generating embeddings for {len(top_posts)} LinkedIn posts...")
        for _, row in top_posts.iterrows():
            cleaned = clean_text(row['post_text'])
            if len(cleaned) > 50: # Filter out very short posts
                embedding = get_embedding(cleaned)
                if embedding:
                    examples.append({"text": cleaned, "embedding": embedding})
        
        print(f"✓ Curated {len(examples)} high-performing LinkedIn posts with embeddings.")
        return examples
    except Exception as e:
        print(f"Error processing LinkedIn data: {e}")
        return []

def curate_youtube_data(filepath):
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found.")
        return []
    
    try:
        df = pd.read_csv(filepath)
        # Create a composite engagement score
        # Views are common, likes/comments are high signal
        df['view_count'] = pd.to_numeric(df['view_count'], errors='coerce').fillna(0)
        df['like_count'] = pd.to_numeric(df['like_count'], errors='coerce').fillna(0)
        df['comment_count'] = pd.to_numeric(df['comment_count'], errors='coerce').fillna(0)
        
        df['engagement_score'] = df['view_count'] * 0.1 + df['like_count'] * 10 + df['comment_count'] * 20
        
        df_sorted = df.sort_values(by='engagement_score', ascending=False)
        
        top_n = max(10, int(len(df) * 0.1))
        top_videos = df_sorted.head(top_n)
        
        examples = []
        print(f"   Generating embeddings for {len(top_videos)} YouTube videos...")
        for _, row in top_videos.iterrows():
            title = clean_text(row['title'])
            desc = clean_text(row['description'])
            # Combine title and description for a full context example
            full_text = f"Title: {title}\nDescription: {desc[:500]}..." # Truncate desc if too long
            
            embedding = get_embedding(full_text)
            if embedding:
                examples.append({"text": full_text, "embedding": embedding})
            
        print(f"✓ Curated {len(examples)} high-performing YouTube video scripts/descriptions with embeddings.")
        return examples
    except Exception as e:
        print(f"Error processing YouTube data: {e}")
        return []

def curate_twitter_data(filepath):
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found. Skipping Twitter.")
        return []
    
    try:
        df = pd.read_csv(filepath)
        # Assuming columns like 'favorite_count', 'retweet_count', 'text'
        # Adjust based on actual extractor if needed, but standard is usually these
        if 'favorite_count' not in df.columns:
            # Fallback if columns are different
            if 'likes' in df.columns:
                 df['favorite_count'] = df['likes']
            if 'retweets' in df.columns:
                 df['retweet_count'] = df['retweets']
            
            if 'favorite_count' not in df.columns:
                 print("Twitter CSV missing engagement columns.")
                 return []

        df['score'] = df['favorite_count'] + df.get('retweet_count', 0) * 2
        df_sorted = df.sort_values(by='score', ascending=False)
        
        top_n = max(10, int(len(df) * 0.1))
        top_tweets = df_sorted.head(top_n)
        
        examples = []
        print(f"   Generating embeddings for {len(top_tweets)} Tweets...")
        for _, row in top_tweets.iterrows():
            cleaned = clean_text(row['text'])
            embedding = get_embedding(cleaned)
            if embedding:
                examples.append({"text": cleaned, "embedding": embedding})
            
        print(f"✓ Curated {len(examples)} high-performing Tweets with embeddings.")
        return examples
    except Exception as e:
        print(f"Error processing Twitter data: {e}")
        return []

def get_trending_topics(filepath):
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found.")
        return []
    
    try:
        df = pd.read_csv(filepath)
        # Assuming 'query' column from Google Trends related queries
        if 'query' in df.columns:
            return df['query'].head(20).tolist()
        elif 'top_query' in df.columns:
             return df['top_query'].head(20).tolist()
        elif 'keyword_searched' in df.columns: # Fallback
             return df['keyword_searched'].unique().tolist()
        return []
    except Exception as e:
        print(f"Error processing Trends data: {e}")
        return []

if __name__ == "__main__":
    print("--- Starting Data Curation for Content Engine ---")
    
    # Locate data directory relative to this script (src/engine/ -> ../../data)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.abspath(os.path.join(script_dir, "..", "..", "data"))
    
    print(f"Looking for data in: {data_dir}")
    
    data = {
        "linkedin_best": curate_linkedin_data(os.path.join(data_dir, "linkedin_product_marketing_posts.csv")),
        "youtube_best": curate_youtube_data(os.path.join(data_dir, "youtube_product_marketing_videos.csv")),
        "twitter_best": curate_twitter_data(os.path.join(data_dir, "product_marketing_tweets.csv")),
        "trending_topics": get_trending_topics(os.path.join(data_dir, "google_trends_related_queries.csv"))
    }
    
    output_file = os.path.join(data_dir, "top_performing_examples.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"\n✓ 'Fine-Tuning' Dataset saved to: {output_file}")
    print(f"  - LinkedIn Examples: {len(data['linkedin_best'])}")
    print(f"  - YouTube Examples: {len(data['youtube_best'])}")
    print(f"  - Twitter Examples: {len(data['twitter_best'])}")
    print(f"  - Trending Topics: {len(data['trending_topics'])}")
    print("--- Curation Complete ---")
