from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
import os
import csv
from datetime import datetime

# Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini
llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=api_key)

# PROMPT 1: Feedback analysis (for analytics only)
analysis_prompt = PromptTemplate.from_template(
    """
You are a feedback analysis assistant.

Analyze the following feedback and provide:
1. Fine-grained sentiment (Very Negative / Negative / Neutral / Positive / Very Positive)
2. Urgency level (Low / Medium / High)
3. Dominant customer emotion (anger, joy, frustration, gratitude, disappointment, etc.)

Only return your answer in this exact format:
Sentiment: <sentiment>
Urgency: <urgency>
Emotion: <emotion>

Feedback:
"{feedback}"
"""
)

# PROMPT 2: Human-like response generation
response_prompt = PromptTemplate.from_template(
    """
You are a polite and emotionally intelligent automated customer support responder for automatically responding to customer reviews.
Given the customer's feedback, sentiment, urgency, and emotion,
write a short, natural, context-aware and kind reply. Adapt the tone to match the emotion and urgency.

Feedback: "{feedback}"
Sentiment: {sentiment}
Urgency: {urgency}
Emotion: {emotion}

Reply:
"""
)

# CSV log file
CSV_FILE = "feedback_log.csv"

# Save all to CSV
def save_to_csv(feedback, sentiment, urgency, emotion, reply, filename=CSV_FILE):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "feedback", "sentiment", "urgency", "emotion", "reply"])
        writer.writerow([datetime.now().isoformat(), feedback, sentiment, urgency, emotion, reply])

# Main logic
def main():
    print("📨 Feedback Agent (type 'exit' to quit)\n")
    while True:
        feedback = input("Enter customer feedback:\n> ").strip()
        if feedback.lower() == "exit":
            print("👋 Exiting.")
            break

        # Step 1: Analyze feedback
        analysis_query = analysis_prompt.format(feedback=feedback)
        analysis_result = llm.invoke(analysis_query).strip()

        try:
            sentiment = analysis_result.split("Sentiment:")[1].split("\n")[0].strip()
            urgency = analysis_result.split("Urgency:")[1].split("\n")[0].strip()
            emotion = analysis_result.split("Emotion:")[1].strip()
        except Exception as e:
            print("❌ Error parsing analysis result:", e)
            print("Raw output:\n", analysis_result)
            continue

        # Step 2: Generate response
        response_query = response_prompt.format(
            feedback=feedback,
            sentiment=sentiment,
            urgency=urgency,
            emotion=emotion
        )
        reply = llm.invoke(response_query).strip()

        # Step 3: Print and save
        print(f"\n🔍 Sentiment: {sentiment}")
        print(f"⚡ Urgency: {urgency}")
        print(f"🎭 Emotion: {emotion}")
        print(f"💬 Reply: {reply}\n")
        save_to_csv(feedback, sentiment, urgency, emotion, reply)
        print("✅ Saved to feedback_log.csv\n" + "-"*50)

if __name__ == "__main__":
    main()
