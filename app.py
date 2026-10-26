import streamlit as st
import pandas as pd

st.set_page_config(page_title="Scholarship Tracker", layout="wide")
st.title("🎓 Scholarship Tracker Dashboard")
st.write("আপনার সবকটি Excel ফাইল (যেমন: May to Dec, Jan to June ইত্যাদি) একসাথে আপলোড করুন।")
st.divider()

# একাধিক ফাইল একসাথে আপলোডের অপশন
uploaded_files = st.file_uploader(
    "📁 আপনার সকল Scholarship Excel ফাইল এখানে একসাথে আপলোড করুন:", 
    type=["xlsx", "xls"], 
    accept_multiple_files=True
)

students_record = {}

if uploaded_files:
    for uploaded_file in uploaded_files:
        # ফাইলের নাম সংরক্ষণ
        file_name = uploaded_file.name.rsplit('.', 1)[0]
        try:
            df = pd.read_excel(uploaded_file)
            ids = df.iloc[:, 0].dropna().astype(str).str.strip().tolist()
            
            for s_id in ids:
                if s_id and s_id.lower() != 'nan':
                    if s_id not in students_record:
                        students_record[s_id] = []
                    students_record[s_id].append(file_name)
        except Exception as e:
            st.error(f"'{file_name}' ফাইলে সমস্যা: {e}")

st.divider()
st.header("🔍 স্টুডেন্ট স্কলারশিপ সার্চ")
search_id = st.text_input("স্টুডেন্ট আইডি লিখুন (যেমন: 242-115-001):", "")

if search_id:
    search_id = search_id.strip()
    if search_id in students_record:
        found_files = students_record[search_id]
        st.success(f"Result for Student ID: **{search_id}**")
        st.metric(label="মোট প্রাপ্তি (Total Record Found)", value=f"{len(found_files)} টি ফাইলে পাওয়া গেছে")
        
        st.subheader("📋 আইডিটি যে যে এক্সেল ফাইলে (মেয়াদে) রয়েছে:")
        for idx, fname in enumerate(found_files, 1):
            st.markdown(f"**{idx}.** 📄 **{fname}**")
    else:
        st.warning(f"আইডি **{search_id}** এর কোনো স্কলারশিপ রেকর্ড আপলোডকৃত ফাইলগুলোতে পাওয়া যায়নি।")
