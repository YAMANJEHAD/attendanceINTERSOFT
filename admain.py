import streamlit as st
import pandas as pd
from datetime import datetime
import os

# إعداد
st.set_page_config(page_title="لوحة الموظف", layout="centered")
upload_dir = "uploaded_files"
os.makedirs(upload_dir, exist_ok=True)
excel_file = "attendance_log.xlsx"

# حماية
if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.warning("الرجاء تسجيل الدخول أولاً.")
    st.stop()

username = st.session_state.username

# تحميل البيانات
if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
else:
    df = pd.DataFrame(columns=["اسم المستخدم", "التاريخ", "وقت الحضور", "وقت الانصراف"])

today_str = datetime.today().strftime("%Y-%m-%d")
now_time = datetime.now().strftime("%H:%M:%S")

# واجهة المستخدم
st.title(f"👋 مرحباً {username}")
st.markdown("### ✅ سجل حضورك اليوم:")

# تسجيل الحضور أو الانصراف
user_today = df[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str)]

if user_today.empty:
    if st.button("📥 تسجيل الحضور"):
        new_row = pd.DataFrame({
            "اسم المستخدم": [username],
            "التاريخ": [today_str],
            "وقت الحضور": [now_time],
            "وقت الانصراف": [None]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(excel_file, index=False)
        st.success("تم تسجيل الحضور بنجاح")
else:
    if pd.isna(user_today.iloc[0]["وقت الانصراف"]):
        if st.button("📤 تسجيل الانصراف"):
            df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str), "وقت الانصراف"] = now_time
            df.to_excel(excel_file, index=False)
            st.success("تم تسجيل الانصراف بنجاح")
    else:
        st.info("✅ تم تسجيل الحضور والانصراف لهذا اليوم")

# عرض بيانات المستخدم
st.markdown("### 📊 السجلات السابقة وساعات العمل")
user_data = df[df["اسم المستخدم"] == username].copy()

def calc_duration(row):
    try:
        if pd.notna(row["وقت الحضور"]) and pd.notna(row["وقت الانصراف"]):
            in_time = datetime.strptime(str(row["وقت الحضور"]), "%H:%M:%S")
            out_time = datetime.strptime(str(row["وقت الانصراف"]), "%H:%M:%S")
            duration = out_time - in_time
            return str(duration)
    except:
        return ""
    return ""

user_data["ساعات العمل"] = user_data.apply(calc_duration, axis=1)
st.dataframe(user_data)

# رفع ملفات
st.markdown("### 📤 رفع ملفات للمشاركة")
uploaded_file = st.file_uploader("اختر ملفاً", type=["pdf", "docx", "xlsx", "png", "jpg", "txt"])
if uploaded_file:
    with open(os.path.join(upload_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ تم رفع الملف بنجاح")

# عرض وتحميل الملفات
st.markdown("### 📁 الملفات المتوفرة للتحميل")
for file in os.listdir(upload_dir):
    with open(os.path.join(upload_dir, file), "rb") as f:
        st.download_button(label=f"⬇️ تحميل {file}", data=f, file_name=file)
