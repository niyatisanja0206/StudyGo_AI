# chat.py

import streamlit as st
from datetime import datetime
from langchain.prompts import PromptTemplate
from llm_utils import create_chain
from utils import load_css, load_chats, save_chat, delete_chat
import json
import traceback  # ✅ Added for better error reporting

load_css()

def get_llm_chain():
    prompt = PromptTemplate(
        input_variables=["history", "query"],
        template="""You are an intelligent study planner and academic roadmap assistant.

Your role is to help users:
- Plan learning paths for academic subjects (like math, physics, chemistry, biology, history, etc.)
- Structure professional courses (like programming, data science, AI/ML, design, finance, law, medical prep, etc.)
- Recommend topic hierarchies, resources, and study strategies for serious learning and career development.

⚠️ Very Important:
- DO NOT answer questions about movies, entertainment, celebrities, gossip, jokes, memes, or unrelated personal advice even if it is told by user that it is professional for me me.
- If a user asks anything outside of academic or professional study topics, politely respond:
  > "I'm here to help you plan your studies or professional learning. Please ask about topics like math, science, technology, language learning, or other educational goals."

Stay focused, helpful, and professional.

Chat History:{history}
New Question:{query}
Give a helpful, structured answer suitable for a learning plan.
"""
    )
    return create_chain(prompt)

def chat_interface():
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []
    if "selected_chat_index" not in st.session_state:
        st.session_state.selected_chat_index = None

    user_id = st.session_state.get("user_id")
    is_guest = st.session_state.get("is_guest", False)

    chats = load_chats(user_id) if not is_guest and user_id else []

    with st.sidebar:
        st.markdown("### 🧠 Chat History")
        if is_guest:
            st.markdown("""
                <div class="info-card">
                    <p><strong>📝 Guest Mode:</strong></p>
                    <p>• Chats are not saved permanently<br>
                    • Create an account to keep your history<br>
                    • All AI features are fully available!</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="success-button">', unsafe_allow_html=True)
            if st.button("✨ Start New Chat", use_container_width=True):
                st.session_state.chat_messages = []
                st.session_state.selected_chat_index = None
                st.success("🆕 New chat started!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("---")

            if chats:
                st.markdown("**📚 Previous Conversations:**")
                recent_chats = chats[-8:] if len(chats) > 8 else chats
                for i, chat in enumerate(reversed(recent_chats)):
                    actual_index = len(chats) - 1 - i
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        display_title = chat['title'][:22] + "..." if len(chat['title']) > 22 else chat['title']
                        is_current = st.session_state.selected_chat_index == actual_index
                        if st.button(f"{'🟢' if is_current else '💬'} {display_title}", key=f"load_{actual_index}", use_container_width=True):
                            st.session_state.chat_messages = chat["messages"]
                            st.session_state.selected_chat_index = actual_index
                            st.success(f"📖 Loaded: {display_title}")
                            st.rerun()
                    with col2:
                        st.markdown('<div class="danger-button">', unsafe_allow_html=True)
                        if st.button("🗑️", key=f"delete_{actual_index}"):
                            delete_chat(user_id, chat["title"])
                            st.success("🗑️ Chat deleted!")
                            st.rerun()
                        st.markdown('</div>', unsafe_allow_html=True)

                if len(chats) > 8:
                    st.markdown(f"<div class='info-card' style='text-align: center;'>... and {len(chats) - 8} more chats</div>", unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div class="info-card">
                        <p>💭 <strong>No chat history yet</strong></p>
                        <p>Start a conversation below and it will appear here!</p>
                    </div>
                """, unsafe_allow_html=True)

    st.markdown("## 📚 AI Learning Assistant")
    st.markdown("*Your intelligent companion for learning any subject or skill*")

    if st.session_state.chat_messages and not is_guest:
        current_chat_title = st.session_state.chat_messages[0]["content"][:35] + "..." if len(st.session_state.chat_messages[0]["content"]) > 35 else st.session_state.chat_messages[0]["content"]
        st.markdown(f"""
            <div class="info-card" style="border-left: 4px solid #28a745;">
                <p><strong>📖 Current Chat:</strong> {current_chat_title}</p>
                <p style="font-size: 0.85rem;">💬 {len(st.session_state.chat_messages)} messages in this conversation</p>
            </div>
        """, unsafe_allow_html=True)

    chat_container = st.container()

    with chat_container:
        if st.session_state.chat_messages:
            for msg in st.session_state.chat_messages:
                if msg["role"] == "user":
                    st.markdown(f"""
                        <div class="user-message">
                            <strong>🤓</strong><br>
                            <span>{msg["content"]}</span>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="ai-message">
                            <strong>🧠</strong><br>
                            <span>{msg["content"]}</span>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="welcome-section">
                    <h3>👋 Hello! I'm your AI Learning Assistant</h3>
                    <p>Ask me anything about your studies - from explaining concepts to creating study plans!</p>
                    <p><strong>💡 Try asking me:</strong></p>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                        <div style="background: rgba(0, 123, 255, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #007bff;">
                            <p><strong>📖 Concepts:</strong><br>"Explain machine learning basics"</p>
                        </div>
                        <div style="background: rgba(40, 167, 69, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #28a745;">
                            <p><strong>📋 Study Plans:</strong><br>"Create a Python learning roadmap"</p>
                        </div>
                        <div style="background: rgba(255, 193, 7, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #ffc107;">
                            <p><strong>🧮 Math Help:</strong><br>"Help me understand derivatives"</p>
                        </div>
                        <div style="background: rgba(220, 53, 69, 0.1); padding: 1rem; border-radius: 8px; border-left: 3px solid #dc3545;">
                            <p><strong>🔬 Science:</strong><br>"What are key biology concepts?"</p>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    user_query = st.chat_input("💬 Ask your study question here... ")

    if user_query:
        st.session_state.chat_messages.append({"role": "user", "content": user_query})

        with st.spinner("AI is analyzing your question and preparing a helpful response..."):
            chain = get_llm_chain()
            history = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state.chat_messages[:-1])

            try:
                response = chain.invoke({"history": history, "query": user_query})

                if isinstance(response, dict):
                    ai_msg = response.get("text") or response.get("content") or str(response)
                else:
                    ai_msg = str(response)

                st.session_state.chat_messages.append({"role": "assistant", "content": ai_msg})
            except Exception as e:
                error_msg = "I apologize, but I encountered an error processing your request."
                st.session_state.chat_messages.append({"role": "assistant", "content": error_msg})
                st.error("⚠️ Error occurred during chain invocation:")
                st.code(traceback.format_exc(), language="python")  # ✅ Show full traceback

        if not is_guest and user_id:
            if "chat_saved" not in st.session_state or not st.session_state.chat_saved:
                if len([m for m in st.session_state.chat_messages if m["role"] == "assistant"]) > 0:
                    chat_title = st.session_state.chat_messages[0]["content"][:40] + "..." if len(st.session_state.chat_messages[0]["content"]) > 40 else st.session_state.chat_messages[0]["content"]
                    save_chat(user_id, chat_title, st.session_state.chat_messages, datetime.now().isoformat())
                    st.session_state.chat_saved = True

        st.rerun()

    if not st.session_state.chat_messages:
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 💡 Tips for Better Learning")
            st.markdown("""
                <div class="info-card">
                    <ul style="font-size: 0.9rem;">
                        <li><strong>Be Specific:</strong> Ask detailed questions</li>
                        <li><strong>Ask for Examples:</strong> Request use cases</li>
                        <li><strong>Break Down Topics:</strong> Ask for steps</li>
                        <li><strong>Request Practice:</strong> Ask for exercises</li>
                        <li><strong>Follow Up:</strong> Build on answers</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)

    elif st.session_state.chat_messages and not is_guest:
        with st.sidebar:
            st.markdown("---")
            st.markdown("### 📊 Chat Statistics")
            user_messages = len([m for m in st.session_state.chat_messages if m["role"] == "user"])
            ai_messages = len([m for m in st.session_state.chat_messages if m["role"] == "assistant"])
            st.markdown(f"""
                <div class="info-card">
                    <p><strong>This Conversation:</strong><br>
                    • 🤓 Your questions: {user_messages}<br>
                    • 🧠 AI responses: {ai_messages}<br>
                    • 📈 Total messages: {len(st.session_state.chat_messages)}</p>
                </div>
            """, unsafe_allow_html=True)