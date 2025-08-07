import os
import google.generativeai as genai
from sentiment import detect_mood

def get_llm_response(message: str) -> str:
    """
    Gets a response from the Google Gemini model.
    """
    if not os.environ.get("GOOGLE_API_KEY"):
        return "Sorry, the Google API key is not configured."

    system_prompt = f"""
    You are a friendly and caring chatbot in a lofi-themed chat app. Your responses must be short, concise, and easy to read, aiming for 2-4 sentences.

    **CRITICAL RULE:** If the user mentions feeling suicidal, wanting to die, or self-harm, your ONLY response must be:
    "It sounds like you are going through a lot. Please reach out for immediate help. You can call the Vandrevala Foundation Helpline at 9999666555. They are there for you."

    For all other messages, listen to the user and offer gentle, supportive advice for their feelings. **Crucially, always end your response with a gentle, open-ended question to keep the conversation going and encourage the user to share more.**

    User's message: "{message}"
    """

    try:
        genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(system_prompt)

        if not response.parts:
            if response.prompt_feedback.block_reason:
                print(f"Response blocked due to: {response.prompt_feedback.block_reason.name}")
            return "My thoughts were blocked. Please try rephrasing your message."
        return response.text.strip()

    except Exception as e:
        print(f"An error occurred while connecting to the AI model: {e}")
        return print(f"An error occurred while connecting to the AI model: {e}")


def get_bot_response(message: str, music_recommended: bool) -> dict:
    """
    Analyzes the message and returns the AI response.
    A mood for music is only included if music_recommended is False.
    """
    base_response = get_llm_response(message)
    response_data = {"reply": base_response, "mood": None}

    if not music_recommended:
        mood = detect_mood(message)
        response_data["mood"] = mood
    
    return response_data
