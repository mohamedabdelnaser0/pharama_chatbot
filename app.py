%%writefile app.py

import streamlit as st
import pandas as pd
from rapidfuzz import process


# ==========================
# Page Config
# ==========================

st.set_page_config(
    page_title="Pharma AI",
    page_icon="💊"
)


# ==========================
# Load Dataset
# ==========================

# ==========================
# Load Dataset
# ==========================

@st.cache_data
def load_data():

    url = "https://huggingface.co/mohamed22264/medical_data/resolve/main/medicines.csv"

    df = pd.read_csv(url)

    df.columns = df.columns.str.strip()

    return df


df = load_data()



# ==========================
# Title
# ==========================

st.markdown(
    """
    <h1 style='text-align:center;color:#1565C0'>
    💊 Pharma AI Assistant
    </h1>
    """,
    unsafe_allow_html=True
)


st.write(
    "اسأل عن أي دواء وسأعطيك المعلومات الموجودة في قاعدة البيانات."
)



# ==========================
# Search
# ==========================

def search_medicine(question):


    names = df["drug_name"].astype(str).tolist()


    match = process.extractOne(
        question.upper(),
        names
    )


    if match:

        medicine_name = match[0]


        medicine = df[
            df["drug_name"] == medicine_name
        ].iloc[0]


        return f"""

💊 **اسم الدواء:**
{medicine['drug_name']}


🏷️ **الفئة:**
{medicine['drug_class']}


🩺 **الحالة:**
{medicine['condition']}


📈 **الفعالية:**
{medicine['effectiveness']}


⚠️ **الأعراض الجانبية:**
{medicine['side_effect']}


🤰 **تحذيرات الحمل:**
{medicine['pregnancy_warning']}


📋 **التوصيات:**
{medicine['recommendation']}

"""


    return "لم أجد الدواء في قاعدة البيانات."



# ==========================
# Chat Memory
# ==========================

if "messages" not in st.session_state:

    st.session_state.messages = []



for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):

        st.write(msg["content"])



# ==========================
# Chat
# ==========================

question = st.chat_input(
    "💬 اكتب اسم الدواء..."
)


if question:


    st.session_state.messages.append(
        {
            "role":"user",
            "content":question
        }
    )


    with st.chat_message("user"):

        st.write(question)



    answer = search_medicine(question)


    with st.chat_message("assistant"):

        st.write(answer)



    st.session_state.messages.append(
        {
            "role":"assistant",
            "content":answer
        }
    )
