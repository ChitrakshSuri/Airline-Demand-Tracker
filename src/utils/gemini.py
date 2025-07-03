import google.generativeai as genai
import os

# Load API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_flight_insights_from_gemini(df):
    prompt = f"""
You are an AI analyst. Summarize key insights from this flight dataset:
- Popular routes
- Most common airlines
- High-traffic periods
- Trends or patterns

Dataset (20 rows):
{df.head(20).to_string(index=False)}
    """

    # ✅ Using Gemini 1.5 Flash
    model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")

    response = model.generate_content(prompt)
    return response.text
