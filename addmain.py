import streamlit as st
import pandas as pd
from datetime import datetime

# إعداد الصفحة
st.set_page_config(page_title="لوحة المشرف", layout="wide")

# حماية
if "logged_in" not in st.session_state or st.session_state.username != "MOH":
    st.warning("⚠️ غير مصرح لك بالدخول هنا.")
    st.stop()

st.title("📋 لوحة المشرف - جميع سجلات الموظفين")

excel_file = "attendance_log.xlsx"
if os.path.exists(excel_file):
    df = pd.read_excel(excel_file)
else:
    df = pd.DataFrame(columns=["اسم المستخدم", "التاريخ", "وقت الحضور", "وقت الانصراف"])

# حساب الفروقات
def calc(row):
    expected_start = datetime.strptime("09:00:00", "%H:%M:%S")
    expected_end = datetime.strptime("17:00:00", "%H:%M:%S")
    try:
        in_time = datetime.strptime(str(row["وقت الحضور"]), "%H:%M:%S")
        out_time = datetime.strptime(str(row["وقت الانصراف"]), "%H:%M:%S")
        late = (in_time - expected_start).seconds // 60 if in_time > expected_start else 0
        early = (expected_end - out_time).seconds // 60 if out_time < expected_end else 0
        duration = out_time - in_time
        return pd.Series([late, early, str(duration)])
    except:
        return pd.Series([None, None, None])

df[["تأخير (دقائق)", "انصراف مبكر (دقائق)", "مدة العمل"]] = df.apply(calc, axis=1)
st.dataframe(df)
