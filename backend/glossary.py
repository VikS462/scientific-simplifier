import re
from collections import Counter
import textstat

def detect_jargon(text: str, num_terms: int = 5) -> list:
    """
    Scans the abstract and identifies complex technical terms 
    based on syllable count and word length.
    """
    if not text:
        return []
        
    # Extract all alphabetic words (removes numbers and punctuation)
    words = re.findall(r'\b[A-Za-z]+\b', text)
    
    jargon_candidates = []
    for word in words:
        # A word is likely jargon if it is long AND has 3 or more syllables
        if len(word) >= 9 and textstat.syllable_count(word) >= 3:
            jargon_candidates.append(word.lower())
            
    # Count frequencies to find the most prominent complex words
    word_counts = Counter(jargon_candidates)
    
    # Extract just the words (ignoring the count numbers)
    top_jargon = [word for word, count in word_counts.most_common(num_terms)]
    
    return top_jargon