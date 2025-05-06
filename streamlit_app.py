import streamlit as st
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="نظام الحضور", layout="centered")

# زر اختيار اللغة في الزاوية العلوية
col1, col2 = st.columns([6, 1])
with col2:
    lang = st.selectbox("🌐", ["العربية", "English"], label_visibility="collapsed")
st.session_state.lang = lang

# الترجمة
translations = {
    "العربية": {
        "title": "🕒 نظام الحضور",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login": "تسجيل الدخول",
        "wrong_credentials": "❌ اسم المستخدم أو كلمة المرور غير صحيحة",
        "welcome": "مرحباً"
    },
    "English": {
        "title": "🕒 Attendance System",
        "username": "Username",
        "password": "Password",
        "login": "Login",
        "wrong_credentials": "❌ Invalid username or password",
        "welcome": "Welcome"
    }
}
t = translations[lang]

# بيانات المستخدمين
users = {
    "MOH": "Mm123456789",  # المشرف
    "user1": "1234",
    "user2": "abcd",
}

# واجهة الدخول
st.title(t["title"])
username = st.text_input(t["username"])
password = st.text_input(t["password"], type="password")

if st.button(t["login"]):
    if username in users and users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        if username == "MOH":
            st.switch_page("pages/admin_dashboard.py")
        else:
            st.switch_page("pages/dashboard.py")
    else:
        st.error(t["wrong_credentials"])
