import streamlit as st
import threading
import tempfile
import os
import time


# Global variable to track voice availability
VOICE_AVAILABLE = False



# Try to import voice-related packages
try:
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("pyttsx3 not available - voice output disabled")

# Try to import speech recognition
try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False
    print("speech_recognition not available - voice input disabled")

# Try to import advanced TTS options
try:
    import requests
    import pygame
    import urllib.parse
    ADVANCED_TTS_AVAILABLE = True
except ImportError:
    ADVANCED_TTS_AVAILABLE = False
    print("Advanced TTS features not available")

def speak_text(text, language='en'):
    """
    Convert text to speech with multilingual support
    Uses Google TTS for multilingual support, falls back to pyttsx3
    """
    if not VOICE_AVAILABLE:
        return
    
    def _speak():
        try:
            # Try Google TTS first for better multilingual support
            if ADVANCED_TTS_AVAILABLE:
                _google_tts(text, language)
            else:
                # Fallback to pyttsx3
                _pyttsx3_tts(text, language)
                
        except Exception as e:
            print(f"TTS Error: {e}")
            # Final fallback
            try:
                _pyttsx3_tts(text, language)
            except:
                print("All TTS methods failed")

    # Run in separate thread to avoid blocking
    thread = threading.Thread(target=_speak)
    thread.daemon = True
    thread.start()

def _google_tts(text, language='en'):
    """Use Google Translate TTS for multilingual support"""
    try:
        # Language codes for Google TTS
        lang_codes = {
            'en': 'en',  # English
            'hi': 'hi',  # Hindi
            'mr': 'mr',  # Marathi
            'es': 'es',  # Spanish
            'fr': 'fr',  # French
            'de': 'de'   # German
        }
        
        lang_code = lang_codes.get(language, 'en')
        
        # URL encode the text
        encoded_text = urllib.parse.quote(text)
        
        # Google TTS URL
        url = f"https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl={lang_code}&q={encoded_text}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Save to temporary file and play
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmpfile:
                tmpfile.write(response.content)
                tmpfile.flush()
                tmpfile_path = tmpfile.name
            
            pygame.mixer.init()
            pygame.mixer.music.load(tmpfile_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.quit()
            os.unlink(tmpfile_path)
        else:
            raise Exception(f"Google TTS request failed with status {response.status_code}")
            
    except Exception as e:
        print(f"Google TTS failed: {e}")
        # Fallback to pyttsx3
        _pyttsx3_tts(text, language)

def _pyttsx3_tts(text, language='en'):
    """Fallback TTS using pyttsx3"""
    try:
        engine = pyttsx3.init()
        
        # Configure voice properties
        engine.setProperty('rate', 150)  # Speaking speed
        engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)
        
        # Try to find appropriate voice for language
        voices = engine.getProperty('voices')
        
        # Voice selection based on language
        voice_preferences = {
            'hi': ['india', 'hindi'],
            'mr': ['india', 'marathi'],
            'es': ['spanish', 'mexican'],
            'fr': ['french', 'france'],
            'de': ['german', 'deutsch']
        }
        
        target_keywords = voice_preferences.get(language, ['english'])
        
        # Find matching voice
        for voice in voices:
            voice_name = voice.name.lower()
            if any(keyword in voice_name for keyword in target_keywords):
                engine.setProperty('voice', voice.id)
                break
        else:
            # Use default voice if no match found
            if voices:
                engine.setProperty('voice', voices[0].id)
        
        engine.say(text)
        engine.runAndWait()
        
    except Exception as e:
        print(f"pyttsx3 TTS failed: {e}")
        raise

def record_voice(timeout=5, phrase_time_limit=10):
    """
    Record voice input and convert to text
    Returns: transcribed text or empty string if failed
    """
    if not SPEECH_RECOGNITION_AVAILABLE:
        st.warning("Speech recognition not available. Please install speech_recognition and PyAudio.")
        return ""
    
    try:
        recognizer = sr.Recognizer()
        
        with sr.Microphone() as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            st.info("🎤 Listening... Speak now")
            
            try:
                # Listen for audio with timeout
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                
                # Recognize speech using Google's speech recognition
                text = recognizer.recognize_google(audio)
                return text
                
            except sr.WaitTimeoutError:
                st.warning("No speech detected. Please try again.")
                return ""
            except sr.UnknownValueError:
                st.warning("Could not understand the audio. Please try again.")
                return ""
            except sr.RequestError as e:
                st.warning(f"Speech recognition service error: {e}")
                return ""
                
    except Exception as e:
        st.warning(f"Microphone access unavailable: {str(e)}")
        st.info("Please use text input instead.")
        return ""

def get_voice_status():
    """Return voice system status"""
    return {
        'voice_output': VOICE_AVAILABLE,
        'voice_input': SPEECH_RECOGNITION_AVAILABLE,
        'advanced_tts': ADVANCED_TTS_AVAILABLE
    }

def test_voice_system():
    """Test the voice system functionality"""
    results = {
        'output': False,
        'input': False,
        'message': ''
    }
    
    # Test voice output
    try:
        speak_text("Voice test completed successfully")
        results['output'] = True
    except Exception as e:
        results['message'] += f"Output failed: {e}. "
    
    # Test voice input (brief test)
    if SPEECH_RECOGNITION_AVAILABLE:
        try:
            import speech_recognition as sr
            r = sr.Recognizer()
            # Just check if microphone is available without actually listening
            with sr.Microphone() as source:
                results['input'] = True
        except:
            results['message'] += "Input not available. "
    
    return results

# Voice settings configuration
class VoiceSettings:
    def __init__(self):
        self.rate = 150
        self.volume = 0.9
        self.enabled = True
    
    def configure(self, rate=None, volume=None, enabled=None):
        if rate is not None:
            self.rate = rate
        if volume is not None:
            self.volume = volume
        if enabled is not None:
            self.enabled = enabled

# Global voice settings instance
voice_settings = VoiceSettings()

def setup_voice_controls():
    """Setup voice controls for Streamlit sidebar"""
    with st.sidebar:
        st.header("🔊 Voice Settings")
        
        # Voice enable/disable
        voice_enabled = st.checkbox(
            "Enable Voice Responses", 
            value=voice_settings.enabled,
            help="Play AI responses as speech",
            key="voice_enable_checkbox"  # Add key
        )
        
        if voice_enabled:
            # Voice speed control
            voice_rate = st.slider(
                "Voice Speed",
                min_value=100,
                max_value=300,
                value=voice_settings.rate,
                help="Adjust speech speed",
                key="voice_speed_slider"  # Add key
            )
            
            # Voice volume control
            voice_volume = st.slider(
                "Voice Volume",
                min_value=0.1,
                max_value=1.0,
                value=voice_settings.volume,
                help="Adjust speech volume",
                key="voice_volume_slider"  # Add key
            )
            
            # Update settings
            voice_settings.configure(
                rate=voice_rate,
                volume=voice_volume,
                enabled=voice_enabled
            )
            
            st.success("✅ Voice enabled")
        else:
            voice_settings.enabled = False
            st.info("🔇 Voice disabled")
        
        # Voice status
        st.write("---")
        st.write("**Voice System Status:**")
        status = get_voice_status()
        
        if status['voice_output']:
            st.success("✅ Voice output: Available")
        else:
            st.error("❌ Voice output: Not available")
            
        if status['voice_input']:
            st.success("✅ Voice input: Available")
        else:
            st.warning("⚠️ Voice input: Not available")
        
        # Test button
        if st.button("Test Voice System", key="test_voice_button"):  # Add key
            test_results = test_voice_system()
            if test_results['output']:
                st.success("Voice output test passed!")
            else:
                st.error("Voice output test failed")
            
            if test_results['input']:
                st.success("Voice input test passed!")
            else:
                st.warning("Voice input test skipped or failed")

# For quick testing
if __name__ == "__main__":
    print("Voice IO Module Test")
    print(f"Voice Output Available: {VOICE_AVAILABLE}")
    print(f"Voice Input Available: {SPEECH_RECOGNITION_AVAILABLE}")
    print(f"Advanced TTS Available: {ADVANCED_TTS_AVAILABLE}")
    
    # Test voice output
    if VOICE_AVAILABLE:
        print("Testing voice output...")
        speak_text("Hello! This is a test of the voice system.")