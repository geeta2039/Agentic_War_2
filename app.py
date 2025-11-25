import streamlit as st
import os
from dotenv import load_dotenv
import datetime
import matplotlib.pyplot as plt
import random
from langdetect import detect, DetectorFactory

# -----------------------
# Custom CSS Styling
# -----------------------
def apply_custom_styles():
    st.markdown("""
    <style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #2e4a7d 0%, #1f3a60 100%);
    }
    
   .main-header {
      font-size: 3.5rem;
      color: blue;
      text-align: center;
      margin-bottom: 1rem;
      font-weight: bold;
     -webkit-background-clip: text;
     background-clip: text;
 } 
    

    
    /* Section headers */
    .section-header {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
        color: white;
        padding: 15px;
        border-radius: 15px;
        margin: 20px 0px 10px 0px;
        font-weight: bold;
        text-align: center;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    
    /* User section highlight */
    .user-section {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 20px;
        border: 3px solid #ffffff;
        margin: 15px 0px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    /* Language section styling */
    .language-section {
        background: linear-gradient(135deg, #a8ff78 0%, #78ffd6 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    
    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%);
        color: white;
        border: none;
        padding: 15px 30px;
        border-radius: 12px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
        background: linear-gradient(135deg, #ffa726 0%, #ff6b6b 100%);
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        font-weight: bold;
        text-align: center;
        margin: 15px 0px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Info box styling */
    .info-box {
        background: linear-gradient(135deg, #a8c0ff 0%, #3f4c6b 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        margin: 15px 15px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    

    /* Tab styling */
   .stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: transparent;
    padding: 10px 0;
    }

    .stTabs [data-baseweb="tab"] {
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    color: white;
    border-radius: 18px 18px 0px 0px;
    padding: 22px 38px;
    font-weight: bold;
    font-size: 3.4rem;
    margin-top: 0px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.2);
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 200px;
    transition: all 0.3s ease;
}

   .stTabs [data-baseweb="tab"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 22px rgba(0,0,0,0.3);
}

   .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #ff6b6b 0%, #ffa726 100%) !important;
    transform: scale(1.05) translateY(-5px);
    font-size: 3.5rem;
    box-shadow: 0 10px 25px rgba(255,107,107,0.5);
}
   /* Text input styling */
    .stTextInput>div>div>input {
        background-color: #ffffff;
        border: 3px solid #667eea;
        border-radius: 12px;
        padding: 12px;
        font-size: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Select box styling */
    .stSelectbox>div>div {
        background-color: #ffffff;
        border: 3px solid #667eea;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Checkbox styling */
    .stCheckbox>label {
        font-weight: bold;
        color: #2e4a7d;
        font-size: 1rem;
    }
    
    /* Voice section styling */
    .voice-section {
        background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 15px 0px;
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    

    
    /* Stats container */
    .stats-container {
        background: linear-gradient(135deg, #a8ff78 0%, #78ffd6 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# -----------------------
# Voice Configuration
# -----------------------
try:
    from utils.voice_io import speak_text, record_voice, VOICE_AVAILABLE
except ImportError:
    VOICE_AVAILABLE = False
    def speak_text(text, language='en') -> None:
        pass
    def record_voice():
        return ""

# -----------------------
# Load Environment
# -----------------------
load_dotenv()
api_key = os.getenv("GENAI_API_KEY")

if not api_key:
    st.error("❌ Gemini API Key not found. Please set GENAI_API_KEY in your .env file")
    st.stop()

# -----------------------
# SIMPLIFIED IMPORTS (No Agents)
# -----------------------
try:
    from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
    from langchain_community.vectorstores import Chroma
    
    # ✅ CORRECT Memory import
    try:
        from langchain_community import ConversationBufferMemory
    except ImportError:
        try:
            from langchain_community.chat_message_histories import ChatMessageHistory
            from langchain_community import ConversationBufferMemory
        except ImportError:
            # Final fallback - create a simple memory class
            class ConversationBufferMemory:
                def __init__(self, memory_key="chat_history", return_messages=True):
                    self.memory_key = memory_key
                    self.return_messages = return_messages
                    self.chat_memory = type('obj', (object,), {'messages': []})()
                
                def save_context(self, inputs, outputs):
                    if not hasattr(self.chat_memory, 'messages'):
                        self.chat_memory.messages = []
                    self.chat_memory.messages.append(type('obj', (object,), {'type': 'human', 'content': list(inputs.values())[0]})())
                    self.chat_memory.messages.append(type('obj', (object,), {'type': 'ai', 'content': list(outputs.values())[0]})())
                    
except ImportError as e:
    st.error(f"❌ Import Error: {e}")
    st.info("Please install: pip install langchain-community langchain-google-genai")
    st.stop()

# Import other utilities with error handling
try:
    from utils.youtube_tools import get_youtube_suggestion
    YOUTUBE_AVAILABLE = True
except ImportError:
    YOUTUBE_AVAILABLE = False

try:
    from utils.image_tools import generate_image_url
    IMAGE_AVAILABLE = True
except ImportError:
    IMAGE_AVAILABLE = False

# -----------------------
# Memory Management
# -----------------------
persist_dir = "./db/chroma"
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=api_key)

try:
    vectorstore = Chroma(
        collection_name="mental_wellness_chat",
        embedding_function=embeddings,
        persist_directory=persist_dir
    )
except Exception as e:
    st.warning(f"ChromaDB initialization warning: {e}")
    vectorstore = None

DetectorFactory.seed = 0

# -----------------------
# Language Configuration
# -----------------------
supported_languages = {
    "English": "en",
    "Hindi": "hi", 
    "Marathi": "mr",
    "Spanish": "es",
    "French": "fr",
    "German": "de"
}

language_names = {
    'en': 'English',
    'hi': 'Hindi',
    'mr': 'Marathi',
    'es': 'Spanish', 
    'fr': 'French',
    'de': 'German'
}

# -----------------------
# Enhanced LLM Prompt System
# -----------------------
def create_contextual_prompt(user_input, language, context_type, conversation_history=None) -> str:
    """Create dynamic prompts for different contexts"""
    
    base_instructions = {
        'en': "You are a compassionate mental wellness assistant. Provide warm, empathetic, and practical support.",
        'hi': "आप एक दयालु मानसिक स्वास्थ्य सहायक हैं। गर्मजोशी, सहानुभूतिपूर्ण और व्यावहारिक सहायता प्रदान करें।",
        'mr': "तुम एक कनवाळू मानसिक आरोग्य सहाय्यक आहात. उबदार, सहानुभूतिपूर्ण आणि व्यावहारिक आधार द्या.",
        'es': "Eres un asistente de bienestar mental compasivo. Proporciona apoyo cálido, empático y práctico.",
        'fr': "Vous êtes un assistant de bien-être mental compatissant. Fournissez un soutien chaleureux, empathique et pratique.",
        'de': "Sie sind ein mitfühlender Assistent für psychisches Wohlbefinden. Bieten Sie warme, einfühlsame und praktische Unterstützung."
    }
    
    context_prompts = {
        'mood_analysis': {
            'en': "Analyze the user's mood and provide supportive, practical mental health advice. Be empathetic and understanding.",
            'hi': "उपयोगकर्ता के मूड का विश्लेषण करें और सहायक, व्यावहारिक मानसिक स्वास्थ्य सलाह दें। सहानुभूतिपूर्ण और समझदार बनें।",
            'mr': "वापरकर्त्याच्या मूडचे विश्लेषण करा आणि सहाय्यक, व्यावहारिक मानसिक आरोग्य सल्ला द्या. सहानुभूतिपूर्ण आणि समजूतदार व्हा.",
            'es': "Analiza el estado de ánimo del usuario y proporciona consejos de salud mental prácticos y de apoyo. Sé empático y comprensivo.",
            'fr': "Analysez l'humeur de l'utilisateur et fournissez des conseils de salud mental pratiques et de soutien. Soyez empathique et compréhensif.",
            'de': "Analysieren Sie die Stimmung des Benutzers und geben Sie praktische Ratschläge zur psychischen Gesundheit. Seien Sie einfühlsam und verständnisvoll."
        },
        'mindfulness': {
            'en': "Provide a practical mindfulness or meditation exercise. Make it easy to follow and beneficial for mental wellbeing.",
            'hi': "एक व्यावहारिक माइंडफुलनेस या ध्यान व्यायाम प्रदान करें। इसे आसान और मानसिक स्वास्थ्य के लिए फायदेमंद बनाएं।",
            'mr': "एक व्यावहारिक माइंडफुलनेस किंवा ध्यान व्यायाम प्रदान करा. तो अनुसरण करण्यास सोपा आणि मानसिक आरोग्यासाठी फायदेशीर बनवा.",
            'es': "Proporciona un ejercicio práctico de mindfulness o meditación. Hazlo fácil de seguir y beneficioso para el bienestar mental.",
            'fr': "Fournissez un exercice pratique de pleine conscience ou de méditation. Rendez-le fácil à suivre et bénéfique pour le bien-être mental.",
            'de': "Bieten Sie eine praktische Achtsamkeits- oder Meditationsübung an. Machen Sie sie fácil zu befolgen und vorteilhaft für das psychische Wohlbefinden."
        },
        'motivation': {
            'en': "Provide motivational encouragement that inspires hope and positivity. Be uplifting and supportive.",
            'hi': "प्रेरक प्रोत्साहन प्रदान करें जो आशा और सकारात्मकता को प्रेरित करे। उत्थान और सहायक बनें।",
            'mr': "प्रेरणादायी प्रोत्साहन प्रदान करा जे आशा आणि सकारात्मकतेस प्रेरित करे. उत्थान आणि सहाय्यक व्हा.",
            'es': "Proporciona un estímulo motivador que inspire esperanza y positividad. Sé edificante y solidario.",
            'fr': "Fournissez un encouragement motivationnel qui inspire l'espoir et la positivité. Soyez édifiante y solidaire.",
            'de': "Bieten Sie motivationsfördernde Ermutigung, die Hoffnung und Positivität inspiriert. Seien Sie erhebend und unterstützend."
        },
        'journal': {
            'en': "Provide a thoughtful journaling prompt that encourages self-reflection and personal growth.",
            'hi': "एक विचारशील जर्नलिंग प्रॉम्प्ट प्रदान करें जो आत्म-चिंतन और व्यक्तिगत विकास को प्रोत्साहित करे।",
            'mr': "एक विचारपूर्वक जर्नलिंग प्रॉम्प्ट प्रदान करा जो स्व-चिंतन आणि वैयक्तिक वाढीस प्रोत्साहित करेल.",
            'es': "Proporciona un mensaje de diario reflexivo que fomente la autorreflexión y el crecimiento personal.",
            'fr': "Fournissez une invite de journalisation réfléchie qui encourage l'autoréflexion et la croissance personnelle.",
            'de': "Geben Sie einen nachdenklichen Journaling-Prompt, der Selbstreflexion und persönliches Wachstum fördert."
        },
        'general': {
            'en': "Provide helpful mental wellness support and guidance.",
            'hi': "मददगार मानसिक स्वास्थ्य सहायता और मार्गदर्शन प्रदान करें।",
            'mr': "उपयुक्त मानसिक आरोग्य आधार आणि मार्गदर्शन प्रदान करा.",
            'es': "Proporciona ayuda y orientación útiles para el bienestar mental.",
            'fr': "Fournissez un soutien et des conseils utiles para el bien-être mental.",
            'de': "Bieten Sie hilfreiche Unterstützung und Anleitung für das psychische Wohlbefinden."
        }
    }
    
    base_instruction = base_instructions.get(language, base_instructions['en'])
    context_instruction = context_prompts[context_type].get(language, context_prompts[context_type]['en'])
    # Build conversation history context
    history_context = ""
    if conversation_history:
        history_context = "\n\nPrevious conversation:\n"
        for msg in conversation_history[-6:]:  # Last 3 exchanges
            if hasattr(msg, 'type') and hasattr(msg, 'content'):
                role = "User" if msg.type == "human" else "Assistant"
                history_context += f"{role}: {msg.content}\n"
    
    prompt = f"""{base_instruction}

Context: {context_instruction}
{history_context}

Current user message: {user_input}

Please respond in {language_names.get(language, 'English')} language with appropriate warmth and empathy."""
    
    return prompt

def detect_user_language(text):
    """Detect language from user input"""
    try:
        return detect(text)
    except:
        return 'en'

def get_llm_response(user_input, language, context_type, llm, memory=None):
    """Get response from LLM in specified language and context"""
    try:
        # Get conversation history if memory exists
        conversation_history = []
        if memory and hasattr(memory, 'chat_memory') and hasattr(memory.chat_memory, 'messages'):
            conversation_history = memory.chat_memory.messages
        
        # Create a more specific prompt based on context type
        if context_type == 'mood_analysis':
            # For mood analysis, use the actual user input
            prompt_text = user_input
        elif context_type == 'mindfulness':
            # For mindfulness, be more specific
            prompt_text = f"The user wants a mindfulness exercise. {user_input}" if user_input else "Provide a practical mindfulness exercise"
        elif context_type == 'motivation':
            # For motivation, be more specific  
            prompt_text = f"The user needs motivation. {user_input}" if user_input else "Provide an inspiring motivational message"
        elif context_type == 'journal':
            # For journal, be more specific
            prompt_text = f"The user wants a journal prompt. {user_input}" if user_input else "Provide a thoughtful journaling prompt"
        else:
            prompt_text = user_input
        
        prompt = create_contextual_prompt(prompt_text, language, context_type, conversation_history)
        
        response = llm.invoke(prompt)
        
        # Save to memory
        if memory:
            memory.save_context({"input": user_input}, {"output": response.content})
        
        return response.content
        
    except Exception as e:
        # Fallback response in appropriate language
        fallback_responses = {
            'en': "I understand you're reaching out for support. Let me help you with that. Could you please share a bit more about how you're feeling?",
            'hi': "मैं समझता हूं कि आप सहायता के लिए संपर्क कर रहे हैं। मुझे आपकी मदद करने दें। क्या आप कृपया थोड़ा और बता सकते हैं कि आप कैसा महसूस कर रहे हैं?",
            'mr': "मी समजतो की तुम्हाला आधारासाठी संपर्क करत आहात. मला तुमची मदत करू द्या. कृपया तुम्हाला कसे वाटत आहे ते थोडे अधिक सांगू शकता?",
            'es': "Entiendo que estás buscando apoyo. Permíteme ayudarte con eso. ¿Podrías compartir un poco más sobre cómo te sientes?",
            'fr': "Je comprends que vous cherchez du soutien. Permettez-moi de vous aider avec cela. Pourriez-vous s'il vous plaît partager un peu plus sur ce que vous ressentez ?",
            'de': "Ich verstehe, dass Sie Unterstützung suchen. Lassen Sie mich Ihnen dabei helfen. Könnten Sie bitte etwas mehr darüber teilen, wie Sie sich fühlen?"
        }
        return fallback_responses.get(language, fallback_responses['en'])

user_memories = {}

def get_user_memory(user_id):
    """Get or create conversation memory for a user"""
    if user_id not in user_memories:
        user_memories[user_id] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
    return user_memories[user_id]

def execute_wellness_tool(query, user_input, memory, llm=None, language='en', context_type='general'):
    """Execute wellness tools with multilingual LLM support"""
    try:
        # Auto-detect language if enabled
        current_language = language
        if st.session_state.get('auto_detect', False):
            detected_lang = detect_user_language(query)
            if detected_lang in supported_languages.values():
                current_language = detected_lang
                st.session_state.current_language = detected_lang
        
        # Determine context type based on query
        query_lower = query.lower()
        
        if any(word in query_lower for word in ["mood", "feeling", "feel", "emotion", "emotional"]):
            context_type = 'mood_analysis'
        elif any(word in query_lower for word in ["mindfulness", "meditation", "exercise", "breathe", "calm", "relax"]):
            context_type = 'mindfulness'
        elif any(word in query_lower for word in ["motivation", "quote", "inspire", "encouragement", "positive"]):
            context_type = 'motivation'
        elif any(word in query_lower for word in ["journal", "prompt", "write", "reflect", "reflection"]):
            context_type = 'journal'
        else:
            context_type = 'general'
        
        # Use LLM for all responses
        if llm:
            response = get_llm_response(query, current_language, context_type, llm, memory)
        else:
            # Fallback to English if no LLM
            response = "I'm here to support your mental wellness. Please try again."
        
        return response
        
    except Exception as e:
        error_msg = f"I encountered an issue while processing your request. Please try again."
        return error_msg
# -----------------------
# Streamlit UI
# -----------------------
st.set_page_config(
    page_title="Mental Wellness AI Companion", 
    page_icon="🧘", 
    layout="wide",
    initial_sidebar_state="expanded"
)
apply_custom_styles()

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False

# Main header with enhanced styling
st.markdown('<h1 class="main-header">🧘 Mental Wellness AI Companion</h1>', unsafe_allow_html=True)

# Sidebar for customization
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Language Selection
    st.markdown("### 🌐 Language")
    selected_language_name = st.selectbox(
        "Choose your language:",
        options=list(supported_languages.keys()),
        index=0,
        key="sidebar_language_selector"
    )
    
    auto_detect = st.checkbox(
        "Auto-detect language", 
        value=True, 
        key="sidebar_auto_detect"
    )
    
    # Voice Settings
    st.markdown("### 🔊 Voice")
    enable_voice = st.checkbox(
        "Enable voice responses", 
        value=False,
        key="sidebar_voice_enable"
    )
    
    if enable_voice and VOICE_AVAILABLE:
        st.success("Voice enabled!")
    elif enable_voice and not VOICE_AVAILABLE:
        st.warning("Voice not available")
    
    # Initialize session
if not st.session_state.initialized:
        if st.button("🚀 Start Journey", use_container_width=True, type="primary"):
            user_id = f"user_{random.randint(1000, 9999)}"
            
            st.session_state.user_id = user_id
            st.session_state.initialized = True
            st.session_state.selected_language = selected_language_name
            st.session_state.auto_detect = auto_detect
            st.session_state.current_language = supported_languages[selected_language_name]
            st.session_state.enable_voice = enable_voice
            
            # Initialize user session
            memory = get_user_memory(user_id)
            
            # Initialize LLM 
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.5-flash",
                temperature=0.7, 
                google_api_key=api_key
            )
            
            # Store in session state
            st.session_state.memory = memory
            st.session_state.llm = llm
            
            st.balloons()
            st.success("Ready to begin!")
            st.rerun()
    

    

# Main Content Area
if st.session_state.get('initialized', False):
    # Access session state
    memory = st.session_state.memory
    llm = st.session_state.llm
    enable_voice_responses = st.session_state.enable_voice
    # Welcome Banner
    st.markdown(f"""
    <div style="text-align: center; padding: 10px 20px;">
        <p style="color:#32CD32; font-size: 1.3rem; margin-bottom: 10px;">
            Your AI companion for emotional support, mindfulness, and personal growth is ready to help you
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Stats Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="stats-container">📅<br>Daily Check-ins<br><h3>Ready!</h3></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="stats-container">🧘<br>Mindfulness<br><h3>Available</h3></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div class="stats-container">📖<br>Journal<br><h3>Ready!</h3></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div class="stats-container">💫<br>Motivation<br><h3>24/7</h3></div>', unsafe_allow_html=True)
   
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏠 Daily Check-In", "🌿 Mindfulness", "📔 Journal", "💪 Motivation", "🎨 Creative Space"])

    # --- Daily Mood Check-In ---
    with tab1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #1f3a60; text-align: center; margin: 0px 0;">🌈 How Are You Feeling Today?</h2>', unsafe_allow_html=True)
        # Language info
        current_language = st.session_state.current_language
        if st.session_state.auto_detect:
            st.markdown(f'<div class="info-box">🌐 Auto-detect: ON | Current: {language_names.get(current_language, "English")}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="info-box">🌐 Language: {language_names.get(current_language, "English")}</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown('<h4 style="color: #1f3a60;">🎤 Share Your Feelings</h4>', unsafe_allow_html=True)
            mode = st.radio("Choose input method:", ["Text", "Voice"], horizontal=True, key="mood_input_mode")
            mood_input = ""
            
            if mode == "Text":
                mood_input = st.text_area(
                    "Tell me about your day...",
                    placeholder="I'm feeling... happy/sad/anxious/excited/tired/etc.\nWhat's on your mind?",
                    height=120,
                    key="mood_text_input"
                )
            else:
                if VOICE_AVAILABLE:
                    if st.button("🎤 Start Voice Recording", use_container_width=True, key="voice_record_btn"):
                        with st.spinner("🎙️ Listening... Speak now..."):
                            mood_input = record_voice()
                    if mood_input:
                        st.success("✅ Voice recorded successfully!")
                        st.write(f"**You said:** {mood_input}")
                else:
                    st.warning("🎧 Voice input not available in this environment")
        
        with col2:
            st.markdown('<h4 style="color: #1f3a60;">⚡ Quick Emotions</h4>', unsafe_allow_html=True)
            quick_feelings = ["😊 Happy & Content", "😢 Sad & Low", "😰 Anxious & Worried", "😠 Frustrated & Angry", "😴 Tired & Drained", "😌 Calm & Peaceful", "🎉 Excited & Energetic"]
            selected_feeling = st.selectbox("Select your current mood:", [""] + quick_feelings, key="quick_feelings_select")
            
            if selected_feeling:
                mood_input = selected_feeling
                st.info(f"Selected: {selected_feeling}")
        
        # Mood check button
        if st.button("🔍 Analyze My Mood & Get Support", type="primary", use_container_width=True, key="analyze_mood_btn"):
            if mood_input:
                # Auto-detect language if enabled
                current_language = st.session_state.current_language
                if st.session_state.auto_detect:
                    detected_lang = detect_user_language(mood_input)
                    if detected_lang in supported_languages.values():
                        current_language = detected_lang
                        st.session_state.current_language = detected_lang
                
                with st.spinner("🔮 Analyzing your emotions and preparing personalized support..."):
                    response = get_llm_response(
                        mood_input, 
                        current_language, 
                        'mood_analysis', 
                        llm, 
                        memory
                    )
                
                st.success("🎯 Mood Analysis Complete!")
                st.markdown(f'<div class="custom-card">{response}</div>', unsafe_allow_html=True)

                # Speak response if voice enabled
                if VOICE_AVAILABLE and enable_voice_responses:
                    speak_text(response, language=current_language)
                
                # Store in vector database if available
                if vectorstore:
                    try:
                        vectorstore.add_texts(
                            [f"Mood: {mood_input}"], 
                            metadatas=[{
                                "user": st.session_state.user_id, 
                                "type": "mood", 
                                "timestamp": str(datetime.datetime.now())
                            }]
                        )
                    except Exception as e:
                        st.warning(f"Note: Could not save to long-term memory: {e}")
            else:
                st.warning("Please share your mood before submitting.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Mindfulness ---
    with tab2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #1f3a60; text-align: center;">🌿 Mindfulness & Meditation Hub</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Find your center with guided mindfulness practices</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🧘 Get Personalized Mindfulness Exercise", use_container_width=True, key="mindfulness_btn"):
                current_language = st.session_state.current_language
                with st.spinner("🌱 Curating a perfect mindfulness exercise for you..."):
                    response = get_llm_response(
                        "Provide a personalized mindfulness or meditation exercise", 
                        current_language, 
                        'mindfulness', 
                        llm, 
                        memory
                    )
                st.markdown(f'<div class="custom-card">{response}</div>', unsafe_allow_html=True)
                if VOICE_AVAILABLE and enable_voice_responses:
                    speak_text(response, language=current_language)

        with col2:
            if st.button("🌬️ Breathing & Relaxation Exercise", use_container_width=True, key="breathing_btn"):
                current_language = st.session_state.current_language
                with st.spinner("💨 Creating a calming breathing exercise..."):
                    response = get_llm_response(
                        "Provide a breathing exercise for deep relaxation and stress relief", 
                        current_language, 
                        'mindfulness', 
                        llm, 
                        memory
                    )
                st.markdown(f'<div class="custom-card">{response}</div>', unsafe_allow_html=True)
                if VOICE_AVAILABLE and enable_voice_responses:
                    speak_text(response, language=current_language)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Journal ---
    with tab3:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #1f3a60; text-align: center;">📔 Reflection & Journal Space</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Process your thoughts and track your growth journey</p>', unsafe_allow_html=True)
        
        if st.button("💡 Get Thoughtful Journal Prompt", use_container_width=True, key="journal_prompt_btn"):
            current_language = st.session_state.current_language
            with st.spinner("📝 Finding a meaningful prompt for reflection..."):
                response = get_llm_response(
                    "Provide an insightful journaling prompt for self-reflection and personal growth", 
                    current_language, 
                    'journal', 
                    llm, 
                    memory
                )
            st.markdown(f'<div class="custom-card">{response}</div>', unsafe_allow_html=True)
            if VOICE_AVAILABLE and enable_voice_responses:
                speak_text(response, language=current_language)
        
        # Journal entry area
        st.markdown("### ✍️ Your Personal Journal")
        journal_entry = st.text_area(
            "Write your thoughts, feelings, and reflections here:",
            placeholder="This is your safe space to express yourself freely...\n\nWhat are you grateful for today?\nWhat challenges did you face?\nHow are you really feeling?\nWhat lessons have you learned?",
            height=200,
            key="journal_entry_area"
        )
        
        if st.button("💾 Save This Journal Entry", use_container_width=True, key="save_journal_btn"):
            if journal_entry:
                try:
                    if vectorstore:
                        vectorstore.add_texts(
                            [f"Journal: {journal_entry}"],
                            metadatas=[{
                                "user": st.session_state.user_id, 
                                "type": "journal", 
                                "timestamp": str(datetime.datetime.now())
                            }]
                        )
                    st.success("✅ Journal entry saved successfully! 📖")
                    st.balloons()
                except Exception as e:
                    st.warning(f"Entry noted locally. Cloud save issue: {e}")
            else:
                st.warning("Please write something before saving.")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Motivation ---
    with tab4:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #1f3a60; text-align: center;">💫 Motivation & Inspiration Station</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Get the boost you need to keep moving forward</p>', unsafe_allow_html=True)
        
        if st.button("🌟 Get Personalized Motivation", use_container_width=True, key="motivation_btn"):
            current_language = st.session_state.current_language
            with st.spinner("✨ Creating some inspiration just for you..."):
                response = get_llm_response(
                    "Provide personalized motivational encouragement and inspiration", 
                    current_language, 
                    'motivation', 
                    llm, 
                    memory
                )
            st.markdown(f'<div class="custom-card">{response}</div>', unsafe_allow_html=True)
            if VOICE_AVAILABLE and enable_voice_responses:
                speak_text(response, language=current_language)
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Creative Space ---
    with tab5:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<h2 style="color: #1f3a60; text-align: center;">🎨 Creative Wellness Space</h2>', unsafe_allow_html=True)
        st.markdown('<p style="text-align: center; color: #666; font-size: 1.2rem;">Explore additional wellness resources and creative tools</p>', unsafe_allow_html=True)
        
        topic = st.text_input(
            "What wellness topic would you like to explore?", 
            placeholder="e.g., meditation techniques, stress management, self-care routines, sleep improvement...",
            key="wellness_topic_input"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if topic and st.button("🔍 Get Wellness Resources", use_container_width=True, key="resources_btn"):
                current_language = st.session_state.current_language
                with st.spinner(f"🌿 Gathering wellness resources about {topic}..."):
                    response = get_llm_response(
                        f"Provide comprehensive mental wellness advice, tips, and resources about: {topic}", 
                        current_language, 
                        'general', 
                        llm, 
                        memory
                    )
                st.markdown(f'<div class="custom-card">{response}</div>', unsafe_allow_html=True)
                if VOICE_AVAILABLE and enable_voice_responses:
                    speak_text(response, language=current_language)
        
        with col2:
            if IMAGE_AVAILABLE:
                if st.button("🖼️ Generate Inspirational Image", use_container_width=True, key="image_btn") and topic:
                    with st.spinner(f"🎨 Creating an inspirational visualization for {topic}..."):
                        response = execute_wellness_tool(
                            f"Generate inspirational image for: {topic}", 
                            f"Requested inspirational image for {topic}", 
                            memory, 
                            llm
                        )
                    st.success("🖼️ Image generated successfully!")
                    if isinstance(response, str) and response.startswith('http'):
                        st.image(response, caption=f"Inspirational visualization: {topic}", use_column_width=True)
            else:
                st.info("🎨 Image generation features coming soon!")
        
        st.markdown('</div>', unsafe_allow_html=True)

    # --- Conversation History ---
    st.markdown("---")
    st.markdown("## 💬 Your Wellness Journey History")
    
    try:
        if hasattr(memory, 'chat_memory') and hasattr(memory.chat_memory, 'messages'):
            messages = memory.chat_memory.messages
            if messages:
                for i, msg in enumerate(messages):
                    if i % 2 == 0:  # Human messages
                        st.markdown(f'<div style="background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%); padding: 15px; border-radius: 15px; margin: 10px 0px;"><strong>You:</strong> {msg.content}</div>', unsafe_allow_html=True)
                    else:  # AI messages
                        st.markdown(f'<div style="background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%); padding: 15px; border-radius: 15px; margin: 10px 0px;"><strong>Assistant:</strong> {msg.content}</div>', unsafe_allow_html=True)
                st.markdown("---")
            else:
                st.info("🌟 Your conversation history will appear here as you start using the features above!")
        else:
            st.info("🌟 Start exploring the features above to begin your wellness journey!")
            
    except Exception as e:
        st.info("🌟 Your wellness journey history will appear here as you use the app!")

    # --- Daily Wellness Tip ---
    st.markdown("---")
    st.markdown("## 🌞 Today's Personalized Wellness Tip")
    
    current_language = st.session_state.current_language
    daily_tip = get_llm_response(
        "Provide a brief, practical daily wellness tip or self-care reminder that is personalized and actionable", 
        current_language, 
        'motivation', 
        llm
    )
    st.markdown(f'<div class="success-message">{daily_tip}</div>', unsafe_allow_html=True)
    
    # Speak reminder button - only speaks when explicitly clicked
    if VOICE_AVAILABLE and st.button("🔊 Listen to This Tip", key="speak_tip_btn"):
        speak_text(daily_tip, language=current_language)

else:
    # Landing page matching your app's gradient theme
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <h2 style="color:#bd00ff; font-size: 3.5rem; margin-bottom: 25px; ">
            Welcome to Your Mental Wellness Journey! 
        </h2>
        <p style="color: 63A361; font-size: 1.6rem; margin-bottom: 40px;">
            Your AI companion for emotional support, mindfulness, and personal growth
        </p>
        <div  padding: 40px; border-radius: 25px;  border: 1px solid rgba(255,255,255,0.2);">
            <div style="color:#1581BF; text-align: center; font-size: 2.2rem; font-weight: bold;">
                <div style="margin: 15px 0;">🌐 Choose your preferred language</div>
                <div style="margin: 15px 0;">🔊 Configure voice settings</div>
                <div style="margin: 15px 0;">🎯 Click "Start Journey" in the sidebar</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# Footer with proper colors
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: blue; padding: 20px;'>"
    "🧘 Mental Wellness AI Companion | Your journey to emotional balance and inner peace starts here 🌟"
    "</div>",
    unsafe_allow_html=True
)

