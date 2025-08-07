# from transformers import pipeline

# try:
#     sentiment_pipeline = pipeline(
#         "sentiment-analysis", 
#         model="distilbert-base-uncased-finetuned-sst-2-english"
#     )
# except Exception as e:
#     print(f"Error loading sentiment analysis model: {e}")
#     # In case of an error, create a dummy pipeline to avoid crashing the app.
#     sentiment_pipeline = None

# def detect_mood(text: str) -> str:
#     """
#     Analyzes the sentiment of the text and returns a corresponding mood.
#     - User message contains neutral/chill keywords -> "chill"
#     - POSITIVE sentiment -> "happy"
#     - NEGATIVE or other -> "mellow"
#     """
#     # --- New: Check for neutral/chill keywords first ---
#     chill_keywords = ["bored", "calm", "relaxed", "nothing", "meh", "okay", "alright", "fine"]
#     lower_text = text.lower()
#     if any(keyword in lower_text for keyword in chill_keywords):
#         return "chill"

#     # If the model failed to load, return a default mood.
#     if not sentiment_pipeline:
#         return "mellow"

#     try:
#         # If no chill keywords, proceed with sentiment analysis
#         result = sentiment_pipeline(text)[0]
#         label = result['label']
        
#         if label == "POSITIVE":
#             return "happy"
#         else:
#             return "mellow"
            
#     except Exception as e:
#         print(f"Error during sentiment analysis: {e}")
#         return "mellow"


# sentiment.py

from textblob import TextBlob

def detect_mood(text: str) -> str:
    """
    Analyzes the sentiment of the text using TextBlob and returns a mood.
    - Polarity > 0.1  -> "happy"
    - Polarity < -0.1 -> "mellow"
    - Otherwise       -> "chill"
    """
    try:
        # Create a TextBlob object
        blob = TextBlob(text)
        
        # Get the polarity score (-1.0 to 1.0)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return "happy"
        elif polarity < -0.1:
            return "mellow"
        else:
            return "chill"
            
    except Exception as e:
        print(f"Error during TextBlob sentiment analysis: {e}")
        # Return a safe default mood in case of an error.
        return "mellow"


