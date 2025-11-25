from youtubesearchpython import VideosSearch
import streamlit as st

def get_youtube_suggestion(topic: str) -> str:
    """Get YouTube video suggestions for mental wellness topics"""
    try:
        if not topic.strip():
            return "Please specify a topic for YouTube suggestions."
        
        # Search for mental wellness related videos
        search_query = f"{topic} mental wellness meditation mindfulness"
        videos_search = VideosSearch(search_query, limit=3)
        results = videos_search.result()
        
        if not results or 'result' not in results or len(results['result']) == 0:
            return f"No YouTube videos found for '{topic}'. Try a different topic."
        
        response = f"Here are some YouTube videos about '{topic}':\n\n"
        
        for i, video in enumerate(results['result'][:3], 1):
            title = video.get('title', 'No title')
            channel = video.get('channel', {}).get('name', 'Unknown channel')
            duration = video.get('duration', 'Unknown duration')
            url = video.get('link', '#')
            
            response += f"{i}. **{title}**\n"
            response += f"   📺 Channel: {channel}\n"
            response += f"   ⏱️ Duration: {duration}\n"
            response += f"   🔗 [Watch Video]({url})\n\n"
        
        response += "I hope these resources are helpful for your wellness journey! 🧘"
        return response
        
    except Exception as e:
        return f"Sorry, I couldn't fetch YouTube suggestions right now. Error: {str(e)}"