"""
hand_detector.py
El algılama modülü - MediaPipe Hands kullanarak kamera görüntüsünden
el landmarklarını, parmak durumlarını ve jest tipini belirler.
Yeni sürüm MediaPipe Tasks API uyumludur.
"""

import cv2
import time
import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision


class HandDetector:
    """
    MediaPipe Tasks HandLandmarker wrapper sınıfı.
    El landmarklarını tespit eder, parmak durumlarını ve jestleri belirler.
    """

    FINGER_TIPS = [4, 8, 12, 16, 20]   
    FINGER_PIP =  [3, 6, 10, 14, 18]   
    GESTURE_HOLD_TIME = 0.5

    def __init__(self, max_hands=1, detection_confidence=0.75, tracking_confidence=0.75):
        # 1. Model dosyasını indir/kontrol et
        self.model_path = os.path.join(os.path.dirname(__file__), 'hand_landmarker.task')
        self._ensure_model_exists()

        # 2. MediaPipe Task Ayarları
        # Türkçe karakterli (Ö, Ş, İ) klasör yollarında hatayı önlemek için 
        # dosyayı bayt olarak okuyup model_asset_buffer ile veriyoruz.
        with open(self.model_path, "rb") as f:
            model_bytes = f.read()
            
        base_options = python.BaseOptions(model_asset_buffer=model_bytes)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_confidence,
            min_hand_presence_confidence=tracking_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.detector = vision.HandLandmarker.create_from_options(options)

        self.landmarks = []          
        self.landmarks_px = []       
        self.h = 0
        self.w = 0

        # Jest sabitleme
        self._last_gesture = None
        self._gesture_start_time = 0.0
        self._confirmed_gesture = None

    def _ensure_model_exists(self):
        """Google'ın model dosyasını otomatik olarak indirir."""
        if not os.path.exists(self.model_path):
            print("[BİLGİ] Yapay zeka modeli indiriliyor (sadece ilk sefer için)...")
            url = "https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task"
            try:
                urllib.request.urlretrieve(url, self.model_path)
                print("[BİLGİ] Model başarıyla indirildi!")
            except Exception as e:
                print(f"[HATA] Model indirilemedi! İnternet bağlantınızı kontrol edin. Hata: {e}")

    def find_hands(self, frame, draw=True):
        self.h, self.w = frame.shape[:2]
        self.landmarks = []
        self.landmarks_px = []
        self.all_hands = []

        # MP formatına çevir
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Elleri bul
        detection_result = self.detector.detect(mp_image)

        if detection_result.hand_landmarks:
            # Geriye dönük uyumluluk için ilk eli al
            hand_lms = detection_result.hand_landmarks[0]
            self.landmarks = hand_lms

            for hlms in detection_result.hand_landmarks:
                lms_px = []
                for lm in hlms:
                    cx = int(lm.x * self.w)
                    cy = int(lm.y * self.h)
                    lms_px.append((cx, cy))
                
                if draw:
                    self._draw_landmarks(frame, lms_px)
                    
                raw_gest = self._detect_gesture_for_hand(lms_px)
                idx_tip = lms_px[8] if len(lms_px) > 8 else None
                
                self.all_hands.append({
                    'landmarks_px': lms_px,
                    'raw_gesture': raw_gest,
                    'index_tip': idx_tip
                })
            
            self.landmarks_px = self.all_hands[0]['landmarks_px']
            return True
        return False

    def get_all_hands(self):
        """Tüm algılanan elleri liste olarak döndürür."""
        if not hasattr(self, 'all_hands'):
            return []
        return self.all_hands

    def _draw_landmarks(self, frame, landmarks_px):
        """Basit bir el iskeleti çizer (MediaPipe tasks API kendi çizicisini sağlamaz, kendimiz çiziyoruz)"""
        connections = [
            (0, 1), (1, 2), (2, 3), (3, 4),        # Thumb
            (0, 5), (5, 6), (6, 7), (7, 8),        # Index
            (5, 9), (9, 10), (10, 11), (11, 12),   # Middle
            (9, 13), (13, 14), (14, 15), (15, 16), # Ring
            (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Pinky
        ]
        
        # Çizgiler
        for p1, p2 in connections:
            if p1 < len(landmarks_px) and p2 < len(landmarks_px):
                cv2.line(frame, landmarks_px[p1], landmarks_px[p2], (0, 255, 0), 2, cv2.LINE_AA)
        
        # Noktalar
        for p in landmarks_px:
            cv2.circle(frame, p, 4, (0, 0, 255), -1, cv2.LINE_AA)

    def get_index_tip(self):
        if len(self.landmarks_px) > 8:
            return self.landmarks_px[8]
        return None

    def get_landmark(self, index):
        if len(self.landmarks_px) > index:
            return self.landmarks_px[index]
        return None

    def _get_finger_states_for_hand(self, lms_px):
        if len(lms_px) < 21:
            return [False] * 5

        import math
        states = []
        wrist = lms_px[0]

        def dist(p1, p2):
            return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

        # Baş parmak kontrolü (Açıya ve el yönüne tam duyarsız)
        thumb_tip = lms_px[4]
        thumb_base = lms_px[2]  # Thumb MCP
        pinky_base = lms_px[17] # Pinky MCP
        states.append(dist(thumb_tip, pinky_base) > dist(thumb_base, pinky_base) * 1.1)

        # Diğer parmaklar: Uç noktanın (Tip) bileğe (Wrist) olan uzaklığı,
        # MCP (parmak kökü) noktasının bileğe olan uzaklığı ile oranlanır.
        # Böylece çocuk parmağını hafif kıvırsa bile "çizme" işlemi kesintiye uğramaz.
        FINGER_MCP = [2, 5, 9, 13, 17]
        for tip_idx, mcp_idx in zip(self.FINGER_TIPS[1:], FINGER_MCP[1:]):
            tip_dist = dist(lms_px[tip_idx], wrist)
            mcp_dist = dist(lms_px[mcp_idx], wrist)
            # Eğer uç, kök eklemden %10 bile daha uzaktaysa parmak açıktır.
            states.append(tip_dist > mcp_dist * 1.1)

        return states

    def get_finger_states(self):
        return self._get_finger_states_for_hand(self.landmarks_px)

    def _detect_gesture_for_hand(self, lms_px):
        if not lms_px:
            return 'none'
        s = self._get_finger_states_for_hand(lms_px)
        thumb, index, middle, ring, pinky = s

        if index and not middle and not ring and not pinky: return 'draw'
        elif index and middle and not ring and not pinky: return 'erase'
        elif thumb and index and middle and ring and pinky: return 'clear'
        elif thumb and not index and not middle and not ring and not pinky: return 'save'
        elif not thumb and not index and not middle and not ring and not pinky: return 'color'
        elif thumb and index and not middle and not ring and pinky: return 'triangle' # 🤟 Spiderman
        elif not thumb and index and not middle and not ring and pinky: return 'star' # 🤘 Rock
        else: return 'none'

    def detect_gesture(self):
        return self._detect_gesture_for_hand(self.landmarks_px)

    def get_stable_gesture(self):
        raw = self.detect_gesture()
        now = time.time()
        if raw != self._last_gesture:
            self._last_gesture = raw
            self._gesture_start_time = now

        elapsed = now - self._gesture_start_time
        if elapsed >= self.GESTURE_HOLD_TIME and raw != 'none':
            self._confirmed_gesture = raw
        elif raw == 'none':
            self._confirmed_gesture = 'none'

        return self._confirmed_gesture or 'none'

    def get_raw_gesture(self):
        return self.detect_gesture()
