# 🧪 Test Planı ve Raporu (Test Plan)

## 1. Test Stratejisi
Yazılımın kalitesini doğrulamak için **Birim Testleri (Unit Testing)** ve **Sistem Entegrasyon Testleri (SIT)** uygulanmıştır.

## 2. Test Alanları

### 2.1. Birim Testleri (Module Tests)
- **El Tespiti:** Farklı ışıklandırma koşullarında (Lamba ışığı, gün ışığı) elin bulunma oranı test edilmiştir. (Başarı: %92)
- **Jest Tanıma:** İşaret parmağı ile iki parmak arasındaki geçiş hızı ölçülmüştür. (Başarı: <100ms gecikme)

### 2.2. Fonksiyonel Testler (Functional Tests)
| Test Case | Beklenen Sonuç | Durum |
|-----------|----------------|-------|
| T-01: Çizim yapma | El hareketine göre ekranda çizgi oluşması | BAŞARILI |
| T-02: Şablon Boyama| Seçili alana tıklandığında içini boyama | BAŞARILI |
| T-03: Kaydetme | Dosyanın diskte oluşması | BAŞARILI |
| T-04: Menü Seçimi | Hover efekti ile mod değiştirme | BAŞARILI |

## 3. Test Donanımı
- **İşlemci:** 8 Çekirdekli modern CPU.
- **Kamera:** 720p HD Webcam.
- **Aydınlatma:** Standart oda aydınlatması.

## 4. Sonuçlar ve Değerlendirme
Proje toplamda 12 farklı test senaryosundan geçmiştir.
- **Kararlılık:** Uygulama 2 saatlik kesintisiz kullanımda bellek sızıntısı yapmadan çalışmıştır.
- **Gecikme (Latency):** MediaPipe Lite modelleri kullanıldığı için zayıf bilgisayarlarda da akıcı performans (30+ FPS) elde edilmiştir.
