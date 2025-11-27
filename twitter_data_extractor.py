# twitter_data_extractor.py (DEMO-SAFE)
import tweepy
import pandas as pd
import time
import random
import os
from datetime import datetime, timedelta, timezone

# ---------------- CONFIG ----------------
DEMO_MODE = True   # keep True for demo (single-term, small results)
DEFAULT_MAX_RESULTS = 10 if DEMO_MODE else 50
RECENT_TWEETS_DAYS = 7

# --- 1. Load API Credentials from credentials.py ---
try:
    # credentials.py must contain BEARER_TOKEN (you can include others but only BEARER_TOKEN is required for demo)
    from credentials import BEARER_TOKEN
except ImportError:
    print("Error: credentials.py not found or missing BEARER_TOKEN. Please create it with your Twitter BEARER_TOKEN.")
    exit()

# --- 2. Initialize Tweepy Client (bearer-only, wait on rate limit) ---
try:
    client = tweepy.Client(bearer_token=BEARER_TOKEN, wait_on_rate_limit=True)
except Exception as e:
    print("Failed to create Tweepy client with bearer token:", e)
    exit()

# --- 3. Define Search Terms ---
FULL_PRODUCT_SEARCH_TERMS = [
    "\"new product\"", "\"product launch\"", "#newtech", "#innovation", "#techtrends",
    "#futureof", "#unveiled", "#comingsoon", "#AI", "#wearables", "#electricvehicle", "#EV",
    "#sustainablefashion", "#ecofriendly", "#foodtech", "#plantbased", "#medtech",
    "#digitalhealth", "#smartdevice", "#smarthome"
]

if DEMO_MODE:
    PRODUCT_SEARCH_TERMS = ['"new product"']  # single-term demo
else:
    PRODUCT_SEARCH_TERMS = FULL_PRODUCT_SEARCH_TERMS

# ---------------- Extractor (simple demo-friendly) ----------------
def get_product_marketing_tweets(search_terms, max_results=DEFAULT_MAX_RESULTS, days_ago=RECENT_TWEETS_DAYS):
    rows = []
    start_time = datetime.now(timezone.utc) - timedelta(days=days_ago)
    print(f"Starting extraction for {len(search_terms)} term(s), looking back {days_ago} days. max_results={max_results}")

    for term in search_terms:
        print(f"\nSearching for term: {term}")
        try:
            query = f'{term} -is:retweet -is:reply lang:en'
            resp = client.search_recent_tweets(
                query=query,
                tweet_fields=['created_at', 'text', 'public_metrics', 'entities', 'author_id'],
                user_fields=['username', 'name', 'public_metrics'],
                expansions=['author_id'],
                start_time=start_time,
                max_results=max(5, min(max_results, 100))
            )

            users = {}
            if hasattr(resp, "includes") and resp.includes:
                for u in resp.includes.get("users", []) or []:
                    users[str(u["id"])] = u

            if resp.data:
                added = 0
                for t in resp.data:
                    tid = str(t.id)
                    author = users.get(str(t.author_id))
                    rows.append({
                        "platform": "Twitter",
                        "tweet_id": tid,
                        "created_at": t.created_at.isoformat() if t.created_at else None,
                        "text": t.text,
                        "search_term_matched": term,
                        "likes": t.public_metrics.get("like_count", 0) if t.public_metrics else 0,
                        "retweets": t.public_metrics.get("retweet_count", 0) if t.public_metrics else 0,
                        "replies": t.public_metrics.get("reply_count", 0) if t.public_metrics else 0,
                        "quotes": t.public_metrics.get("quote_count", 0) if t.public_metrics else 0,
                        "impressions": t.public_metrics.get("impression_count", 0) if t.public_metrics else 0,
                        "author_id": t.author_id,
                        "author_username": author.get("username") if author else None,
                        "author_name": author.get("name") if author else None,
                        "author_followers": author.get("public_metrics", {}).get("followers_count", 0) if author else 0,
                        "hashtags": [h["tag"] for h in t.entities.get("hashtags", [])] if getattr(t, "entities", None) and t.entities.get("hashtags") else [],
                        "mentions": [m["username"] for m in t.entities.get("mentions", [])] if getattr(t, "entities", None) and t.entities.get("mentions") else [],
                        "urls": [u["expanded_url"] for u in t.entities.get("urls", [])] if getattr(t, "entities", None) and t.entities.get("urls") else [],
                    })
                    added += 1
                print(f"  Added {added} tweets (returned: {len(resp.data)})")
            else:
                print("  No tweets returned for this term.")

            # short polite pause (demo-friendly)
            time.sleep(random.randint(2, 6))

        except tweepy.errors.TooManyRequests as e:
            print("  Rate limit (429) encountered while demoing. Error:", e)
            print("  Demo aborted to avoid long waits. Run the mock generator instead or try again later.")
            return pd.DataFrame(rows)
        except tweepy.errors.TweepyException as e:
            print("  Tweepy error:", e)
        except Exception as e:
            print("  Unexpected error:", e)

    return pd.DataFrame(rows)


if __name__ == "__main__":
    print("--- Starting Product Marketing Tweet Extraction (DEMO-SAFE) ---")
    df = get_product_marketing_tweets(PRODUCT_SEARCH_TERMS)
    if df is not None and not df.empty:
        out = "product_marketing_tweets.csv"
        df.to_csv(out, index=False)
        print(f"\nSaved {len(df)} rows to {out}\n")
        print(df.head().to_string(index=False))
    else:
        print("\nNo data saved (empty DataFrame).")
    print("\n--- Extraction (DEMO-SAFE) Complete ---")
