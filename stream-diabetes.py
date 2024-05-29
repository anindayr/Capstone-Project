import pickle
import openai
import streamlit as st
from streamlit_option_menu import option_menu

#navigasi sidebar
with st.sidebar :
    selected = option_menu('GlucoCare Apps', 
    ['Hitung Prediksi Diabetes',
    'Chatbot'],
    default_index=0)


#halaman Hitung Prediksi Diabetes
if(selected == 'Hitung Prediksi Diabetes') :
    #membaca model
    diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))

    #judul web
    st.title('Hitung Prediksi Diabetes')

    #membagi kolom
    col1, col2 = st.columns(2)

    with col1 :
        Pregnancies = st.text_input ('masukkan nilai Pregnancies')

    with col2 :
        Glucose = st.text_input ('masukkan nilai Glucose')

    with col1 :
        BloodPressure = st.text_input ('masukkan nilai Blood Pressure')

    with col2 :
        SkinThickness = st.text_input ('masukkan nilai Skin Thickness')

    with col1 :
        Insulin = st.text_input ('masukkan nilai Insulin')

    with col2 :
        BMI = st.text_input ('masukkan nilai BMI')

    with col1 :
        DiabetesPedigreeFunction = st.text_input ('masukkan nilai Diabetes Pedigree Function')

    with col2 :
        Age = st.text_input ('masukkan nilai Age')

    #code untuk prediksi
    diab_diagnosis = ''

    #membuat tombol untuk prediksi
    if st.button('Hitung Result'):
        diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

        if(diab_prediction[0] == 1):
            diab_diagnosis = 'Pasien terkena Diabetes'
        else :
            diab_diagnosis = 'Pasien tidak terkena Diabetes'
   
        st.success(diab_diagnosis)

#halaman Chatbot
if(selected == 'Chatbot'):
    st.title('Chatbot')

    openai.api_key = st.secrets["OPENAI_API_KEY"]

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    #fitur sesi: untuk mencatat histori antara interaksi pengguna
    if "messages" not in st.session_state:
        st.session_state.messages = []

    #fitur untuk menampilkan histori chat sebelumnya
    for messages in st.session_state.messages:
        with st.chat_message(messages["role"]):
            st.markdown(messages["content"])

    #fitur untuk pengguna menginput pertanyaan/promptnya
    if prompt := st.chat_input("What is up?"):

        #untuk menampilkan pesan
        with st.chat_message("user"):
            st.markdown(prompt)

        #untuk menampilkan histori pesan
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            messages_placeholder = st.empty()
            full_response =""

            response = openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=st.session_state.messages,
                stream=True,
            )
            for chunk in response:
                content = chunk['choices'][0]['delta'].get('content','')
                full_response += content
                messages_placeholder.markdown(full_response + " ")

            messages_placeholder.markdown(full_response)
        st.session_state.message.append({"role": "assistant", "content": full_response})