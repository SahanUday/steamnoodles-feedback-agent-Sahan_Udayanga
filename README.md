# SteamNoodles Feedback Agent System

## 📝 Developer Information
- **Name:** Sahan Udayanga
- **University:** University of Moratuwa
- **Year:** 2025

## 🍜 Project Overview
This project consists of two intelligent agents for SteamNoodles restaurant chain:

1. **Feedback Analysis Agent:** Processes and responds to customer feedback with human-like, context-aware responses in multiple languages (English, Sinhala, Tamil).

2. **Sentiment Dashboard Agent:** Visualizes sentiment trends over time and generates analytical summaries of customer feedback.

The system leverages Google's Gemini model to analyze customer feedback, classify sentiment, determine urgency, identify emotions, and categorize feedback into business areas.

## 🚀 Approach Summary
My approach focused on creating a multi-functional feedback management system that:

- Uses LLM (Google's Gemini) for accurate sentiment analysis and multilingual response generation
- Provides real-time visualization of feedback trends
- Offers detailed category filtering and analysis
- Generates comprehensive summary reports for management
- Supports multilingual feedback handling (English, Sinhala, Tamil)

The architecture uses Flask for the backend API services and Streamlit for the interactive frontend dashboard.

## 🔧 Setup Instructions

### Prerequisites
- Python 3.10 or higher
- Git

### Installation Steps
1. Clone the repository:
   ```
   git clone https://github.com/SahanUday/steamnoodles-feedback-agent-Sahan_Udayanga.git
   cd steamnoodles-feedback-agent-Sahan_Udayanga
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv env
   # On Windows
   .\env\Scripts\activate
   # On macOS/Linux
   source env/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## 🧪 Testing the Agents

### Starting the Application
1. Start the Flask backend:
   ```
   python main.py
   ```

2. In a new terminal, start the Streamlit frontend:
   ```
   streamlit run app.py
   ```

3. Access the application in your browser at: http://localhost:8501

### Testing the Feedback Agent
1. Navigate to the "📨 Feedback Agent" page using the sidebar
2. Enter customer feedback in the text area
3. Click "Submit"
4. View the analyzed sentiment, urgency, emotion, category, and AI-generated response

#### Sample Prompts and Expected Outputs:

**Sample Feedback 1 (English):**
```
The food was excellent but the waiting time was too long. I had to wait for 30 minutes for my order.
```
**Expected Output:**
- Sentiment: Neutral
- Urgency: Medium
- Emotion: Frustration
- Category: Waiting Time
- Response: Thank you for your feedback! We're thrilled you enjoyed our food, but we're sorry about the long wait time. We're working to improve our service speed, and your patience is appreciated. We hope to serve you more efficiently on your next visit! 😊

**Sample Feedback 2 (Sinhala):**
```
ආහාරය සුපිරියි! අතිශයින් සතුටුයි!
```
**Expected Output:**
- Sentiment: Very Positive
- Urgency: Low
- Emotion: Joy
- Category: Food Quality
- Response: ඔබගේ ප්‍රශංසාත්මක ප්‍රතිචාරයට බොහොම ස්තුතියි! අපගේ ආහාර ගැන ඔබ සතුටු වී සිටින බව දැනගැනීමට ලැබීම අපට ඉතා සතුටක්. නැවත වරක් ඔබව සාදරයෙන් පිළිගන්නට බලාපොරොත්තු වෙනවා! 😊

### Testing the Sentiment Dashboard
1. Navigate to the "📊 Sentiment Dashboard" page using the sidebar
2. Select a time range (Last 7 Days, Last 30 Days, or Custom Range)
3. View the sentiment trend visualization
4. Click between "Show Trend Plot" and "Show Total Sentiment Pie Chart" to switch visualizations
5. Filter by feedback category to see specific feedback examples
6. Click "Generate Summary" to get an AI-generated analysis of the selected period

## 📊 Demo Output

### Feedback Analysis and Auto-Response Generation
[INSERT SCREENSHOT: Feedback agent analyzing a customer comment and generating a response]

The Feedback Agent analyzes customer input, determining sentiment, urgency, dominant emotion, and business category. It then generates a natural, context-aware response that matches the language and tone of the original feedback.

### Sentiment Trend Visualization
[INSERT SCREENSHOT: Line chart showing sentiment trends over time]

The Sentiment Dashboard displays trends of different sentiment categories over the selected time period, allowing managers to identify patterns and changes in customer satisfaction.

### Sentiment Distribution Pie Chart
[INSERT SCREENSHOT: Pie chart showing distribution of sentiment categories]

This visualization shows the overall distribution of sentiment categories within the selected time range, providing an at-a-glance view of customer satisfaction levels.

### Feedback Category Selection
[INSERT SCREENSHOT: Category filter buttons and example feedback]

Users can filter feedback by business categories like Food Quality, Pricing, and Delivery to focus on specific aspects of the business that may need attention.

### Summary Report Generation
[INSERT SCREENSHOT: AI-generated summary report]

The system can generate comprehensive summaries of customer sentiment for any selected time period, highlighting key trends, successes, and areas for improvement.

## 🎯 Evaluation Criteria

| Criteria | Weight | Description |
|----------|--------|-------------|
| Functionality of both agents | 40% | Both the Feedback Analysis Agent and Sentiment Dashboard Agent function as intended, providing accurate analysis, responses, and visualizations |
| Use of LLMs + Sentiment logic | 25% | Effective implementation of Google's Gemini model for sentiment analysis, classification, and response generation with appropriate prompting strategies |
| Code quality & documentation | 20% | Clean, modular code with proper error handling, comments, and comprehensive documentation |
| Innovation & improvements | 15% | Added features like multilingual support, detailed categorization, and comprehensive visualization options |

## 🎬 Demo Video
[INSERT LINK TO DEMO VIDEO]

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.