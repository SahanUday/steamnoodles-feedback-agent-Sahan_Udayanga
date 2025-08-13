import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="SteamNoodles Feedback Agents", page_icon="🍜", layout="wide")

# ---- Sidebar Navigation with Buttons ----
st.sidebar.title("🍜 SteamNoodles")

if 'page' not in st.session_state:
    st.session_state.page = "📨 Feedback Agent"

if st.sidebar.button("📨 Feedback Agent"):
    st.session_state.page = "📨 Feedback Agent"
if st.sidebar.button("📊 Sentiment Dashboard"):
    st.session_state.page = "📊 Sentiment Dashboard"

page = st.session_state.page

# ---- Agent 1: Feedback Analyzer ----
if page == "📨 Feedback Agent":
    st.title("📨 Feedback Agent")
    st.markdown("##### Enter customer feedback.")
    with st.form("feedback_form"):
        feedback = st.text_area("📝 Customer Feedback", height=150)
        submitted = st.form_submit_button(" Submit ")

    if submitted and feedback:
        with st.spinner("Please wait...."):
         
            res = requests.post("http://localhost:5000/analyze_feedback", json={"feedback": feedback})
            data = res.json()
            if "reply" in data:
                st.success("✅ Feedback processed successfully!")
                st.markdown("### 💬 Auto-Generated Response")
                st.markdown(data['reply'].replace("\n", "  \n"))

# ---- Agent 2: Sentiment Visualization ----
elif page == "📊 Sentiment Dashboard":
    st.title("📊 Sentiment Trend Dashboard")

    df = pd.read_csv("steamnoodles_feedback_dataset.csv")
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    today = datetime.today().date()

    range_option = st.selectbox(
        "Select time range",
        options=["Last 7 Days", "Last 30 Days", "Custom Range"],
        index=0
    )

    if range_option == "Last 7 Days":
        start_date = today - timedelta(days=7)
        end_date = today
    elif range_option == "Last 30 Days":
        start_date = today - timedelta(days=30)
        end_date = today
    else:
        start_date = st.date_input("Start date", today - timedelta(days=7))
        end_date = st.date_input("End date", today)

    if start_date > end_date:
        st.error("❌ Start date must be before or equal to end date.")
        st.stop()

    mask = (df["timestamp"].dt.date >= start_date) & (df["timestamp"].dt.date <= end_date)
    filtered_df = df.loc[mask]

    if filtered_df.empty:
        st.info("No feedback entries found in this range.")
    else:
        trend_df = filtered_df.groupby([filtered_df["timestamp"].dt.date, "sentiment"]).size().reset_index(name="count")
        trend_df.columns = ["date", "sentiment", "count"]

        st.markdown("## 👆 Select Visualization Type")
        col1, col2 = st.columns(2)
        with col1:
            show_trend = st.button("📈 Show Trend Plot")
        with col2:
            show_pie = st.button("🥧 Show Total Sentiment Pie Chart")

        if ("show_trend" not in st.session_state) and ("show_pie" not in st.session_state):
            st.session_state.show_trend = True
            st.session_state.show_pie = False
        if show_trend:
            st.session_state.show_trend = True
            st.session_state.show_pie = False
        if show_pie:
            st.session_state.show_trend = False
            st.session_state.show_pie = True

        if st.session_state.show_trend:
            st.markdown("## 📈 Sentiment Trends Over Time")
            fig_line = px.line(trend_df, x="date", y="count", color="sentiment", markers=True,
                               title="Sentiment Counts by Day",
                               labels={"count": "Feedback Count", "date": "Date"},
                               hover_data={"count": True, "sentiment": True, "date": True})
            fig_line.update_layout(hovermode="x unified")
            fig_line.update_traces(mode="lines+markers")
            st.plotly_chart(fig_line, use_container_width=True)

        elif st.session_state.show_pie:
            total_counts = filtered_df['sentiment'].value_counts().reset_index()
            total_counts.columns = ['sentiment', 'count']

            st.markdown("## 🥧 Total Sentiment Distribution")
            fig_pie = px.pie(total_counts, values='count', names='sentiment',
                             title="Overall Sentiment Distribution in Selected Period",
                             color='sentiment',
                             color_discrete_map={
                                 "Very Positive": "green",
                                 "Positive": "lightgreen",
                                 "Neutral": "gray",
                                 "Negative": "orange",
                                 "Very Negative": "red"
                             })
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)

        # Generate Summary button & display summary

        st.markdown("### 📂 Select Feedback Category")

        categories = ["Food Quality", "Pricing", "Cleanliness", "Delivery", "Other"]

        if "selected_category" not in st.session_state:
            st.session_state.selected_category = None

        col_cat = st.columns(len(categories))
        for idx, cat in enumerate(categories):
            if col_cat[idx].button(cat):
                if st.session_state.selected_category == cat:
                    st.session_state.selected_category = None  # unselect if same clicked
                else:
                    st.session_state.selected_category = cat

        # Show example feedback for selected category
        if st.session_state.selected_category:
            st.markdown(f"#### ✨ Example Feedback for **{st.session_state.selected_category}**")

            # Ensure your dataset has a 'category' column, else you need logic to assign categories
            if "category" in filtered_df.columns:
                examples_df = filtered_df[filtered_df["category"] == st.session_state.selected_category]
            else:
                examples_df = pd.DataFrame(columns=df.columns)  # fallback empty

            if not examples_df.empty:
                sample_texts = examples_df["feedback"].dropna().sample(min(5, len(examples_df)), random_state=42)
                for i, fb in enumerate(sample_texts, 1):
                    st.markdown(f"**{i}.** {fb}")
            else:
                st.info("No feedback found for this category in the selected date range.")

        st.markdown(f"### 📝 Summary Report")

        if st.button("📝 Generate Summary"):
            with st.spinner("Generating summary..."):
           
                res = requests.post(
                    "http://localhost:5000/generate_summary",
                    json={
                        "start_date": start_date.strftime("%Y-%m-%d"),
                        "end_date": end_date.strftime("%Y-%m-%d")
                    }
                )
                res_data = res.json()
                st.markdown(f"#### Customer Sentiment Summary Report: {start_date.strftime('%Y-%m-%d')} - {end_date.strftime('%Y-%m-%d')}")
                st.write(res_data.get("summary", "No summary generated."))
