"""
face_detector.py
Gülümseme ve Yüz Taklit Modülü - MediaPipe Face Landmarker kullanarak 
kullanıcının ifadelerini (gülümseme, göz kırpma, ağız açma) takip eder.
"""

import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import os
import urllib.request

class FaceDetector:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), 'face_landmarker.task')
        self._ensure_model_exists()

        self.detector = None
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    model_bytes = f.read()
                
                base_options = python.BaseOptions(model_asset_buffer=model_bytes)
                options = vision.FaceLandmarkerOptions(
                    base_options=base_options,
                    output_face_blendshapes=True,
                    num_faces=1
                )
                self.detector = vision.FaceLandmarker.create_from_options(options)
            except Exception as e:
                print(f"[HATA] FaceLandmarker başlatılamadı: {e}")

    def _ensure_model_exists(self):
        if not os.path.exists(self.model_path):
            print("[BİLGİ] Yüz analiz modeli indiriliyor...")
            url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
            urllib.request.urlretrieve(url, self.model_path)

    def get_face_data(self, frame):
        """
        Gülümseme, göz kırpma ve ağız açıklığı verilerini döner.
        """
        data = {
            'smile': 0.0,
            'blink_left': 0.0,
            'blink_right': 0.0,
            'jaw_open': 0.0,
            'present': False
        }
        
        if self.detector is None: return data
        
        try:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            result = self.detector.detect(mp_image)
            
            if result.face_blendshapes:
                data['present'] = True
                blendshapes = result.face_blendshapes[0]
                
                for bs in blendshapes:
                    if bs.category_name == 'mouthSmileLeft': data['smile'] += bs.score / 2
                    elif bs.category_name == 'mouthSmileRight': data['smile'] += bs.score / 2
                    elif bs.category_name == 'eyeBlinkLeft': data['blink_left'] = bs.score
                    elif bs.category_name == 'eyeBlinkRight': data['blink_right'] = bs.score
                    elif bs.category_name == 'jawOpen': data['jaw_open'] = bs.score
        except:
            pass
        return data

    def is_face_present(self, frame):
        """Eski kodlarla uyumluluk için."""
        d = self.get_face_data(frame)
        return d['present']

    def get_smile_score(self, frame):
        """Eski kodlarla uyumluluk için."""
        return self.get_face_data(frame)['smile']
