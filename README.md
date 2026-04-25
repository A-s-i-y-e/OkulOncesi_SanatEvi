# 🎨 Minik Eller Atölyesi (AI Destekli Çizim ve Oyun)

Bu proje, çocukların el hareketleri ve vücut takibi ile dijital sanat yapmalarını sağlayan, yapay zeka (MediaPipe) destekli profesyonel bir eğitim ve eğlence uygulamasıdır.

## ✨ Özellikler

-   **🖥️ Premium UI:** 2026 standartlarında Glassmorphism (Buzlu Cam) arayüz ve Neon efektleri.
-   **✍️ Serbest Çizim:** Yapay zeka ile el hareketlerini takip ederek havada çizim yapma.
-   **🪄 Şablon Boyama (Sihirli Doldurma):** 10 farklı şablonu (Ayı, Araba, Roket vb.) taşırmadan tek dokunuşla boyama.
-   **🎈 Balon Patlatma Oyunu:** El koordinasyonunu geliştiren eğlenceli oyun modu.
-   **🍎 Elma Yakala (Tüm Vücut):** Pose tracking teknolojisi ile vücut hareketleriyle oynanan interaktif oyun.
-   **📸 Kayıt Özelliği:** Yapılan sanat eserlerini anında `saved_drawings` klasörüne kaydetme.

## 📁 Proje Dokümantasyonu (Yazılım Mühendisliği)

Bu proje, akademik standartlara uygun olarak dökümante edilmiştir:
-   [📄 Yazılım Gereksinim Belirtimi (SRS)](docs/SRS.md)
-   [🏗️ Yazılım Tasarım Belgesi (SDD)](docs/SDD.md)
-   [🧪 Test Planı ve Raporu](docs/TEST_PLAN.md)

## 🚀 Kurulum ve Çalıştırma

1.  **Gereksinimleri Yükleyin:**
    ```bash
    pip install opencv-python mediapipe numpy
    ```

2.  **Uygulamayı Başlatın:**
    ```bash
    python main.py
    ```

## 🎮 Kontroller

-   **İşaret Parmağı:** Çizim yapma ve Menü etkileşimi.
-   **[M] Tuşu:** Ana Menüye dönme.
-   **[S] Tuşu:** Çizimi kaydetme.
-   **[C] Tuşu:** Ekranı temizleme.
-   **[Q] veya ESC:** Çıkış.

---
*Bu proje OpenCV ve MediaPipe kullanılarak geliştirilmiştir.*
