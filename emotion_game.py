"""
emotion_game.py
Duygu Aynası Oyunu - Görsel Emoji rehberliğinde duygu tanıma oyunu.
"""

import cv2
import time
import numpy as np
from ui_engine import draw_neon_text, draw_glass_panel

class EmotionGame:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        
        # Oyun seviyeleri - Emoji odaklı
        self.levels = [
            {'name': 'MUTLU', 'target': 'smile', 'threshold': 0.55},
            {'name': 'SASKIN', 'target': 'jaw_open', 'threshold': 0.5},
            {'name': 'GOZ KIRP', 'target': 'blink_left', 'threshold': 0.7},
            {'name': 'COK MUTLU', 'target': 'smile', 'threshold': 0.85}
        ]
        
        self.current_level_idx = 0
        self.score = 0
        self.is_success = False
        self.success_time = 0
        self.pulse = 0.0 # Başarı anındaki büyüme efekti

    def update(self, face_data):
        if self.is_success:
            self.pulse = min(1.5, self.pulse + 0.1)
            if time.time() - self.success_time > 1.5:
                self.next_level()
            return

        level = self.levels[self.current_level_idx]
        if face_data.get(level['target'], 0) > level['threshold']:
            self.is_success = True
            self.success_time = time.time()
            self.score += 10
            self.pulse = 1.0

    def next_level(self):
        self.current_level_idx = (self.current_level_idx + 1) % len(self.levels)
        self.is_success = False
        self.pulse = 0.0

    def draw_target_emoji(self, img, level_name, x, y, size, color, face_data_mock):
        """
        Hedef ifadeyi (emoji şeklinde) ekrana çizer. 
        Bu emoji sabit bir rehberdir.
        """
        cx, cy = x, y
        r = size
        
        # Rehber emojinin rengi (yumușak beyaz/neon)
        base_color = color
        
        # Kafa
        cv2.circle(img, (cx, cy), r, base_color, 3, cv2.LINE_AA)
        
        # Gözler ve Ağız (Level ismine göre şekil alır)
        if level_name == 'MUTLU' or level_name == 'COK MUTLU':
            # Gülen Gözler
            cv2.circle(img, (cx - 40, cy - 30), 12, base_color, -1, cv2.LINE_AA)
            cv2.circle(img, (cx + 40, cy - 30), 12, base_color, -1, cv2.LINE_AA)
            # Gülen Ağız
            cv2.ellipse(img, (cx, cy + 20), (60, 40), 0, 0, 180, base_color, 5, cv2.LINE_AA)
        
        elif level_name == 'SASKIN':
            # Yuvarlak Gözler
            cv2.circle(img, (cx - 40, cy - 30), 15, base_color, 3, cv2.LINE_AA)
            cv2.circle(img, (cx + 40, cy - 30), 15, base_color, 3, cv2.LINE_AA)
            # Yuvarlak Ağız
            cv2.circle(img, (cx, cy + 50), 30, base_color, 4, cv2.LINE_AA)
            
        elif level_name == 'GOZ KIRP':
            # Sol Göz Kapalı (Çizgi)
            cv2.line(img, (cx - 55, cy - 30), (cx - 25, cy - 30), base_color, 4, cv2.LINE_AA)
            # Sağ Göz Açık
            cv2.circle(img, (cx + 40, cy - 30), 12, base_color, -1, cv2.LINE_AA)
            # Hafif Gülümseme
            cv2.ellipse(img, (cx, cy + 20), (50, 20), 0, 0, 180, base_color, 4, cv2.LINE_AA)

    def draw(self, img, face_data):
        level = self.levels[self.current_level_idx]
        
        # 1. Arka Plan Karartma (Odağı merkeze al)
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (self.w, self.h), (20, 10, 30), -1)
        cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)
        
        # 2. Üst Bilgi Paneli
        draw_glass_panel(img, 50, 20, 200, 60, 15, color=(255, 255, 100), alpha=0.2)
        cv2.putText(img, f"YILDIZ: {self.score}", (70, 60), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
        
        # 3. MERKEZİ HEDEF EMOJİ (REHBER)
        # Başarı anında emoji büyür (pulse efekti)
        scale = 1.0 + (self.pulse * 0.2)
        target_size = int(120 * scale)
        color = (0, 255, 0) if self.is_success else (255, 255, 255)
        
        self.draw_target_emoji(img, level['name'], self.w//2, self.h//2, target_size, color, face_data)
        
        # 4. Alt Bilgi (Küçük simge ile)
        if not self.is_success:
            cv2.putText(img, "AYNISINI YAP!", (self.w//2 - 100, self.h//2 + 200), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
        else:
            draw_neon_text(img, "HARIKASIN!", self.w//2 - 100, self.h//2 + 200, cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 3)

        # 5. Geri Dön Butonu
        cv2.rectangle(img, (self.w - 180, 20), (self.w - 20, 70), (50, 50, 200), -1)
        cv2.putText(img, "CIKIS [M]", (self.w - 165, 55), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

        return img
