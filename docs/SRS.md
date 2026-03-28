# 📄 Yazılım Gereksinim Belirtimi (SRS) - Okul Öncesi Sanat Evi

## 1. Giriş
Bu belge, **Okul Öncesi Sanat Evi** projesi için hazırlanan yazılım gereksinim belgesidir. Proje, okul öncesi çocukların el hareketleri ve vücut takibi ile dijital ortamda sanat yapmalarına ve eğitici oyunlar oynamalarına yardımcı olmayı amaçlar.

## 2. Genel Özellikler
Uygulama, MediaPipe kütüphanesi ile gerçek zamanlı görüntü işleme yaparak el ve vücut konumlarını tespit eder.

### 2.1. Fonksiyonel Gereksinimler (FR)
- **FR_01 (El Takibi):** Sistem, aynı anda 2 elin parmak uçlarını ve jestlerini takip edebilmelidir.
- **FR_02 (Serbest Çizim):** İşaret parmağı ile ekranda serbestçe çizim yapılabilmelidir.
- **FR_03 (Şablon Boyama):** Sistem, kapalı alanları (flood-fill) tek dokunuşla seçili renkle doldurabilmelidir.
- **FR_04 (Balon Oyunu):** Koordinasyon gelişimi için parmak ucuyla balon patlatma mekanizması sunulmalıdır.
- **FR_05 (Vücut Takibi):** Kullanıcı, vücut (burun/kafa) hareketiyle ekrandaki bir sepeti kontrol edebilmelidir.
- **FR_06 (Kaydetme):** Yapılan çizimler yerel disk üzerine resim dosyası olarak kaydedilebilmelidir.

### 2.2. Fonksiyonel Olmayan Gereksinimler (NFR)
- **NFR_01 (Performans):** Görüntü işleme süreci saniyede en az 25 kare (FPS) işleme hızı sunmalıdır.
- **NFR_02 (Kullanılabilirlik):** Arayüz, okul öncesi çocukların anlayabileceği görsel ikonlar ve neon ışıklar içermelidir.
- **NFR_03 (Hata Toleransı):** Kamera bağlantısı koptuğunda sistem çökmeden uyarı vermelidir.

## 3. Kullanım Durumları (Use Cases)
- **Çizen Çocuk:** Havada elini hareket ettirerek resim yapar.
- **Boyayan Çocuk:** Bir şablon seçer (Ayı, Ev) ve bölümleri renklendirir.
- **Oyuncu Çocuk:** Balon patlatır veya düşen elmaları toplar.
- **Veli/Öğretmen:** Çizimleri kaydeder ve geçmiş çalışmaları inceler.
