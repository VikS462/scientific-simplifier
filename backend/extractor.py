import fitz  # PyMuPDF library for PDF processing
import requests
import re

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Takes an uploaded PDF file stream, loops through EVERY page, 
    and combines the text so the AI can read the entire paper.
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        full_text = ""
        # Loop through all the pages in the document
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            full_text += page.get_text() + "\n\n"
            
        doc.close()
        return full_text
        
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


def fetch_abstract_from_doi(doi: str) -> str:
    """
    Pings the free CrossRef metadata API to grab an abstract 
    using a Digital Object Identifier (DOI).
    """
    # Clean the input in case the user pastes a full URL instead of just the DOI
    clean_doi = doi.replace("https://doi.org/", "").strip()
    url = f"https://api.crossref.org/works/{clean_doi}"
    
    try:
        # We add a 10-second timeout so the app doesn't hang if the API is slow
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            # Safely check if 'abstract' exists in the returned data
            abstract = data['message'].get('abstract')
            
            if abstract:
                # CrossRef often returns text wrapped in XML tags like <jats:p>
                # This regex removes those formatting tags for clean text
                clean_abstract = re.sub(r'<[^>]+>', '', abstract)
                return clean_abstract
            else:
                return "No abstract found in the database for this DOI."
        else:
            return f"Error: Received status code {response.status_code} from CrossRef."
            
    except requests.exceptions.RequestException as e:
        return f"Error connecting to CrossRef API: {str(e)}"
def fetch_citation(doi: str, style: str = "apa") -> str:
    """Fetches formatted citation using CrossRef content negotiation."""
    clean_doi = doi.replace("https://doi.org/", "").strip()
    url = f"https://api.crossref.org/works/{clean_doi}/transform/text/x-bibliography?style={style}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.text.strip()
    except:
        return "Could not generate citation."