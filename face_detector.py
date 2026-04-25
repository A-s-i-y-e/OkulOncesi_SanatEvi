"""
face_detector.py
Yüz algılama modülü - MediaPipe Tasks API kullanarak 
ekranda bir çocuk olup olmadığını belirler.
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request

class FaceDetector:
    def __init__(self, min_detection_confidence=0.5):
        # 1. Model dosyasını indir/kontrol et
        self.model_path = os.path.join(os.path.dirname(__file__), 'face_detector.task')
        self._ensure_model_exists()

        # 2. MediaPipe Task Ayarları
        try:
            with open(self.model_path, "rb") as f:
                model_bytes = f.read()
                
            base_options = python.BaseOptions(model_asset_buffer=model_bytes)
            options = vision.FaceDetectorOptions(
                base_options=base_options,
                min_detection_confidence=min_detection_confidence
            )
            self.detector = vision.FaceDetector.create_from_options(options)
        except Exception as e:
            print(f"[HATA] FaceDetector başlatılamadı: {e}")
            self.detector = None

    def _ensure_model_exists(self):
        """Face detection model dosyasını indirir."""
        if not os.path.exists(self.model_path):
            print("[BİLGİ] Yüz tanıma modeli indiriliyor (sadece ilk sefer için)...")
            # Doğru model URL'si
            url = "https://storage.googleapis.com/mediapipe-models/face_detector/blaze_face_short_range/float16/1/face_detector.task"
            try:
                # SSL sertifika hatalarını önlemek için context oluşturulabilir gerekirse
                urllib.request.urlretrieve(url, self.model_path)
                print("[BİLGİ] Model başarıyla indirildi!")
            except Exception as e:
                print(f"[HATA] Model indirilemedi! URL: {url}\nHata: {e}")

    def is_face_present(self, frame):
        """Ekranda en az bir yüz olup olmadığını döndürür."""
        if self.detector is None:
            return False
            
        try:
            # MP formatına çevir
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # Tespit yap
            detection_result = self.detector.detect(mp_image)
            
            return len(detection_result.detections) > 0
        except:
            return False
