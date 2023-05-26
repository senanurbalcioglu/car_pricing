import numpy as np
import streamlit as st
import pandas as pd
import pickle
import base64
import openpyxl
import xgboost

def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('arkaplan.jpg')


col7,col8,col9=st.columns(3)
with col8:
    st.image("sunum/logo2.png", width=200)


df = pd.read_excel("newOutput_2.xlsx", sheet_name="Sheet1")


col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Marka</span>
                    </div>
                """, unsafe_allow_html=True)
    marka = st.selectbox("Marka",options=sorted(list(df["Marka"].unique())), index=0, label_visibility="collapsed")

    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Seri</span>
                    </div>
                """, unsafe_allow_html=True)
    seri_options = df[df["Marka"] == marka]["Seri"].unique()
    seri = st.selectbox("Seri",options=sorted(list(seri_options)), index=0, label_visibility="collapsed")

    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Model</span>
                    </div>
                """, unsafe_allow_html=True)
    model_options = df[df["Seri"] == seri]["Model"].unique()
    model = st.selectbox("Model",options=sorted(list(model_options)), index=0, label_visibility="collapsed")

    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Yıl</span>
                    </div>
                """, unsafe_allow_html=True)
    yil = st.text_input("Yıl", label_visibility="collapsed")

with col2:
    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Yakıt Tipi</span>
                    </div>
                """, unsafe_allow_html=True)
    yakit_tipi = st.selectbox("Yakıt Tipi",options=list(df["Yakıt Tipi"].unique()) , index=0, label_visibility="collapsed")

    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Vites Tipi</span>
                    </div>
                """, unsafe_allow_html=True)
    vites_tipi = st.selectbox("Vites Tipi",options=list(df["Vites Tipi"].unique()) , index=0, label_visibility="collapsed")

    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Motor Gücü</span>
                    </div>
                """, unsafe_allow_html=True)
    motor_options = df[df["Model"] == model]["Motor Gücü"].unique()
    motor_gucu = st.selectbox("Motor Gücü",options=sorted(list(motor_options)), index=0, label_visibility="collapsed")

    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Motor Hacmi</span>
                    </div>
                """, unsafe_allow_html=True)
    motor_hacmi_options = df[df["Model"] == model]["Motor Hacmi"].unique()
    motor_hacmi = st.selectbox("Motor Hacmi",options=sorted(list(motor_hacmi_options)), index=0, label_visibility="collapsed")

with col3:

    st.markdown(f"""
                <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                    <span style="font-family: Arial; font-size: 24px; color: blue;">Kilometre</span>
                </div>
            """,unsafe_allow_html=True)
    km = st.number_input("kilometre",0,1000000,0,1000, label_visibility="collapsed")

    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Boya Sayısı</span>
                    </div>
                """, unsafe_allow_html=True)
    boya = st.radio( "boya",options=["Boyalı", "Boyasız"], label_visibility="collapsed", key="Radio")

    st.markdown(
        """
        <style>
        .stRadio > div > label {
            background-color: rgba(255, 255, 255, 0.8);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if boya == "Boyalı":
        boya_sayisi = st.selectbox("boyalı", range(1, 13), index=0,
                                      label_visibility="collapsed")
    else:
        boya_sayisi = 0

    st.markdown(f"""
                    <div style="text-align:center;background-color: rgba(255, 255, 255, 0.8); border-radius: 5px; ">
                        <span style="font-family: Arial; font-size: 24px; color: blue;">Değişen Parça Sayısı</span>
                    </div>
                """, unsafe_allow_html=True)
    degisen = st.radio("degisen_sayi",options=["Var", "Yok"], label_visibility="collapsed")
    if degisen == "Var":
        degisen_sayisi = st.selectbox("degisen", range(1,13), index=0,
                                   label_visibility="collapsed")

    else:
        degisen_sayisi = 0




df2 = pd.DataFrame(columns=["Marka","Seri","Model","Yıl","Yakıt Tipi","Vites Tipi","Motor Gücü","Motor Hacmi"
                            ,"Kilometre","Boya","Değişen"])
yeni_veri = {
    "Marka": [marka],
    "Seri": [seri],
    "Model": [model],
    "Yıl": [yil],
    "Yakıt Tipi": [yakit_tipi],
    "Vites Tipi": [vites_tipi],
    "Motor Gücü": [motor_gucu],
    "Motor Hacmi": [motor_hacmi],
    "Kilometre": [km],
    "Boya": [boya_sayisi],
    "Değişen": [degisen_sayisi]
}

df2 = pd.concat([df2, pd.DataFrame(yeni_veri)], ignore_index=True)

sample = df2.copy()

col4, col5, col6 = st.columns(3)
with col5:

    fiyat = st.button("Fiyat", use_container_width=True)

    if fiyat:
        if marka == "Mercedes - Benz":
            name = "Code/Mercedes.pkl"
        else:
            name = "Code/"+marka+".pkl"

        with open(name, "rb") as file:
            f = pickle.load(file)

            df3 = pd.read_excel("markaFile/"+marka+".xlsx")
            df3.drop("Fiyat",axis=1,inplace=True)
            df3.drop("Unnamed: 0", axis=1, inplace=True)

            sutun_isimleri = df3.columns

            # "Seri_A6" sütununun indeksini bulun
            indeks_seri = sutun_isimleri.get_loc("Seri_" + sample["Seri"].values[0])
            indeks_model = sutun_isimleri.get_loc("Model_" + sample["Model"].values[0])
            indeks_yakit_tipi = sutun_isimleri.get_loc("Yakıt Tipi_" + sample["Yakıt Tipi"].values[0])
            indeks_vites_tipi = sutun_isimleri.get_loc("Vites Tipi_" + sample["Vites Tipi"].values[0])

            ru = [0]*len(sutun_isimleri)
            ru[0] = int(sample["Yıl"].values[0])
            ru[1] = sample["Motor Gücü"].values[0]
            ru[2] = sample["Motor Hacmi"].values[0]
            ru[3] = sample["Kilometre"].values[0]
            ru[4] = int(sample["Boya"].values[0])
            ru[5] = int(sample["Değişen"].values[0])

            ru[indeks_seri] = 1
            ru[indeks_model] = 1
            ru[indeks_yakit_tipi] = 1
            ru[indeks_vites_tipi] = 1

            sutun_isimleri = list(sutun_isimleri)
            ru_np = np.array(ru)
            ru_reshaped = ru_np.reshape((1, len(ru_np)))
            ru_ = pd.DataFrame(ru_reshaped, columns=sutun_isimleri)
            new_scaled_data = ru_.copy()
            num_cols = ["Yıl",'Motor Gücü', 'Motor Hacmi', 'Kilometre']
            #scaler = RobustScaler()

            with open('scaler.pickle', 'rb') as file2:
                s = pickle.load(file2)
                new_scaled_data[num_cols] = s.transform(ru_[num_cols])

            result = f.predict(new_scaled_data)

            result = int(result)

            st.markdown(
                f"""
                <div style="text-align: center;background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 10px;">
                    <span style="font-size: 30px; color: red;">{result} TL</span>
                </div>
                """,
                unsafe_allow_html=True
            )
