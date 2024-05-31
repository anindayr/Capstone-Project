import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
import pickle
import openai
import streamlit as st
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler
from streamlit_option_menu import option_menu

with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie'] ['name'],
    config['cookie'] ['key'],
    config['cookie'] ['expiry_days'],
    config['pre-authorized']
)

left_pane, right_pane = st.columns(2)
with left_pane:
    name, state, username = authenticator.login()
with right_pane:
    if not st.session_state["authentication_status"]:
        try:
            email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(pre_authorization=False)
            if email_of_registered_user:
                st.success('User registered successfully')
                with open('config.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)

if st.session_state["authentication_status"]:
    authenticator.logout()

    #programnya masuk sini
    with open('scaler.sav', "rb") as f:
        scaler = pickle.load(f)

    #navigasi sidebar
    with st.sidebar :
        selected = option_menu('GlucoCare Apps', 
        ['Hitung Prediksi Diabetes',
        'Chatbot',
        'Setting'
        ],
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
            Glucose = st.text_input ('masukkan nilai Kadar Gula')

        with col2 :
            BloodPressure = st.text_input ('masukkan nilai Tekanan Darah')

        with col1 :
            BMI = st.text_input ('masukkan nilai BMI')

        with col2 :
            Age = st.text_input ('masukkan nilai Umur')

        #code untuk prediksi
        diab_diagnosis = ''

        #membuat tombol untuk prediksi
        if st.button('Hitung Result'):
            x=(Glucose, BloodPressure, BMI, Age)
            x=np.array(x)
            x=x.reshape(1,-1)
            x=scaler.transform(x)
            diab_prediction = diabetes_model.predict(x)

            st.write(diab_prediction)
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

    #halaman Setting
    if(selected == 'Setting'):
        st.title('Setting')

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')