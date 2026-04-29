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
def simplify_text_with_gemini(text, target_level="12th grade", language="English"):
    try:
        # 1. DEFINE THE MODEL (This was the missing line!)
        import google.generativeai as genai
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 2. Set up your prompt
        prompt = f"""
        You are an expert science communicator. 
        Analyze the following academic abstract and simplify it for a {target_level} reading level in {language}.
        
        Abstract text:
        {text}
        
        Provide the output in JSON format with these exact keys:
        - core_finding (a 1-sentence summary)
        - plain_summary (a 2-3 paragraph simple explanation)
        - key_takeaways (a list of 3-5 bullet points)
        - glossary (a dictionary of 2-3 hard words and their simple definitions)
        """
        
        # 3. Call the AI
        response = model.generate_content(prompt)
        
        # 4. Parse the result (assuming you have your JSON parsing code here)
        import json
        # Strip markdown formatting if Gemini returns it inside code blocks
        clean_text = response.text.replace("```json", "").replace("```", "").strip()
        result = json.loads(clean_text)
        return result

    except Exception as e:
        # THE BULLETPROOF ERROR CATCHER
        error_message = str(e)
        if "429" in error_message or "Quota" in error_message:
            return {"error": "⏳ The AI is receiving too many requests right now. Please wait 10 seconds and click simplify again!"}
        elif "400" in error_message or "API_KEY_INVALID" in error_message:
            return {"error": "🔑 The API key is invalid or expired. Please check your settings."}
        else:
            return {"error": f"⚠️ An unexpected error occurred: {error_message}"}