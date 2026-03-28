import cv2
import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class PoseDetector:
    def __init__(self, detection_confidence=0.7, tracking_confidence=0.7):
        self.model_path = os.path.join(os.path.dirname(__file__), 'pose_landmarker_lite.task')
        self._ensure_model_exists()

        with open(self.model_path, "rb") as f:
            model_bytes = f.read()
            
        base_options = python.BaseOptions(model_asset_buffer=model_bytes)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            output_segmentation_masks=False,
            min_pose_detection_confidence=detection_confidence,
            min_pose_presence_confidence=tracking_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)

        self.landmarks_px = []
        self.h = 0
        self.w = 0

    def _ensure_model_exists(self):
        if not os.path.exists(self.model_path):
            print("[BİLGİ] Pose modeli indiriliyor (sadece ilk sefer için)...")
            url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task"
            try:
                urllib.request.urlretrieve(url, self.model_path)
                print("[BİLGİ] Pose Modeli başarıyla indirildi!")
            except Exception as e:
                print(f"[HATA] Model indirilemedi! {e}")

    def find_pose(self, frame, draw=True):
        self.h, self.w = frame.shape[:2]
        self.landmarks_px = []

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        detection_result = self.detector.detect(mp_image)

        if detection_result.pose_landmarks:
            pose_lms = detection_result.pose_landmarks[0]

            for lm in pose_lms:
                cx = int(lm.x * self.w)
                cy = int(lm.y * self.h)
                self.landmarks_px.append((cx, cy))

            if draw:
                self._draw_landmarks(frame, self.landmarks_px)
            return True
        return False

    def _draw_landmarks(self, frame, lms_px):
        # Draw some essential skeleton lines
        # Nose: 0, Shoulders: 11, 12, Elbows: 13, 14, Wrists: 15, 16 
        POINT_COLOR = (0, 255, 255)
        LINE_COLOR = (255, 0, 255)
        
        connections = [(11, 12), (11, 13), (13, 15), (12, 14), (14, 16), (11, 23), (12, 24), (23, 24)]
        
        for p1, p2 in connections:
            if p1 < len(lms_px) and p2 < len(lms_px):
                cv2.line(frame, lms_px[p1], lms_px[p2], LINE_COLOR, 3, cv2.LINE_AA)
        
        for i, p in enumerate(lms_px):
            if i in [0, 11, 12, 13, 14, 15, 16]: # Sadece ust vucut
                cv2.circle(frame, p, 5, POINT_COLOR, -1, cv2.LINE_AA)

    def get_nose(self):
        if len(self.landmarks_px) > 0:
            return self.landmarks_px[0]
        return None
