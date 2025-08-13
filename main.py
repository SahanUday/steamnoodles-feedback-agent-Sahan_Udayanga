from flask import Flask, request, jsonify
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from datetime import datetime
import os, csv, pandas as pd

load_dotenv()
app = Flask(__name__)
api_key = os.getenv("GOOGLE_API_KEY")
llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key)

summary_prompt_template = """
You are an expert customer feedback analyst. Given the counts of customer feedback sentiments in a selected period, write a concise, insightful summary report.

Sentiment Counts:
Very Positive: {very_positive}
Positive: {positive}
Neutral: {neutral}
Negative: {negative}
Very Negative: {very_negative}

Summarize the overall customer sentiment trend, highlighting notable positives and areas needing urgent attention.
"""

@app.route("/generate_summary", methods=["POST"])
def generate_summary():
    data = request.get_json()
    start_date_str = data.get("start_date")
    end_date_str = data.get("end_date")
    if not start_date_str or not end_date_str:
        return jsonify({"error": "start_date and end_date are required"}), 400

    try:
        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    # Read CSV and filter by date
    if not os.path.isfile("steamnoodles_feedback_dataset.csv"):
        return jsonify({"error": "Feedback dataset not found."}), 404

    df = pd.read_csv("steamnoodles_feedback_dataset.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"]).dt.date

    filtered = df[(df["timestamp"] >= start_date) & (df["timestamp"] <= end_date)]
    counts = filtered["sentiment"].value_counts().to_dict()

    very_positive = counts.get("Very Positive", 0)
    positive = counts.get("Positive", 0)
    neutral = counts.get("Neutral", 0)
    negative = counts.get("Negative", 0)
    very_negative = counts.get("Very Negative", 0)

    # Collect actual feedback texts for very positive and very negative
    very_positive_feedbacks = filtered[filtered["sentiment"] == "Very Positive"]["feedback"].tolist()
    very_negative_feedbacks = filtered[filtered["sentiment"] == "Very Negative"]["feedback"].tolist()

    # Format feedbacks for prompt
    very_positive_text = "\n".join(very_positive_feedbacks[:5]) if very_positive_feedbacks else "None"
    very_negative_text = "\n".join(very_negative_feedbacks[:5]) if very_negative_feedbacks else "None"

    prompt = f"""
Your summary MUST mention both the very positive and very negative feedbacks, using provided counts and using the sample comments and counts to highlight key strengths and urgent issues. 
Summarize the overall customer sentiment trend, notable positives, and areas needing immediate attention. Do not include any heading or title in your summary.
Generate paragraphs that are coherent and contextually relevant, ensuring a smooth flow of ideas.
Add last paragraph by including overall overveiw of the summarize

Sentiment Counts:
Very Positive: {very_positive}
Positive: {positive}
Neutral: {neutral}
Negative: {negative}
Very Negative: {very_negative}

Sample Very Positive Feedbacks:
{very_positive_text}

Sample Very Negative Feedbacks:
{very_negative_text}

Summarize the overall customer sentiment trend, highlighting notable positives and areas needing urgent attention. Use the sample feedbacks to provide concrete examples in your summary.
"""

    try:
        summary = llm.invoke(prompt).strip()
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PROMPT 1: Feedback analysis (analytics + category classification)
analysis_prompt = PromptTemplate.from_template(
    """
You are a feedback analysis assistant for SteamNoodles, a rapidly growing restaurant chain.

Analyze the following customer feedback and provide:
1. Fine-grained sentiment (Very Negative / Negative / Neutral / Positive / Very Positive)
2. Urgency level (Low / Medium / High)
3. Dominant customer emotion (anger, joy, frustration, gratitude, disappointment, etc.)
4. Business category (one of: Food Quality, Delivery, Customer Service, Pricing, Cleanliness, Take away, Waiting Time, Other)

Only return your answer in this exact format:
Sentiment: <sentiment>
Urgency: <urgency>
Emotion: <emotion>
Category: <category>

Feedback:
"{feedback}"
"""
)

# PROMPT 2: Human-like response generation with multilingual support
response_prompt = PromptTemplate.from_template(
    """
You are a warm, emotionally intelligent automated customer support responder of the restaurant.
You automatically write replies to customer feedbacks.
Your task is to generate a short, natural, context-aware and kind reply based on the feedback, sentiment, urgency, and emotion. Adapt the tone to match the emotion and urgency.

RULES:
- Use the **same language(eg: සිංහල->සිංහල) or transliteration style(e.g., Singlish:Sinhala in English letters → සිංහල)** as the feedback .
- Always reply in the **same language and writing style** as the customer's original feedback.
- If feedback is in Sinhala, reply in Sinhala.
- If it's Tamil, reply in Tamil.
- If it's English, reply in English.
- If feedback is Sinhala/Tamil typed using English letters (like Singlish or Tanglish), reply using the Sinhala or Tamil (not typed using English letters).
- Do NOT use formal or overly structured grammar in such cases.
- Avoid robotic or unnatural phrasing. Make it sound like a human wrote it, not robotic or overly structured.
- Never ask follow-up questions. This is a one-way automatic reply.
- Express empathy, kindness, and a sense of care.
- Match the tone to the customer's emotion and urgency.
- Use emojis to enhance warmth and empathy.

Given the customer's feedback, sentiment, urgency, and emotion as follows,
write a short, natural, context-aware and kind reply based on the feedback,sentiment, urgency,emotion. Adapt the tone to match the emotion and urgency.

Feedback: {feedback}
Sentiment: {sentiment}
Urgency: {urgency}
Emotion: {emotion}

Reply:
"""
)

CSV_FILE = "steamnoodles_feedback_dataset.csv"

def save_to_csv(feedback, sentiment, urgency, emotion, category, reply, filename=CSV_FILE):
    file_exists = os.path.isfile(filename)
    with open(filename, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "feedback", "sentiment", "urgency", "emotion", "category"])
        writer.writerow([datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), feedback, sentiment, urgency, emotion, category])

@app.route("/analyze_feedback", methods=["POST"])
def analyze_feedback():
    data = request.get_json()
    feedback = data.get("feedback", "").strip()
    if not feedback:
        return jsonify({"error": "Feedback is required"}), 400

    try:
        analysis = llm.invoke(analysis_prompt.format(feedback=feedback)).strip()
        sentiment = analysis.split("Sentiment:")[1].split("\n")[0].strip()
        urgency = analysis.split("Urgency:")[1].split("\n")[0].strip()
        emotion = analysis.split("Emotion:")[1].split("\n")[0].strip()
        category = analysis.split("Category:")[1].strip()

        response = llm.invoke(response_prompt.format(
            feedback=feedback,
            sentiment=sentiment,
            urgency=urgency,
            emotion=emotion
        )).strip()

        save_to_csv(feedback, sentiment, urgency, emotion, category, response)

        return jsonify({
            "sentiment": sentiment,
            "urgency": urgency,
            "emotion": emotion,
            "category": category,
            "reply": response
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000)
