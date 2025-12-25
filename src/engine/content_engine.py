import google.generativeai as genai
import pandas as pd
import json
import os
import random
import time
import numpy as np
import sys
from datetime import datetime

# Add project root to path to import credentials
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# Load API Key
try:
    from credentials import GEMINI_API_KEY
    genai.configure(api_key=GEMINI_API_KEY)
except ImportError:
    print("Error: GEMINI_API_KEY not found in credentials.py.")
    exit()

# Load Data Curator Dataset
# Script is in src/engine/ -> ../../data/
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "data", "top_performing_examples.json"))

def load_dataset():
    if os.path.exists(DATASET_PATH):
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    print(f"Warning: Dataset not found at {DATASET_PATH}")
    return {"linkedin_best": [], "youtube_best": [], "twitter_best": [], "trending_topics": []}

DATASET = load_dataset()

class ContentEngine:
    def __init__(self):
        self.model = genai.GenerativeModel("models/gemini-2.5-flash")
        
    def get_embedding(self, text):
        try:
            result = genai.embed_content(
                model="models/text-embedding-004",
                content=text,
                task_type="retrieval_query"
            )
            return result['embedding']
        except Exception as e:
            print(f"Embedding error: {e}")
            return None

    def get_style_examples(self, platform, topic, product_info, n=3):
        key = f"{platform.lower()}_best"
        examples = DATASET.get(key, [])
        if not examples:
            return ""
        
        # Check if examples have embeddings (new format)
        if isinstance(examples[0], dict) and "embedding" in examples[0]:
            print(f"   Using Semantic RAG to find best {platform} examples for '{topic}'...")
            query = f"{topic} {product_info}"
            query_embedding = self.get_embedding(query)
            
            if query_embedding:
                # Calculate Cosine Similarity
                scored_examples = []
                for ex in examples:
                    emb = ex['embedding']
                    score = np.dot(query_embedding, emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(emb))
                    scored_examples.append((score, ex['text']))
                
                # Sort by score descending
                scored_examples.sort(key=lambda x: x[0], reverse=True)
                selected = [ex[1] for ex in scored_examples[:n]]
                print(f"   Selected top {n} examples with similarity scores: {[f'{s:.2f}' for s, _ in scored_examples[:n]]}")
            else:
                print("   Warning: Could not generate query embedding. Falling back to random.")
                selected = [ex['text'] for ex in random.sample(examples, min(n, len(examples)))]
        else:
            # Old format (list of strings)
            print("   Using Random Selection (No embeddings found in dataset)...")
            selected = random.sample(examples, min(n, len(examples)))

        formatted = "\n\n".join([f"Example {i+1}:\n{ex}" for i, ex in enumerate(selected)])
        return f"\n\nHere are {len(selected)} examples of highly successful {platform} content to mimic:\n{formatted}\n"

    def generate_draft(self, topic, platform, product_info):
        style_examples = self.get_style_examples(platform, topic, product_info)
        
        prompt = f"""
        You are an expert Content Marketing AI specialized in {platform}.
        
        Task: Write a high-engagement {platform} post about the following product.
        Topic/Angle: {topic}
        Product Info: {product_info}
        
        {style_examples}
        
        Instructions:
        1. Analyze the style examples (tone, structure, hooks, emoji usage).
        2. Write a NEW post that perfectly mimics this "viral style".
        3. Ensure the first line is a powerful hook.
        4. Focus on value and engagement.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating draft: {e}")
            return None

    def critique_content(self, draft, platform):
        prompt = f"""
        Act as a strict Editor-in-Chief. Critique the following {platform} post draft.
        
        Draft:
        {draft}
        
        Return a JSON object with:
        - "hook_score": (1-10)
        - "value_score": (1-10)
        - "viral_score": (1-10)
        - "average_score": (mean of above)
        - "critique": "One sentence summary of what to improve"
        """
        
        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text)
        except Exception as e:
            print(f"Error critiquing: {e}")
            # Fallback
            return {"average_score": 5, "critique": "Error in critique step."}

    def optimize_content(self, draft, critique, platform):
        prompt = f"""
        You are an expert Copywriter. Improve this draft based on the editor's feedback.
        
        Original Draft:
        {draft}
        
        Editor's Feedback: "{critique}"
        
        Task: Rewrite the post to address the feedback and maximize engagement. Keep the original core message but make it punchier.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error optimizing: {e}")
            return draft

    def run_pipeline(self, topic, platform, product_info):
        print(f"\n--- Running Content Engine for {platform} ---")
        print(f"Topic: {topic}")
        
        # 1. Draft
        print("1. Generating Draft with Style Injection...")
        draft = self.generate_draft(topic, platform, product_info)
        if not draft: return None
        
        # 2. Critique
        print("2. Critiquing Draft...")
        scores = self.critique_content(draft, platform)
        print(f"   Score: {scores.get('average_score')}/10 - {scores.get('critique')}")
        
        final_content = draft
        status = "Draft Accepted"
        
        # 3. Optimize (if needed)
        if scores.get('average_score', 0) < 8.5:
            print("3. Score below 8.5. Optimizing...")
            final_content = self.optimize_content(draft, scores.get('critique'), platform)
            status = "Optimized"
            
            # Re-score (optional, but good for logging)
            new_scores = self.critique_content(final_content, platform)
            print(f"   New Score: {new_scores.get('average_score')}/10")
            scores = new_scores # Update scores for logging
            
        return {
            "platform": platform,
            "topic": topic,
            "final_content": final_content,
            "original_draft": draft,
            "quality_score": scores.get('average_score'),
            "critique_notes": scores.get('critique'),
            "status": status,
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    engine = ContentEngine()
    
    # Example Product
    product = "TrendForgeAI - An AI tool that predicts marketing trends and auto-generates viral content."
    
    # Topics (Try to get from trends if available, else use defaults)
    topics = DATASET.get("trending_topics", [])
    
    results = []
    topic = "Remote Work Trends"
    num_posts = 3

    print(f"Generating {num_posts} posts for topic: {topic}")

    for i in range(num_posts):
        print(f"\n--- Generation {i+1}/{num_posts} ---")
        # Generate for LinkedIn
        res_li = engine.run_pipeline(topic, "LinkedIn", product)
        if res_li: 
            res_li['variation'] = i + 1
            results.append(res_li)
        
        # Generate for YouTube
        res_yt = engine.run_pipeline(topic, "YouTube", product)
        if res_yt: 
            res_yt['variation'] = i + 1
            results.append(res_yt)
    
    # Save to Sheets
    if results:
        df = pd.DataFrame(results)
        print("\n--- Generated Content ---")
        print(df[['platform', 'quality_score', 'status']].to_string())
        
        try:
            from src.utils.upload_to_sheets import upload_to_google_sheet
            print("\nUploading to Google Sheets...")
            # Using the user's Sheet ID
            upload_to_google_sheet(df, "1gNHWjMghm4kTVbFSgC298LgWOWhgREY2wRRzTq-yHrk", "Generated_Marketing_Content")
            
            # Slack Notification
            try:
                from src.utils.slack_notifier import send_slack_notification
                msg = (
                    f"🚀 *Content Engine Report*\n"
                    f"Generated {len(results)} optimized posts.\n"
                    f"Avg Quality Score: {df['quality_score'].mean():.1f}/10\n"
                    f"Check Sheet: https://docs.google.com/spreadsheets/d/1gNHWjMghm4kTVbFSgC298LgWOWhgREY2wRRzTq-yHrk/edit?usp=sharing"
                )
                send_slack_notification(msg, username="TrendForge Engine", icon_emoji=":rocket:")
            except: pass
            
        except Exception as e:
            print(f"Upload failed: {e}")
