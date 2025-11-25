import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os
import base64
import requests
from io import BytesIO

def generate_image_url(text: str) -> str:
    """Generate placeholder images with motivational quotes"""
    try:
        if not text.strip():
            text = "Mental Wellness"
        
        # Create a simple placeholder image URL with the text
        # In a real implementation, you would use DALL-E, Midjourney, or similar API
        encoded_text = text.replace(' ', '+')
        
        # Using a placeholder service that creates motivational images
        placeholder_url = f"https://via.placeholder.com/400x200/4CAF50/FFFFFF?text={encoded_text}"
        
        # Alternative: Create a more visually appealing placeholder
        colors = ['4CAF50', '2196F3', 'FF9800', '9C27B0', 'F44336']
        import random
        color = random.choice(colors)
        
        image_url = f"https://via.placeholder.com/400x200/{color}/FFFFFF?text={encoded_text}+🧘"
        
        st.info(f"Generated inspirational image for: '{text}'")
        return image_url
        
    except Exception as e:
        st.warning(f"Image generation placeholder: {str(e)}")
        return "https://via.placeholder.com/400x200/cccccc/666666?text=Wellness+Image"