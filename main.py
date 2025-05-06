import streamlit as st
import os

# إعداد صفحة Streamlit
st.set_page_config(page_title="تسجيل الدخول", layout="centered")
st.markdown("<h1 style='text-align: center;'>🕒 نظام الحضور</h1>", unsafe_allow_html=True)

# زر اختيار اللغة في الزاوية العلوية
lang = st.selectbox("🌐 Language / اللغة", ["العربية", "English"], key="lang", index=0)

# بيانات الدخول
users = {
    "MOH": "Mm123456789",  # المشرف
    "user1": "1234",
    "user2": "abcd"
}

# إدخال البيانات
username = st.text_input("👤 اسم المستخدم")
password = st.text_input("🔑 كلمة المرور", type="password")

# إنشاء مجلد رفع الملفات إن لم يكن موجودًا
os.makedirs("uploaded_files", exist_ok=True)

if st.button("🚪 تسجيل الدخول"):
    if username in users and users[username] == password:
        st.session_state.username = username
        st.session_state.language = lang

        if username == "MOH":
            st.switch_page("pages/admin_dashboard.py")
        else:
            st.switch_page("pages/dashboard.py")
    else:
        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
