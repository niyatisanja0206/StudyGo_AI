# auth_ui.py
import streamlit as st
from auth import create_user, authenticate_user, delete_user
import uuid

def show_auth_ui():
    st.sidebar.subheader("🔐 Authentication")

    auth_mode = st.sidebar.radio("Choose an option:", ["Login", "Sign Up", "Continue as Guest"])

    if auth_mode == "Sign Up":
        st.sidebar.markdown("### 📝 Create New Account")
        username = st.sidebar.text_input("New Username", placeholder="Enter username")
        password = st.sidebar.text_input("New Password", type="password", placeholder="Enter password")
        
        st.sidebar.markdown('<div class="success-button">', unsafe_allow_html=True)
        if st.sidebar.button("Sign Up", use_container_width=True):
            if username and password:
                user_id = create_user(username, password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.is_guest = False
                    st.sidebar.success("✅ Account created successfully!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Username already exists.")
            else:
                st.sidebar.error("❌ Please fill in both fields.")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)

    elif auth_mode == "Login":
        st.sidebar.markdown("### 🔑 Sign In")
        username = st.sidebar.text_input("Username", placeholder="Enter username")
        password = st.sidebar.text_input("Password", type="password", placeholder="Enter password")
        
        st.sidebar.markdown('<div class="primary-button">', unsafe_allow_html=True)
        if st.sidebar.button("Login", use_container_width=True):
            if username and password:
                user_id = authenticate_user(username, password)
                if user_id:
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.is_guest = False
                    st.sidebar.success("✅ Welcome back!")
                    st.rerun()
                else:
                    st.sidebar.error("❌ Invalid username or password.")
            else:
                st.sidebar.error("❌ Please enter both username and password.")
        st.sidebar.markdown('</div>', unsafe_allow_html=True)

    elif auth_mode == "Continue as Guest":
        st.sidebar.markdown("### 🕶️ Guest Access")
        st.sidebar.info("💡 **Note:** Guest data won't be saved permanently.")
        
        st.sidebar.markdown('<div class="primary-button">', unsafe_allow_html=True)
        if st.sidebar.button("Enter as Guest", use_container_width=True):
            st.session_state.user_id = None
            st.session_state.username = "Guest"
            st.session_state.is_guest = True
            st.sidebar.success("🕶️ Welcome, Guest!")
            st.rerun()
        st.sidebar.markdown('</div>', unsafe_allow_html=True)