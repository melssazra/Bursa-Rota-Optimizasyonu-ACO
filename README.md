Bursa İl Milli Eğitim Müdürlüğü Rota Optimizasyonu (ACO)
Bu proje, Bursa ilindeki 15 farklı lisenin en verimli şekilde ziyaret edilebilmesi için Karınca Kolonisi Algoritması (Ant Colony Optimization - ACO) kullanılarak geliştirilmiş bir rota optimizasyon sistemidir.

Projenin Amacı
Bursa İl Milli Eğitim Müdürlüğü'nden yola çıkan bir yetkilinin; Nilüfer, Osmangazi, Yıldırım, İnegöl ve Mudanya gibi farklı ilçelerde bulunan 12 okulu en kısa mesafeyi kat ederek ziyaret etmesini ve başlangıç noktasına geri dönmesini sağlamaktır. Projede kuş uçuşu mesafe yerine, Google Maps API kullanılarak gerçek zamanlı sürüş mesafeleri baz alınmıştır.

Kullanılan Teknolojiler
Python 3.9+: Uygulamanın geliştirildiği ana dil.

Streamlit: Web tabanlı interaktif kullanıcı arayüzü.

Google Maps API: Okul koordinatlarını (Geocoding) ve gerçek yol mesafelerini (Distance Matrix) çekmek için kullanılmıştır.

Folium: Hesaplanan rotanın interaktif bir harita üzerinde görselleştirilmesini sağlar.

Numpy & Pandas: Matematiksel modelleme ve veri yönetimi için kullanılmıştır.

Algoritma: Karınca Kolonisi (ACO)
Algoritma, doğadaki karıncaların feromon izlerini takip ederek en kısa yolu bulma davranışını simüle eder. Her adımda bir sonraki okul belirli bir matematiksel olasılık formülüne göre seçilir.


Öne Çıkan Özellikler
Yüksek Hassasiyet: Koordinat hesaplamaları ödev şartlarına uygun olarak virgülden sonra 4 basamak hassasiyetle yapılmaktadır.

Dinamik Analiz: Algoritmanın her iterasyonda rotayı nasıl kısalttığı canlı bir grafik üzerinden takip edilebilir.

Güvenlik: API anahtarları .env dosyası ile korunmakta ve GitHub reposuna dahil edilmemektedir.
