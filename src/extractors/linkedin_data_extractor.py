import pandas as pd
from datetime import datetime, timedelta
import time
import random
import os
from linkedin_api import Linkedin

# --- 1. Load API Credentials from credentials.py ---
try:
    from credentials import LINKEDIN_EMAIL, LINKEDIN_PASSWORD
except ImportError:
    print("Error: LinkedIn credentials not found in credentials.py. Please add LINKEDIN_EMAIL and LINKEDIN_PASSWORD.")
    exit()

# --- 2. Initialize LinkedIn API Client ---
try:
    api = Linkedin(LINKEDIN_EMAIL, LINKEDIN_PASSWORD)
    print("Successfully authenticated to LinkedIn API")
except Exception as e:
    print(f"Failed to authenticate to LinkedIn: {e}")
    print("Please ensure your credentials are correct and 2FA is disabled or configured properly.")
    exit()

# --- 3. Define Search Parameters ---
# Companies to monitor (LinkedIn public IDs or company names)
TARGET_COMPANIES = [
    "microsoft",
    "google",
    "apple",
    "tesla",
    "openai",
    "meta",
    "amazon",
    "nvidia",
    "ibm",
    "salesforce"
]

# Search terms for product-related content
LINKEDIN_PRODUCT_SEARCH_TERMS = [
    "new product launch",
    "product update",
    "innovation",
    "AI technology",
    "machine learning",
    "digital transformation",
    "tech trends",
    "product announcement",
    "new feature",
    "technology release"
]

POSTS_PER_COMPANY = 10  # How many recent posts to fetch per company
DAYS_BACK = 7  # How far back to look for posts

def get_linkedin_product_posts(companies, search_terms, posts_limit=POSTS_PER_COMPANY, days_back=DAYS_BACK):
    """
    Fetches product-centric posts from specified LinkedIn companies and performs keyword searches.
    """
    all_posts_data = []
    seen_post_ids = set()  # To prevent duplicate posts
    
    print(f"Starting LinkedIn data extraction...")
    print(f"Looking back {days_back} days for content\n")
    
    # Calculate cutoff date
    cutoff_date = datetime.now() - timedelta(days=days_back)
    
    # --- Fetch from specific companies ---
    print("Fetching posts from target companies...")
    for company_name in companies:
        print(f"  Processing: {company_name}")
        try:
            # Get company URN/ID
            company_info = api.get_company(company_name)
            
            if not company_info:
                print(f"    Could not find company: {company_name}")
                continue
            
            # Fetch company posts
            company_posts = api.get_company_updates(
                public_id=company_name,
                max_results=posts_limit
            )
            
            if company_posts:
                added = 0
                for post in company_posts:
                    post_data = extract_post_data(post, f"company:{company_name}", cutoff_date)
                    if post_data and post_data['post_id'] not in seen_post_ids:
                        all_posts_data.append(post_data)
                        seen_post_ids.add(post_data['post_id'])
                        added += 1
                
                print(f"    Added {added} posts")
            else:
                print(f"    No posts found")
            
            # Be polite with rate limiting
            time.sleep(random.randint(3, 6))
            
        except Exception as e:
            print(f"    Error fetching from {company_name}: {e}")
    
    # --- Perform keyword searches ---
    print("\nPerforming keyword searches...")
    for term in search_terms:
        print(f"  Searching for: '{term}'")
        try:
            # Search for posts containing the term
            search_results = api.search_posts(
                keywords=term,
                limit=15
            )
            
            if search_results:
                added = 0
                for post in search_results:
                    post_data = extract_post_data(post, f"search:'{term}'", cutoff_date)
                    if post_data and post_data['post_id'] not in seen_post_ids:
                        all_posts_data.append(post_data)
                        seen_post_ids.add(post_data['post_id'])
                        added += 1
                
                print(f"    Added {added} unique posts")
            else:
                print(f"    No results found")
            
            # Be polite with rate limiting
            time.sleep(random.randint(3, 6))
            
        except Exception as e:
            print(f"    Error searching for '{term}': {e}")
    
    return pd.DataFrame(all_posts_data)

def extract_post_data(post, source_identifier, cutoff_date=None):
    """
    Helper function to extract relevant data from a LinkedIn post object.
    """
    try:
        # Extract timestamp
        post_date = None
        if 'created' in post and 'time' in post['created']:
            post_date = datetime.fromtimestamp(post['created']['time'] / 1000)
        
        # Skip posts older than cutoff date
        if cutoff_date and post_date and post_date < cutoff_date:
            return None
        
        # Extract post ID
        post_id = post.get('updateMetadata', {}).get('urn', '').split(':')[-1]
        if not post_id:
            post_id = post.get('urn', '').split(':')[-1]
        
        # Extract text content
        text = ""
        if 'commentary' in post:
            text = post['commentary'].get('text', {}).get('text', '')
        elif 'value' in post and 'com.linkedin.voyager.feed.render.UpdateV2' in post['value']:
            update = post['value']['com.linkedin.voyager.feed.render.UpdateV2']
            if 'commentary' in update:
                text = update['commentary'].get('text', {}).get('text', '')
        
        # Extract engagement metrics
        likes = 0
        comments = 0
        shares = 0
        
        if 'socialDetail' in post:
            social = post['socialDetail']
            likes = social.get('totalSocialActivityCounts', {}).get('numLikes', 0)
            comments = social.get('totalSocialActivityCounts', {}).get('numComments', 0)
            shares = social.get('totalSocialActivityCounts', {}).get('numShares', 0)
        
        # Extract author information
        author_name = "Unknown"
        author_url = ""
        is_company_post = False
        
        if 'actor' in post:
            actor = post['actor']
            author_name = actor.get('name', {}).get('text', 'Unknown')
            
            # Check if it's a company or personal profile
            actor_urn = actor.get('urn', '')
            if 'company' in actor_urn or 'organization' in actor_urn:
                is_company_post = True
                author_url = f"https://www.linkedin.com/company/{actor_urn.split(':')[-1]}"
            else:
                author_url = f"https://www.linkedin.com/in/{actor_urn.split(':')[-1]}"
        
        # Build post URL
        post_url = f"https://www.linkedin.com/feed/update/{post_id}" if post_id else ""
        
        return {
            "platform": "LinkedIn",
            "post_id": post_id,
            "author": author_name,
            "author_profile_url": author_url,
            "is_company_post": is_company_post,
            "post_text": text,
            "post_url": post_url,
            "published_date": post_date.isoformat() if post_date else None,
            "likes": likes,
            "comments": comments,
            "shares": shares,
            "total_engagement": likes + comments + shares,
            "search_term_matched": source_identifier,
            "extracted_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        print(f"  Error extracting post data: {e}")
        return None

# --- Main Execution ---
if __name__ == "__main__":
    print("--- Starting LinkedIn Product Marketing Data Extraction ---\n")
    
    linkedin_posts_df = get_linkedin_product_posts(
        TARGET_COMPANIES, 
        LINKEDIN_PRODUCT_SEARCH_TERMS
    )
    
    # Filter out any None entries from failed extractions
    linkedin_posts_df = linkedin_posts_df.dropna(subset=['post_id'])
    
    if not linkedin_posts_df.empty:
        # Sort by total engagement
        linkedin_posts_df = linkedin_posts_df.sort_values('total_engagement', ascending=False)
        
        # Save to data directory
        output_csv_path = os.path.join("data", "linkedin_product_marketing_posts.csv")
        linkedin_posts_df.to_csv(output_csv_path, index=False)
        
        print(f"\n{'='*60}")
        print(f"Successfully extracted {len(linkedin_posts_df)} unique product-related LinkedIn posts.")
        print(f"Data saved to {output_csv_path}")
        print(f"{'='*60}\n")
        
        print("Top 5 posts by engagement:")
        print(linkedin_posts_df[['author', 'post_text', 'total_engagement', 'published_date']].head().to_string(index=False))
        
        # --- Integrate with Google Sheets ---
        try:
            from src.utils.upload_to_sheets import upload_to_google_sheet
            print("\n\nAttempting to upload data to Google Sheets...")
            upload_to_google_sheet(
                linkedin_posts_df, 
                "1gNHWjMghm4kTVbFSgC298LgWOWhgREY2wRRzTq-yHrk",  # Spreadsheet ID from URL
                "LinkedIn_Product_Content"
            )
            print("✓ Successfully uploaded to Google Sheets")
        except ImportError:
            print("\nWarning: src.utils.upload_to_sheets not found. Skipping Google Sheets upload.")
        except Exception as e:
            print(f"\nError uploading to Google Sheets: {e}")
        
        # --- Slack Notification Integration ---
        try:
            from src.utils.slack_notifier import send_slack_notification
            
            slack_message = (
                f"✨ New LinkedIn product marketing posts found! 💼\n"
                f"Extracted {len(linkedin_posts_df)} unique product-related LinkedIn posts.\n"
                f"Total engagement: {linkedin_posts_df['total_engagement'].sum():,}\n"
                f"Check the Google Sheet here: https://docs.google.com/spreadsheets/d/1gNHWjMghm4kTVbFSgC298LgWOWhgREY2wRRzTq-yHrk/edit?usp=sharing\n"
                f"Worksheet: TrendForgeAI\n"
                f"Check: LinkedIn_Product_Content worksheet for the details."
            )
            send_slack_notification(slack_message)
            print("✓ Slack notification sent")
        except ImportError:
            print("\nSlack notification function not available.")
        except Exception as e:
            print(f"\nError sending Slack notification: {e}")
    
    else:
        print("\nNo product marketing LinkedIn posts found or an error occurred during extraction.")
    
    print("\n--- LinkedIn Product Marketing Data Extraction Complete ---")
