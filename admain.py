import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="لوحة الموظف", layout="wide")

st.markdown("## 👤 لوحة الموظف")
username = st.session_state.get("username", "")
lang = st.session_state.get("language", "العربية")

excel_file = "attendance_log.xlsx"
now = datetime.now()
today_str = now.strftime("%Y-%m-%d")
now_str = now.strftime("%H:%M:%S")

# تحميل ملف Excel
if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
else:
    df = pd.DataFrame(columns=["اسم المستخدم", "التاريخ", "وقت الحضور", "وقت الانصراف", "ساعات العمل", "تأخير", "انصراف مبكر"])

# عرض معلومات اليوم
user_today = df[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str)]

if user_today.empty:
    if st.button("📥 تسجيل الحضور"):
        new_row = pd.DataFrame({
            "اسم المستخدم": [username],
            "التاريخ": [today_str],
            "وقت الحضور": [now_str],
            "وقت الانصراف": [None],
            "ساعات العمل": [None],
            "تأخير": [None],
            "انصراف مبكر": [None]
        })
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_excel(excel_file, index=False)
        st.success("✅ تم تسجيل الحضور")
else:
    row = user_today.iloc[0]
    if pd.isna(row["وقت الانصراف"]):
        if st.button("📤 تسجيل الانصراف"):
            df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str), "وقت الانصراف"] = now_str

            # حساب الوقت
            in_time = datetime.strptime(row["وقت الحضور"], "%H:%M:%S")
            out_time = datetime.strptime(now_str, "%H:%M:%S")
            work_duration = out_time - in_time
            hours = round(work_duration.total_seconds() / 3600, 2)

            # حساب التأخير والانصراف المبكر
            expected_start = datetime.strptime("09:00:00", "%H:%M:%S")
            expected_end = datetime.strptime("17:00:00", "%H:%M:%S")

            delay = max((in_time - expected_start).total_seconds() / 60, 0)
            early_leave = max((expected_end - out_time).total_seconds() / 60, 0)

            df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str), "ساعات العمل"] = hours
            df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str), "تأخير"] = round(delay, 1)
            df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str), "انصراف مبكر"] = round(early_leave, 1)

            df.to_excel(excel_file, index=False)
            st.success("✅ تم تسجيل الانصراف")
    else:
        st.info("✅ تم تسجيل الحضور والانصراف لهذا اليوم")

# تعديل السجلات القديمة
with st.expander("✏️ تعديل سجلات سابقة"):
    user_records = df[df["اسم المستخدم"] == username]
    edit_date = st.date_input("📅 اختر تاريخ", datetime.today())
    edit_row = user_records[user_records["التاريخ"] == edit_date.strftime("%Y-%m-%d")]

    if not edit_row.empty:
        new_in = st.text_input("🕘 وقت الحضور الجديد", edit_row.iloc[0]["وقت الحضور"])
        new_out = st.text_input("🕔 وقت الانصراف الجديد", edit_row.iloc[0]["وقت الانصراف"] or "")
        if st.button("💾 حفظ التعديل"):
            idx = df.index[(df["اسم المستخدم"] == username) & (df["التاريخ"] == edit_date.strftime("%Y-%m-%d"))][0]
            df.at[idx, "وقت الحضور"] = new_in
            df.at[idx, "وقت الانصراف"] = new_out

            # إعادة حساب
            in_time = datetime.strptime(new_in, "%H:%M:%S")
            out_time = datetime.strptime(new_out, "%H:%M:%S")
            work_duration = out_time - in_time
            hours = round(work_duration.total_seconds() / 3600, 2)

            expected_start = datetime.strptime("09:00:00", "%H:%M:%S")
            expected_end = datetime.strptime("17:00:00", "%H:%M:%S")

            delay = max((in_time - expected_start).total_seconds() / 60, 0)
            early_leave = max((expected_end - out_time).total_seconds() / 60, 0)

            df.at[idx, "ساعات العمل"] = hours
            df.at[idx, "تأخير"] = round(delay, 1)
            df.at[idx, "انصراف مبكر"] = round(early_leave, 1)

            df.to_excel(excel_file, index=False)
            st.success("✅ تم التحديث")

# رفع ملفات
st.markdown("## 📤 رفع ملف لمشاركته")
uploaded = st.file_uploader("اختر ملف", type=["pdf", "docx", "xlsx", "jpg", "png"])
if uploaded:
    with open(os.path.join("uploaded_files", uploaded.name), "wb") as f:
        f.write(uploaded.read())
    st.success("✅ تم رفع الملف")

# عرض الملفات
st.markdown("## 📁 ملفات مرفوعة من الجميع")
files = os.listdir("uploaded_files")
for file in files:
    st.markdown(f"📎 [{file}](uploaded_files/{file})")
