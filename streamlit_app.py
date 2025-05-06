import streamlit as st
import pandas as pd
import os
from datetime import datetime

# إعداد صفحة Streamlit
st.set_page_config(page_title="Attendance System | نظام الحضور", layout="centered", initial_sidebar_state="expanded")

# اسم ملف Excel لتخزين السجلات
excel_file = "attendance_log.xlsx"

# بيانات المستخدمين (اسم المستخدم وكلمة السر)
users = {
    "MOH": "Mm123456789",  # المشرف
    "user1": "1234",
    "user2": "abcd",
}

# اختيار اللغة
language = st.sidebar.selectbox("Language | اللغة", ["العربية", "English"])

# ترجمات
translations = {
    "العربية": {
        "title": "🕒 نظام الحضور",
        "username": "اسم المستخدم",
        "password": "كلمة المرور",
        "login": "تسجيل الدخول",
        "welcome": "مرحباً",
        "admin_panel": "📋 لوحة المشرف - جميع سجلات الموظفين",
        "date_filter": "🔎 اختر تاريخ لعرض السجلات",
        "check_in": "📥 تسجيل الحضور",
        "check_out": "📤 تسجيل الانصراف",
        "already_checked": "✅ تم تسجيل الحضور والانصراف لهذا اليوم",
        "edit_logs": "✏️ تعديل سجلات سابقة",
        "select_date": "اختر تاريخ",
        "new_in": "وقت الحضور الجديد (hh:mm:ss)",
        "new_out": "وقت الانصراف الجديد (hh:mm:ss)",
        "save_changes": "💾 حفظ التعديل",
        "updated": "✅ تم تحديث السجل",
        "no_record": "لا يوجد سجل لهذا التاريخ",
        "success_checkin": "تم تسجيل الحضور بنجاح",
        "success_checkout": "تم تسجيل الانصراف بنجاح",
        "wrong_credentials": "❌ اسم المستخدم أو كلمة المرور غير صحيحة"
    },
    "English": {
        "title": "🕒 Attendance System",
        "username": "Username",
        "password": "Password",
        "login": "Login",
        "welcome": "Welcome",
        "admin_panel": "📋 Admin Panel - All Employees' Records",
        "date_filter": "🔎 Select a date to view records",
        "check_in": "📥 Check In",
        "check_out": "📤 Check Out",
        "already_checked": "✅ You have already checked in and out today",
        "edit_logs": "✏️ Edit Previous Records",
        "select_date": "Select a Date",
        "new_in": "New Check-in Time (hh:mm:ss)",
        "new_out": "New Check-out Time (hh:mm:ss)",
        "save_changes": "💾 Save Changes",
        "updated": "✅ Record Updated",
        "no_record": "No record for this date",
        "success_checkin": "Checked in successfully",
        "success_checkout": "Checked out successfully",
        "wrong_credentials": "❌ Incorrect username or password"
    }
}

t = translations[language]

# واجهة تسجيل الدخول
st.title(t["title"])
st.markdown("---")
username = st.text_input(t["username"])
password = st.text_input(t["password"], type="password")

if st.button(t["login"]):
    if username in users and users[username] == password:
        st.success(f"{t['welcome']} {username}!")

        # تحميل ملف Excel أو إنشاؤه إذا لم يكن موجوداً
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file)
        else:
            df = pd.DataFrame(columns=["اسم المستخدم", "التاريخ", "وقت الحضور", "وقت الانصراف"])

        today_str = datetime.today().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M:%S")

        # لوحة المشرف
        if username == "MOH":
            st.subheader(t["admin_panel"])
            date_filter = st.date_input(t["date_filter"], datetime.today())
            filtered = df[df["التاريخ"] == pd.to_datetime(date_filter).strftime("%Y-%m-%d")]
            st.dataframe(filtered if not filtered.empty else df)

        else:
            user_today = df[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str)]

            if user_today.empty:
                if st.button(t["check_in"]):
                    new_row = pd.DataFrame({
                        "اسم المستخدم": [username],
                        "التاريخ": [today_str],
                        "وقت الحضور": [now],
                        "وقت الانصراف": [None]
                    })
                    df = pd.concat([df, new_row], ignore_index=True)
                    df.to_excel(excel_file, index=False)
                    st.success(t["success_checkin"])
            else:
                if pd.isna(user_today.iloc[0]["وقت الانصراف"]):
                    if st.button(t["check_out"]):
                        df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str), "وقت الانصراف"] = now
                        df.to_excel(excel_file, index=False)
                        st.success(t["success_checkout"])
                else:
                    st.info(t["already_checked"])

            # تعديل السجلات القديمة
            with st.expander(t["edit_logs"]):
                user_records = df[df["اسم المستخدم"] == username]
                edit_date = st.date_input(t["select_date"], datetime.today(), key="edit_date")
                edit_row = user_records[user_records["التاريخ"] == edit_date.strftime("%Y-%m-%d")]

                if not edit_row.empty:
                    new_in = st.text_input(t["new_in"], edit_row.iloc[0]["وقت الحضور"])
                    new_out = st.text_input(t["new_out"], edit_row.iloc[0]["وقت الانصراف"] or "")
                    if st.button(t["save_changes"]):
                        df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == edit_date.strftime("%Y-%m-%d")), "وقت الحضور"] = new_in
                        df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == edit_date.strftime("%Y-%m-%d")), "وقت الانصراف"] = new_out
                        df.to_excel(excel_file, index=False)
                        st.success(t["updated"])
                else:
                    st.warning(t["no_record"])
    else:
        st.error(t["wrong_credentials"])
