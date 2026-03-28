# 🏗️ Yazılım Tasarım Belgesi (SDD) - Okul Öncesi Sanat Evi

## 1. Sistem Mimarisi
Proje, modüler bir mimari üzerine kurulmuştur ve "Katmanlı Mimari" prensiplerini takip eder.

### 1.1. Veri Akış Modeli
1. **Giriş Katmanı:** OpenCV (Kamera görüntüsü yakalama).
2. **Algılama Katmanı:** MediaPipe (Landmark ve landmark koordinat dönüşümü).
3. **Mantık Katmanı:** Gesture recognition (Jest tanıma) ve Oyun mekanikleri.
4. **Sunum Katmanı:** UI Engine (Transparent glass UI) ve Canvas çizim motoru.

## 2. Modül Tanımları

### 2.1. Hand & Pose Detectors (`hand_detector.py`, `pose_detector.py`)
- Ham koordinatları MediaPipe'tan alır.
- Koordinatları ekran çözünürlüğüne (1280x720) normalize eder.
- El jestlerini (Yumruk, İşaret parmağı) sınıflandırır.

### 2.2. Çizim Motoru (`canvas.py`, `templates.py`)
- `NumPy` dizileri üzerinde çizim işlemlerini yürütür.
- `floodFill` algoritması ile şablon boyama yapar.
- Görüntüleri BGR formatında işleterek şeffaf maskeleme uygular.

### 2.3. Kullanıcı Arayüzü (`ui.py`, `ui_engine.py`)
- **Glassmorphism UI:** Gaussian Blur kullanarak buzlu cam efekti oluşturur.
- **Neon Engine:** Birden fazla katman kullanarak parlama ve ışık efektleri sağlar.
- **Particle System:** Arka planda hareketli parçacık simülasyonu yapar.

## 3. Veritabanı ve Depolama
- Sistemde ilişkisel bir veritabanı bulunmamaktadır.
- Kayıtlar `saved_drawings/` klasöründe `.png` formatında saklanır.
- Model ayarları `.task` dosyaları üzerinden yüklenir.

## 4. Kullanılan Teknolojiler
- **Programlama Dili:** Python 3.10+
- **Görüntü İşleme:** OpenCV, NumPy
- **Yapay Zeka:** MediaPipe Solutions (TFLite tabanlı)
