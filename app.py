import streamlit as st
import base64
import os
from groq import Groq
from dotenv import load_dotenv
import markdown

# ============================
# PAGE CONFIG
# ============================
st.set_page_config(page_title="GitaGPT", page_icon="🕉️", layout="wide")





# ============================
# HELPER: LOAD IMAGE AS BASE64
# ============================
def get_img_as_base64(file_path):
    """Reads a local image and converts it to base64 for HTML embedding."""
    if not os.path.exists(file_path):
        return "" # Return empty if file not found
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def get_img_base64(file_path):
    """Reads a local image and converts it to base64 for HTML embedding."""
    if not os.path.exists(file_path):
        return "" # Return empty if file not found
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Load the Krishna image
krishna_img_base64 = get_img_as_base64("krishna (1).png")
arjuna_img_base64 = get_img_base64("arjuna.png")

# ============================
# CUSTOM CSS (EXACT DESIGN)
# ============================
st.markdown(f"""
<style>
/* Main Background */
body {{
    background-color: #ffffff;
}}
header[data-testid="stHeader"] {{ visibility: hidden; }} /* Hide Default Header */
                       
/* 2. Custom Orange Header Bar */
.custom-header {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 70px;
    background-color: #ff9800; /* Exact Orange */
    display: flex;
    align-items: center;
    padding-left: 20px;
    padding-right: 20px;
    z-index: 99; /* Sit below the popover button */
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}}

.header-avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 15px;
    
    border: 2px solid white;
}}

.header-title {{
    color: white;
    font-size: 20px;
    font-weight: bold;
    font-family: sans-serif;
}}



/* 4. Chat Area Spacing */
.chat-container {{
    margin-top: 60px; /* Push chat down so it doesn't hide behind header */
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
    padding-bottom: 20px;
}}

/* General Row Styles */
.chat-row {{
    display: flex;
    margin-bottom: 20px;
    width: 100%;
    align-items: flex-start;
}}

/* --- USER STYLES --- */
.user-row {{
    justify-content: flex-end;
}}

.user-bubble {{
    background-color: #ff9800; /* Exact Orange */
    color: white;
    padding: 12px 18px;
    border-radius: 18px 0px 18px 18px; /* Pointed top-right */
    max-width: 70%;
    font-size: 16px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    line-height: 1.5;
}}

/* --- BOT STYLES --- */
.bot-row {{
    justify-content: flex-start;
}}

/* Container for Avatar and Text */
.bot-content-wrapper {{
    display: flex;
    flex-direction: column;
    max-width: 75%;
}}

/* Avatar Image */
.bot-avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
    margin-right: 12px;
    margin-top: 5px;
}}
.user-avatar {{
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-left: 12px; /* Pushes image away from bubble */
}}

/* Bot Name Label */
.bot-name {{
    font-weight: bold;
    font-size: 14px;
    color: #333;
    margin-bottom: 4px;
    margin-left: 5px;
}}
            


.bot-bubble {{
    background-color: #f0f2f6; /* Light Streamlit Gray */
    color: #31333F;
    padding: 15px 20px;
    border-radius: 0px 18px 18px 18px; /* Pointed top-left */
    font-size: 16px;
    line-height: 1.6;
}}

/* Hide standard Streamlit header/footer elements if desired */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

</style>
""", unsafe_allow_html=True)




# ============================
# RENDER HEADER (HTML)
# ============================
# This renders the visual orange bar
img_tag = f'<img src="data:image/png;base64,{krishna_img_base64}" class="header-avatar">' if krishna_img_base64 else ''
st.markdown(f"""
    <div class="custom-header">
        {img_tag}
        <div class="header-title">GitaGPT</div>
    </div>
""", unsafe_allow_html=True)



    
    



# ============================
# LOAD GROQ CLIENT
# ============================
@st.cache_resource(show_spinner=False)
def get_groq_client():
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        # Fallback for demo purposes if env not set, remove in production
        return None 
    return Groq(api_key=api_key)

# ============================
# SESSION STATE & WELCOME MSG
# ============================
if "messages" not in st.session_state:
    # Initialize with the specific greeting from your screenshot
    st.session_state.messages = [
        {"role": "assistant", "content": "Radhey Radhey, I am GitaGPT. Ask me anything."}
    ]

# ============================
# SYSTEM PROMPT
# ============================

system_prompt = """
You are GitaGPT — a warm, compassionate, emotionally intelligent spiritual companion inspired by the Bhagavad Gita.

Your personality:
- Gentle, calm, loving, and devotional.
- Speak like a caring guide, not like a textbook.
- Never sound like an academic article.
- Always be emotionally aware of the user's feeling.

GREETING BEHAVIOR:
When the user greets (e.g., "Radhe Radhe", "Jai Shri Krishna"):
- Reply with warmth and devotion.
- Keep it short and heartfelt.
- Do NOT give long philosophy unless the user asks.
- You MAY softly include a one-line uplifting thought inspired by the Gita (no heavy explanation).

EMOTIONAL SUPPORT BEHAVIOR:
When the user shares sadness, fear, anxiety, confusion, loneliness:
1. First respond with empathy and warmth.
2. Then gently connect their feeling to a teaching of the Bhagavad Gita.
3. ALWAYS include:
   - Either a short paraphrased verse idea
   - OR a direct short verse quote with chapter & verse.
4. VERY IMPORTANT:
   - Whenever you mention a verse (quoted or paraphrased),
     you MUST also explain its meaning in 1–2 very simple, practical sentences.
5. Keep verse usage natural and comforting — never forced.
6. After that, gently offer options like:
   - “Would you like a verse for today?”
   - “Would you like a small calming practice?”
   - “Would you like to talk more?”

VERY IMPORTANT TONE RULES:
- Short, warm sentences.
- Soft language.
- Human-like.
- Never over-explain.
- Never sound like an encyclopedia or motivational poster.

FORMAT RULES:
- Use **Bold** for key spiritual concepts or verse numbers.
- Short paragraphs.
- Blank line between sections.
- Bullet points only if truly needed.
- Emojis only when they add warmth (🌸🙏✨).

LANGUAGE RULE:
- Primary language: English.
- If the user types in Hindi, reply in Hindi.
- You may gently mix simple Hindi if the user does.

GITA USAGE RULE (IMPORTANT):
- When giving guidance, ALWAYS base it clearly on the Bhagavad Gita.
- You must either:
  a) Paraphrase a real Gita teaching clearly, OR
  b) Quote a short verse with Chapter & Verse.
  1) Give **one real verse from the Bhagavad Gita**.  
  2) First write it in **Sanskrit** (in Devanagari or IAST) in next.  
  3) Then give its **English translation** in next line .  
  4) Then give a **simple 1-3 line explanation** in very plain language. 
  
- Do NOT invent verses.
- Do NOT give long scripture explanations unless the user asks.
- BUT you MUST always give a brief, simple explanation of any verse you reference.

YOUR PURPOSE:
Not to teach philosophy —
but to **comfort, guide, and gently awaken strength using the wisdom of the Bhagavad Gita in a living, human way.**
"""


# ============================
# CHAT DISPLAY LOGIC
# ============================
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["role"] == "user":
        # Render User Message (Right Aligned, Orange)

      user_img_tag = f'<img src="data:image/png;base64,{arjuna_img_base64}" class="user-avatar">' if arjuna_img_base64 else '<div class="user-avatar" style="background:#ddd;">👤</div>'
        
      st.markdown(f"""
            <div class="chat-row user-row">
                <div class="user-bubble">{msg["content"]}</div>
                {user_img_tag}
            </div>
        """, unsafe_allow_html=True)
      
        
    else:
        # Render Bot Message (Left Aligned, Gray, with Avatar & Name)
        
        # We need to process newlines/markdown slightly for HTML display if using raw divs
        # For simplicity in raw HTML, we replace newlines with <br> or use a markdown parser
        # Here we rely on Streamlit's markdown processing by injecting the content cleanly.
        
        # NOTE: To render formatting inside the HTML bubble properly, we need to simple replacement
        #formatted_content = msg["content"].replace("\n", "<br>")
        html_content = markdown.markdown(msg["content"])
        # If you have the image, use it, otherwise use a placeholder emoji
        img_tag = f'<img src="data:image/png;base64,{krishna_img_base64}" class="bot-avatar">' if krishna_img_base64 else '<div class="bot-avatar" style="background:#ddd;display:flex;align-items:center;justify-content:center;">🕉️</div>'
        
        st.markdown(f"""
            <div class="chat-row bot-row">
                {img_tag}
                <div class="bot-content-wrapper">
                    <div class="bot-name">GitaGPT</div>
                    <div class="bot-bubble">{ html_content}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ============================
# USER INPUT
# ============================
# Create a placeholder for the input to keep it at bottom
user_input = st.chat_input("Ask me anything...")

if user_input:
    # 1. Add user message to state
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # 2. Rerun immediately to show user message
    #    (We can't rerun immediately inside the button callback easily without experimental_rerun)
    #    Instead, we process, then rerun.
    
    client = get_groq_client()
    if client:
        try:
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                ] + st.session_state.messages,
                temperature=0.7,
            )
            answer = chat_completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please set GROQ_API_KEY in .env file")

    st.rerun()