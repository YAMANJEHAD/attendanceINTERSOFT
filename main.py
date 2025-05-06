import streamlit as st
import pandas as pd
import datetime
import os

# محاكاة قاعدة بيانات الموظفين (في التطبيق الفعلي يمكن استبداله بقاعدة بيانات)
users_db = {
    'ahmed': '12345',
    'sarah': 'password',
    'mohammed': 'qwerty',
    'lina': 'abcde'
}

# تخزين بيانات الحضور (يمكن استبداله بقاعدة بيانات أو ملف Excel)
attendance_data = []

# استرجاع الوقت الحالي بتنسيق مناسب
def get_current_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# تحديد اللغة المختارة
def set_language(language):
    if language == "Arabic":
        return {
            "employee_page": "صفحة الموظف",
            "admin_page": "صفحة المدير",
            "login": "تسجيل الدخول",
            "username": "اسم المستخدم",
            "password": "كلمة المرور",
            "start_work": "بدء الدوام",
            "end_work": "إنهاء الدوام",
            "hours_worked": "إجمالي الساعات",
            "logout": "تسجيل الخروج",
            "admin": "المدير",
            "employee_data": "بيانات الحضور لجميع الموظفين",
            "export": "تصدير البيانات إلى Excel",
            "success": "تم تصدير التقرير بنجاح!"
        }
    else:
        return {
            "employee_page": "Employee Page",
            "admin_page": "Admin Page",
            "login": "Login",
            "username": "Username",
            "password": "Password",
            "start_work": "Start Work",
            "end_work": "End Work",
            "hours_worked": "Total Hours",
            "logout": "Logout",
            "admin": "Admin",
            "employee_data": "Employee Attendance Data",
            "export": "Export Data to Excel",
            "success": "Report successfully exported!"
        }

# صفحة الموظف
def employee_page(language_dict):
    st.title(language_dict["employee_page"])

    # التحقق من تسجيل الدخول
    username = st.text_input(language_dict["username"])
    password = st.text_input(language_dict["password"], type="password")

    if st.button(language_dict["login"]):
        if username in users_db and users_db[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.start_time = None
            st.success(f"Welcome {username}!")
        else:
            st.error("Incorrect username or password!")

    if 'logged_in' in st.session_state and st.session_state.logged_in:
        # إذا كان الموظف قد سجل الدخول، يمكنه بدء الدوام
        if st.session_state.start_time is None:
            if st.button(language_dict["start_work"]):
                st.session_state.start_time = get_current_time()
                st.write(f"Work started at: {st.session_state.start_time}")
        else:
            if st.button(language_dict["end_work"]):
                end_time = get_current_time()
                start_time = datetime.datetime.strptime(st.session_state.start_time, '%Y-%m-%d %H:%M:%S')
                end_time_dt = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                total_hours = (end_time_dt - start_time).seconds / 3600

                # إضافة البيانات إلى قائمة الحضور
                attendance_data.append({
                    'Employee Name': st.session_state.username,
                    'Attendance Date': start_time.strftime('%Y-%m-%d'),
                    'Check-In Time': st.session_state.start_time,
                    'Check-Out Time': end_time,
                    'Total Hours': total_hours
                })

                st.write(f"Work ended at: {end_time}")
                st.write(f"{language_dict['hours_worked']}: {total_hours} hours")
                st.session_state.start_time = None
        # العودة إلى الصفحة الرئيسية إذا كنت بحاجة
        if st.button(language_dict["logout"]):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.session_state.start_time = None

# صفحة المدير
def admin_page(language_dict):
    st.title(language_dict["admin_page"])

    # عرض جميع بيانات الموظفين
    if len(attendance_data) > 0:
        df = pd.DataFrame(attendance_data)
        st.write(language_dict["employee_data"])
        st.dataframe(df)

        # خيار لتصدير البيانات إلى Excel
        if st.button(language_dict["export"]):
            df.to_excel("attendance_report.xlsx", index=False)
            st.write(language_dict["success"])
    else:
        st.write("No data yet.")

# الصفحة الرئيسية
def main():
    # تحديد اللغة المختارة
    language = st.selectbox("Select Language", ["Arabic", "English"])

    # استرجاع النصوص بناءً على اللغة المختارة
    language_dict = set_language(language)

    # تحديد نوع المستخدم (موظف أو مدير)
    page = st.selectbox(language_dict["admin"], [language_dict["employee_page"], language_dict["admin_page"]])

    if page == language_dict["employee_page"]:
        employee_page(language_dict)
    elif page == language_dict["admin_page"]:
        admin_page(language_dict)

# تشغيل التطبيق
if __name__ == "__main__":
    main()
