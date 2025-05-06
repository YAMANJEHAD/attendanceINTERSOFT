import streamlit as st
import pandas as pd
import os
from datetime import datetime

# إعداد صفحة Streamlit
st.set_page_config(page_title="نظام الحضور", layout="centered", initial_sidebar_state="expanded")

# اسم ملف Excel لتخزين السجلات
excel_file = "attendance_log.xlsx"

# إعداد بيانات المستخدمين (اسم المستخدم وكلمة السر)
users = {
    "MOH": "Mm123456789",  # المشرف
    "user1": "1234",
    "user2": "abcd",
    # أضف مزيداً من المستخدمين هنا
}

# واجهة تسجيل الدخول
st.title("🕒 نظام الحضور")
st.markdown("---")
username = st.text_input("اسم المستخدم")
password = st.text_input("كلمة المرور", type="password")

if st.button("تسجيل الدخول"):
    if username in users and users[username] == password:
        st.success(f"مرحباً {username}!")

        # تحميل ملف Excel أو إنشاءه إذا لم يكن موجوداً
        if os.path.exists(excel_file):
            df = pd.read_excel(excel_file)
        else:
            df = pd.DataFrame(columns=["اسم المستخدم", "التاريخ", "وقت الحضور", "وقت الانصراف"])

        today_str = datetime.today().strftime("%Y-%m-%d")
        now = datetime.now().strftime("%H:%M:%S")

        # لوحة المشرف لرؤية الكل
        if username == "MOH":
            st.subheader("📋 لوحة المشرف - جميع سجلات الموظفين")

            date_filter = st.date_input("🔎 اختر تاريخ لعرض السجلات", datetime.today())
            filtered = df[df["التاريخ"] == pd.to_datetime(date_filter).strftime("%Y-%m-%d")]
            st.dataframe(filtered if not filtered.empty else df)

        else:
            # عرض السجل الحالي للمستخدم
            user_today = df[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str)]

            if user_today.empty:
                if st.button("📥 تسجيل الحضور"):
                    new_row = pd.DataFrame({
                        "اسم المستخدم": [username],
                        "التاريخ": [today_str],
                        "وقت الحضور": [now],
                        "وقت الانصراف": [None]
                    })
                    df = pd.concat([df, new_row], ignore_index=True)
                    df.to_excel(excel_file, index=False)
                    st.success("تم تسجيل الحضور بنجاح")
            else:
                if pd.isna(user_today.iloc[0]["وقت الانصراف"]):
                    if st.button("📤 تسجيل الانصراف"):
                        df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == today_str), "وقت الانصراف"] = now
                        df.to_excel(excel_file, index=False)
                        st.success("تم تسجيل الانصراف بنجاح")
                else:
                    st.info("✅ تم تسجيل الحضور والانصراف لهذا اليوم")

            # تعديل السجلات القديمة للمستخدم
            with st.expander("✏️ تعديل سجلات سابقة"):
                user_records = df[df["اسم المستخدم"] == username]
                edit_date = st.date_input("اختر تاريخ", datetime.today(), key="edit_date")
                edit_row = user_records[user_records["التاريخ"] == edit_date.strftime("%Y-%m-%d")]

                if not edit_row.empty:
                    new_in = st.text_input("وقت الحضور الجديد (hh:mm:ss)", edit_row.iloc[0]["وقت الحضور"])
                    new_out = st.text_input("وقت الانصراف الجديد (hh:mm:ss)", edit_row.iloc[0]["وقت الانصراف"] or "")
                    if st.button("💾 حفظ التعديل"):
                        df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == edit_date.strftime("%Y-%m-%d")), "وقت الحضور"] = new_in
                        df.loc[(df["اسم المستخدم"] == username) & (df["التاريخ"] == edit_date.strftime("%Y-%m-%d")), "وقت الانصراف"] = new_out
                        df.to_excel(excel_file, index=False)
                        st.success("✅ تم تحديث السجل")
                else:
                    st.warning("لا يوجد سجل لهذا التاريخ")
    else:
        st.error("❌ اسم المستخدم أو كلمة المرور غير صحيحة")
