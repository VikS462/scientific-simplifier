import os
import json
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv

# Load the secret API key from your .env file
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    # Fallback for local testing
    import os
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)
@st.cache_data(show_spinner=False)

def simplify_text_with_gemini(text: str, target_level: str = "8th grade", language: str = "English") -> dict:
    """
    Sends the abstract to Gemini and forces a JSON response 
    containing the summary, takeaways, finding, and glossary.
    """
    # Gemini 2.5 Flash is perfect here: it's incredibly fast and very cheap/free
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # This is the "System Prompt" that controls how the AI behaves
    system_instruction = f"""
    You are an expert science communicator. Your job is to simplify complex scientific abstracts.
    Output your response STRICTLY as a JSON object with the following exact keys:
    - "core_finding": 1 simple sentence summarizing the main discovery.
    - "plain_summary": A 2-3 sentence summary at an {target_level} reading level.
    - "key_takeaways": A list of 3-4 bullet points.
    - "glossary": A dictionary mapping 3-5 technical terms to simple definitions.
    """
    
    prompt = f"{system_instruction}\n\nAbstract Text to Simplify:\n{text}"
    
    try:
        # We enforce JSON output so our frontend can easily map the data to the screen
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        # Convert the raw JSON string from Google into a usable Python dictionary
        return json.loads(response.text)
        
    except Exception as e:
        # Failsafe in case the API glitches or the prompt fails
        return {"error": f"Failed to process with Gemini: {str(e)}"}
def simplify_text_with_gemini(text: str, target_level: str = "8th grade", language: str = "English") -> dict:
    """
    Sends the abstract to Gemini and forces a JSON response 
    containing the summary, takeaways, finding, glossary, and domain.
    Translated to the requested language.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # Updated Prompt: Added domain detection and translation commands
    system_instruction = f"""
    You are an expert science communicator. Analyze the provided abstract.
    Output your response STRICTLY as a JSON object with the following exact keys:
    - "domain": Detect the scientific field (e.g., Biology, Physics, Computer Science). Write this in English.
    - "core_finding": 1 simple sentence summarizing the main discovery. Translate this to {language}.
    - "plain_summary": A 2-3 sentence summary at an {target_level} reading level. Translate this to {language}.
    - "key_takeaways": A list of 3-4 bullet points. Translate these to {language}.
    - "glossary": A dictionary mapping 3-5 technical terms (keep terms in English, but translate the definitions to {language}).
    """
    
    prompt = f"{system_instruction}\n\nFull Research Paper Text to Simplify:\n{text}"
    
    try:
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        return json.loads(response.text)
        
    except Exception as e:
        return {"error": f"Failed to process with Gemini: {str(e)}"}