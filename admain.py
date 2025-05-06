import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="لوحة المشرف", layout="wide")
st.title("🛠️ لوحة المشرف - إدارة الحضور")

excel_file = "attendance_log.xlsx"

if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
else:
    st.warning("لا توجد سجلات بعد.")
    df = pd.DataFrame()

# فلترة بالتاريخ
st.markdown("### 🔍 فلترة حسب التاريخ")
date_filter = st.date_input("اختر تاريخ", datetime.today())
filtered = df[df["التاريخ"] == date_filter.strftime("%Y-%m-%d")]

st.dataframe(filtered if not filtered.empty else df)

# تحميل Excel
st.download_button("📥 تحميل كل السجلات كملف Excel", data=df.to_excel(index=False), file_name="attendance_log.xlsx", mime="application/vnd.ms-excel")

# عرض الملفات المرفوعة
st.markdown("## 📁 الملفات المرفوعة من الموظفين")
files = os.listdir("uploaded_files")
for file in files:
    st.markdown(f"📎 [{file}](../uploaded_files/{file})")
