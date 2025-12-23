import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from core.matrix_utils import verileri_api_ile_getir
from core.ant_algorithm import run_aco

st.set_page_config(page_title="Bursa Rota Optimizasyonu", layout="wide")

st.title("Bursa Liseler Arası En Kısa Yol Güzergahı")

# 1. Algoritma Ayarları (Sidebar)
with st.sidebar:
    st.header("🛠️ Algoritma Ayarları")
    k_sayisi = st.slider("Karınca Sayısı", 5, 50, 20)
    iter_sayisi = st.slider("İterasyon Sayısı", 10, 100, 30)
    alpha = st.slider("Alpha (Feromon Etkisi)", 0.0, 5.0, 1.0)
    beta = st.slider("Beta (Mesafe Etkisi)", 0.0, 5.0, 2.0)
    evap = st.slider("Buharlaşma Oranı", 0.0, 1.0, 0.5)


adresler = [
    "Bursa Büyükşehir Belediyesi, Osmangazi, Bursa",
    "Bursa Anadolu Lisesi, Osmangazi, Bursa",
    "Bursa Anadolu Erkek Lisesi, Osmangazi, Bursa",
    "İMKB Gürsu Anadolu Lisesi, Gürsu, Bursa",
    "Tofaş Fen Lisesi, Nilüfer, Bursa",
    "Nilüfer Borsa İstanbul Fen Lisesi, Nilüfer, Bursa",
    "Ahmet Hamdi Gökbayrak Fen Lisesi, Osmangazi, Bursa",
    "Osmangazi Mesleki ve Teknik Anadolu Lisesi, Osmangazi, Bursa",
    "Yeşilyayla Mesleki ve Teknik Anadolu Lisesi, Osmangazi, Bursa",
    "Ali Osman Sönmez Mesleki ve Teknik Anadolu Lisesi, Osmangazi, Bursa",
    "Atatürk Mesleki ve Teknik Anadolu Lisesi, Osmangazi, Bursa",
    "Görükle Mesleki ve Teknik Anadolu Lisesi, Nilüfer, Bursa",
    "Şehit Ömer Halisdemir Mesleki ve Teknik Anadolu Lisesi, Yıldırım, Bursa",
]

# 2. SESSION STATE: Sonuçları hafızada tutmak için (Kritik Bölüm)
if 'hesaplandi' not in st.session_state:
    st.session_state.hesaplandi = False
    st.session_state.sonuclar = {}

# 3. Hesaplama Butonu
if st.button("Rotayı Oluştur ve Optimize Et"):
    with st.spinner("🚀 Veriler çekiliyor ve karıncalar yola çıkıyor..."):
        koordinatlar, mesafe_matrisi = verileri_api_ile_getir(adresler)

        if koordinatlar and mesafe_matrisi is not None:
            # Algoritmayı çalıştır
            en_iyi_yol, en_kisa_dist, gecmis = run_aco(
                mesafe_matrisi,
                karinca_sayisi=k_sayisi,
                iterasyon_sayisi=iter_sayisi,
                alpha=alpha, beta=beta, buharlasma_orani=evap
            )

            # Sonuçları oturuma kaydet ki kaybolmasınlar
            st.session_state.sonuclar = {
                'koordinatlar': koordinatlar,
                'en_iyi_yol': en_iyi_yol,
                'en_kisa_dist': en_kisa_dist,
                'gecmis': gecmis
            }
            st.session_state.hesaplandi = True
            st.balloons()
        else:
            st.error("❌ Veri çekme aşamasında bir sorun oluştu.")

# 4. SONUÇLARI GÖSTER (Hesaplama yapıldıysa her zaman ekranda kalır)
if st.session_state.hesaplandi:
    res = st.session_state.sonuclar

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📍 En Kısa Rota Haritası")
        m = folium.Map(location=[38.4192, 27.1287], zoom_start=11)

        points = []
        for idx in res['en_iyi_yol']:
            name, (lat, lon) = res['koordinatlar'][idx]
            points.append([lat, lon])
            folium.Marker([lat, lon], tooltip=name, popup=name).add_to(m)

        # Rota çizgisini ekle
        folium.PolyLine(points, color="red", weight=4, opacity=0.7).add_to(m)
        # 'key' eklemek haritanın her saniye yenilenmesini engeller
        st_folium(m, width=700, height=500, key="sonuc_haritasi")

    with col2:
        st.subheader("📊 Analiz")
        st.metric("Toplam Sürüş Mesafesi", f"{res['en_kisa_dist']:.2f} km")

        # Grafik
        df_grafik = pd.DataFrame(res['gecmis'], columns=["Mesafe (km)"])
        st.line_chart(df_grafik)

        with st.expander("Rota Sıralamasını Gör"):
            for i, idx in enumerate(res['en_iyi_yol']):
                st.write(f"**{i + 1}. Durak:** {res['koordinatlar'][idx][0]}")

st.info("Not: İlk durak her zaman İl Milli Eğitim Müdürlüğü olarak ayarlanmıştır.")