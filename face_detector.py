"""
face_detector.py
Yüz algılama modülü - MediaPipe Face Detection kullanarak 
ekranda bir çocuk olup olmadığını belirler.
"""

import cv2
import mediapipe as mp
import os
import urllib.request

class FaceDetector:
    def __init__(self, min_detection_confidence=0.5):
        # Model dosyasını kontrol et (Face Detection için genelde yerleşiktir ama Tasks API için gerekebilir)
        # MediaPipe Hands gibi Task API kullanacağız
        self.mp_face_detection = mp.solutions.face_detection
        self.detector = self.mp_face_detection.FaceDetection(
            model_selection=0, # 0: Yakın mesafe (2m), 1: Uzak mesafe (5m)
            min_detection_confidence=min_detection_confidence
        )
        
        self.results = None

    def find_faces(self, frame):
        """Karedeki yüzleri bulur."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.detector.process(rgb_frame)
        
        faces = []
        if self.results.detections:
            for detection in self.results.detections:
                # Koordinatları al
                bbox = detection.location_data.relative_bounding_box
                ih, iw, ic = frame.shape
                x, y, w, h = int(bbox.xmin * iw), int(bbox.ymin * ih), \
                             int(bbox.width * iw), int(bbox.height * ih)
                faces.append([x, y, w, h])
        return faces

    def is_face_present(self, frame):
        """Ekranda en az bir yüz olup olmadığını döndürür."""
        faces = self.find_faces(frame)
        return len(faces) > 0
