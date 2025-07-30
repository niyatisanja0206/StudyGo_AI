# 🎓 StudyGo AI

StudyGo AI is a Streamlit-based intelligent study planner and real-time AI assistant designed to help users:
- Create custom learning roadmaps
- Generate efficient timetables
- Ask academic questions via an intelligent chatbot

Whether you're a student, professional, or lifelong learner — StudyGo AI helps you organize and optimize your study journey.

---

## 🚀 Features

- 🗨️ **AI Chat Assistant**  
  Get structured learning advice, topic breakdowns, and concept explanations for academic and professional subjects.

- 📅 **Timetable Generator**  
  Automatically generate optimized study schedules based on topics and available days/hours.

- 💾 **Persistent Chat & Timetable Storage**  
  Registered users can save their chats and timetables for later review.

- 🔐 **User Authentication**  
  Sign up, log in, or use the app as a guest (chats/timetables won’t be saved permanently in guest mode).

- 🎨 **Responsive UI**  
  Clean, user-friendly layout with interactive sidebar, tool selection, and session-based history.

---

## 🧠 Technologies Used

- [Streamlit](https://streamlit.io/) - frontend and state management
- [LangChain](https://www.langchain.com/) - for LLM orchestration
- [OpenAI API](https://platform.openai.com/docs/) - GPT-4 based responses
- SQLite - local database for chat/timetable persistence
- Python standard libraries: `datetime`, `json`, `os`, `hashlib`, etc.

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/studygo-ai.git
   cd studygo-ai
 ```

Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install dependencies
```
```bash
pip install -r requirements.txt
```
Set your environment variables
Create a .env file in the root directory:

▶️ Run the App
```bash
streamlit run app.py
```
