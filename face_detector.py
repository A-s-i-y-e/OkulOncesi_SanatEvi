"""
face_detector.py
Gülümseme Algılama Modülü - MediaPipe Face Landmarker kullanarak 
kullanıcının gülümsediğini tespit eder.
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request
import math

class FaceDetector:
    def __init__(self):
        # 1. Face Landmarker Modelini İndir
        self.model_path = os.path.join(os.path.dirname(__file__), 'face_landmarker.task')
        self._ensure_model_exists()

        # 2. MediaPipe Task Ayarları
        self.detector = None
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    model_bytes = f.read()
                
                base_options = python.BaseOptions(model_asset_buffer=model_bytes)
                # Blendshapes (gülümseme gibi ifadeler) için ayarlar
                options = vision.FaceLandmarkerOptions(
                    base_options=base_options,
                    output_face_blendshapes=True,
                    output_facial_transformation_matrixes=True,
                    num_faces=1
                )
                self.detector = vision.FaceLandmarker.create_from_options(options)
            except Exception as e:
                print(f"[HATA] FaceLandmarker başlatılamadı: {e}")

    def _ensure_model_exists(self):
        """Face landmarker model dosyasını indirir."""
        if not os.path.exists(self.model_path):
            print("[BİLGİ] Gülümseme algılama modeli indiriliyor...")
            url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
            try:
                urllib.request.urlretrieve(url, self.model_path)
                print("[BİLGİ] Model başarıyla indirildi!")
            except Exception as e:
                print(f"[HATA] Model indirilemedi! {e}")

    def get_smile_score(self, frame):
        """
        Kullanıcının gülümseme skorunu döner (0.0 - 1.0 arası).
        """
        if self.detector is None: return 0.0
        
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            result = self.detector.detect(mp_image)
            
            if result.face_blendshapes:
                # MediaPipe Blendshapes içinde mouthSmileLeft ve mouthSmileRight değerlerini ara
                # Bu değerler 0.0 ile 1.0 arasında gelir.
                blendshapes = result.face_blendshapes[0]
                smile_left = 0.0
                smile_right = 0.0
                
                for bs in blendshapes:
                    if bs.category_name == 'mouthSmileLeft':
                        smile_left = bs.score
                    elif bs.category_name == 'mouthSmileRight':
                        smile_right = bs.score
                
                # İki tarafın ortalamasını al
                return (smile_left + smile_right) / 2.0
        except:
            pass
        return 0.0

    def is_smiling(self, frame, threshold=0.45):
        """Kullanıcının yeterince gülümseyip gülümsemediğini kontrol eder."""
        return self.get_smile_score(frame) > threshold
