import textstat

def get_readability_score(text: str) -> float:
    """
    Returns the Flesch Reading Ease score.
    Higher score = easier to read.
    """
    if not text or len(text.strip()) == 0:
        return 0.0
    return textstat.flesch_reading_ease(text)

def get_grade_level(text: str) -> str:
    """
    Returns a string representing the estimated school grade 
    level required to understand the text (e.g., '8th and 9th grade').
    """
    if not text or len(text.strip()) == 0:
        return "N/A"
    return textstat.text_standard(text)