import pickle
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
    st.title('GlucoCare Apps')

    #membagi kolom
    col1, col2 = st.columns(2)

    with col1 :
        Pregnancies = st.text_input ('input nilai Pregnancies')

    with col2 :
        Glucose = st.text_input ('input nilai Glucose')

    with col1 :
        BloodPressure = st.text_input ('input nilai Blood Pressure')

    with col2 :
        SkinThickness = st.text_input ('input nilai Skin Thickness')

    with col1 :
        Insulin = st.text_input ('input nilai Insulin')

    with col2 :
        BMI = st.text_input ('input nilai BMI')

    with col1 :
        DiabetesPedigreeFunction = st.text_input ('input nilai Diabetes Pedigree Function')

    with col2 :
        Age = st.text_input ('input nilai Age')

    #code untuk prediksi
    diab_diagnosis = ''

    #membuat tombol untuk prediksi
    if st.button('Hitung Prediksi Diabetes'):
        diab_prediction = diabetes_model.predict([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]])

        if(diab_prediction[0] == 1):
            diab_diagnosis = 'Pasien terkena Diabetes'
        else :
            diab_diagnosis = 'Pasien tidak terkena Diabetes'
   
        st.success(diab_diagnosis)


if(selected == 'Chatbot'):
    st.title('Chatbot')