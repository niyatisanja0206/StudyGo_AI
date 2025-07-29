import streamlit as st
from streamlit_cookies_manager import EncryptedCookieManager

if "cookies" not in st.session_state:
    st.session_state.cookies = EncryptedCookieManager(
        prefix="test_",
        password="test-password"
    )

cookies = st.session_state.cookies

st.title("🔐 Cookie Test")

if not cookies.ready():
    st.info("Cookies not ready. Please refresh the page.")
    st.stop()

if not cookies.get("visitor_id"):
    import uuid
    cookies["visitor_id"] = str(uuid.uuid4())
    cookies.save()

st.success("Visitor ID: " + cookies["visitor_id"])
