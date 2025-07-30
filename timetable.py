# timetable.py
import streamlit as st
from utils import save_timetable, load_timetables
from llm_utils import create_chain
from langchain.prompts import PromptTemplate
from datetime import datetime
import json
import re
from utils import load_css

def extract_json(text):
    """Extracts JSON from Markdown-style fenced code blocks."""
    match = re.search(r"```json(.*?)```", text, re.DOTALL)
    raw_json = match.group(1).strip() if match else text.strip()
    return json.loads(raw_json)

def generate_schedule(topics_text, total_days, daily_hours):
    total_hours = int(total_days) * int(daily_hours)

    prompt_template = PromptTemplate(
        input_variables=["topics", "days", "hours", "total_hours"],
        template="""
You are an expert study planning assistant.

You must build a realistic, efficient daily study plan based on a list of academic or professional topics.

User Input:
- Topics: {topics}
- Available time: {days} days, {hours} hours/day

Rules:
1. Analyze each topic and break it into subtopics.
2. Estimate the difficulty (easy/medium/hard).
3. Allocate more time to harder or more complex topics.
4. DO NOT divide time equally — adjust based on difficulty.
5. If total available time is insufficient, still return a plan using all available time, but include a warning like:
   "⚠️ Time is insufficient to fully cover these topics. Recommended minimum is X days at Y hours/day."

Return format:
```json
{{
  "Day 1": [{{"topic": "...", "hours": ...}}],
  "Day 2": [...],
  ...
  "warning": "..."  # optional, only if needed
}}
Only return valid JSON.
"""
    )

    chain = create_chain(prompt_template)

    response = chain.invoke({
        "topics": topics_text,
        "days": str(total_days),
        "hours": str(daily_hours),
        "total_hours": str(total_hours)
    })

    try:
        return extract_json(response["text"])
    except json.JSONDecodeError:
        st.error("⚠️ Could not parse JSON. Please try again.")
        return None

def validate_schedule(schedule, total_days, daily_hours):
    if not schedule:
        return False

    warning = schedule.get("warning", None)
    if warning:
        del schedule["warning"]

    if len(schedule) > total_days:
        return False

    total_scheduled_hours = sum(
        task["hours"] for tasks in schedule.values() for task in tasks
    )

    return total_scheduled_hours <= total_days * daily_hours

def timetable_page():
    st.markdown("## 📆 AI-Powered Study Timetable")
    st.write("Tell us what you want to learn, and we'll generate a structured study plan.")

    with st.container():
        topics_text = st.text_area("✏️ What topics do you want to learn?", height=150, 
                                   help="List the subjects, technologies, or topics you want to study")

        col1, col2 = st.columns(2)
        with col1:
            total_days = st.number_input("📅 Total available days", min_value=1, value=7, 
                                       help="How many days do you have for studying?")
        with col2:
            daily_hours = st.number_input("⏰ Max hours you can study daily", min_value=1, max_value=24, value=3,
                                        help="Maximum hours you can dedicate per day")

        name = st.text_input("🗂️ Optional name for this plan", 
                           placeholder="e.g., 'Python Mastery', 'Data Science Bootcamp'")

        st.markdown('<div class="primary-button">', unsafe_allow_html=True)
        generate_clicked = st.button("🚀 Generate Timetable", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if generate_clicked:
        if not topics_text.strip():
            st.warning("Please enter some topics.")
            return

        with st.spinner("🤖 AI is creating your personalized study plan..."):
            schedule = generate_schedule(topics_text, total_days, daily_hours)

        if schedule:
            warning = schedule.pop("warning", None)
            if not validate_schedule(schedule, total_days, daily_hours):
                st.error("❌ The generated timetable exceeds your available time or days. Please try again with simpler topics or more time.")
                return

            st.success("✅ Timetable generated successfully!")

            if warning:
                st.warning(f"⚠️ {warning}")

            st.markdown("### 📌 Your Personalized Study Plan")
            for day, tasks in schedule.items():
                st.markdown(f'<div class="timetable-day">', unsafe_allow_html=True)
                st.markdown(f"**{day}**")
                for task in tasks:
                    st.markdown(f'''
                    <div class="timetable-task">
                        <strong>{task['topic']}</strong> — {task['hours']} hour(s)
                    </div>
                    ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            if not st.session_state.get("is_guest", False):
                user_id = st.session_state.get("user_id")
                if user_id:
                    plan_name = name.strip() or f"Study Plan {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                    save_timetable(user_id, plan_name, schedule)
                    st.success("💾 Timetable saved to your account.")
            else:
                st.info("📝 You're in guest mode — timetable won't be saved. Sign up to save your plans!")

def display_saved_timetables():
    if st.session_state.get("is_guest", False):
        st.markdown('''
        <div class="info-card">
            <p>📝 <strong>Guest mode:</strong> No saved timetables available. Sign up to save and manage your study plans!</p>
        </div>
        ''', unsafe_allow_html=True)
        return

    user_id = st.session_state.get("user_id")
    timetables = load_timetables(user_id)

    if not timetables:
        st.markdown('''
        <div class="info-card">
            <p>📚 No saved study plans found. Create your first timetable below!</p>
        </div>
        ''', unsafe_allow_html=True)
        return

    st.markdown("## 📁 Your Saved Study Plans")
    for plan_name, schedule in timetables.items():
        st.markdown(f'<div class="timetable-card">', unsafe_allow_html=True)
        st.markdown(f"### 📋 {plan_name}")

        total_days = len(schedule)
        total_hours = sum(sum(task['hours'] for task in tasks) for tasks in schedule.values())
        st.markdown(f"**Duration:** {total_days} days • **Total Study Time:** {total_hours} hours")

        with st.expander(f"📖 View Details - {plan_name}"):
            for day, tasks in schedule.items():
                st.markdown(f"**{day}:**")
                for task in tasks:
                    st.markdown(f"  • {task['topic']} — {task['hours']} hour(s)")

        st.markdown('</div>', unsafe_allow_html=True)
