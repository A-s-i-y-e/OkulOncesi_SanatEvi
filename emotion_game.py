"""
emotion_game.py
Duygu Aynası Oyunu - Tamamen ikon tabanlı sürüm.
"""

import cv2
import time
import numpy as np
import os
from ui_engine import draw_neon_text, draw_glass_panel

class EmotionGame:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        
        # İkonları yükle
        self.icon_star = cv2.imread('icon_star.png')
        if self.icon_star is not None: self.icon_star = cv2.resize(self.icon_star, (40, 40))

        self.levels = [
            {'name': 'GULUMSE', 'target': 'smile', 'threshold': 0.45, 'color': (100, 255, 255)},
            {'name': 'SASIR', 'target': 'jaw_open', 'threshold': 0.30, 'color': (255, 150, 50)},
            {'name': 'SOL GOZ KIRP', 'target': 'blink_left', 'threshold': 0.6, 'color': (200, 100, 255)},
            {'name': 'YANAK SISIR', 'target': 'jaw_open', 'threshold': 0.1, 'color': (100, 255, 100)},
            {'name': 'SAG GOZ KIRP', 'target': 'blink_right', 'threshold': 0.6, 'color': (50, 200, 255)},
            {'name': 'KOCAMAN GUL', 'target': 'smile', 'threshold': 0.80, 'color': (255, 100, 100)},
            {'name': 'AGZINI AC', 'target': 'jaw_open', 'threshold': 0.6, 'color': (100, 100, 255)},
            {'name': 'GOZLERI KAPAT', 'target': 'blink_left', 'threshold': 0.8, 'color': (255, 255, 255)},
        ]
        self.current_level_idx = 0
        self.score = 0
        self.is_success = False
        self.success_time = 0
        self.pulse = 0.0

    def trigger_success(self):
        if not self.is_success:
            self.is_success = True
            self.success_time = time.time()
            self.score += 20
            self.pulse = 1.0

    def update(self, face_data):
        if self.is_success:
            self.pulse = min(1.6, self.pulse + 0.08)
            if time.time() - self.success_time > 1.5:
                self.next_level()
        else:
            level = self.levels[self.current_level_idx]
            if level['name'] == 'GOZLERI KAPAT':
                if face_data.get('blink_left', 0) > 0.7 and face_data.get('blink_right', 0) > 0.7:
                    self.trigger_success()
            else:
                if face_data.get(level['target'], 0) > level['threshold']:
                    self.trigger_success()

    def next_level(self):
        self.current_level_idx = (self.current_level_idx + 1) % len(self.levels)
        self.is_success = False
        self.pulse = 0.0

    def draw_target_emoji(self, img, level_name, x, y, size, color):
        cx, cy = x, y
        r = size
        cv2.circle(img, (cx, cy), r, color, 4, cv2.LINE_AA)
        
        if 'GUL' in level_name:
            cv2.circle(img, (cx - 40, cy - 30), 15, color, -1, cv2.LINE_AA)
            cv2.circle(img, (cx + 40, cy - 30), 15, color, -1, cv2.LINE_AA)
            cv2.ellipse(img, (cx, cy + 20), (70, 50), 0, 0, 180, color, 6, cv2.LINE_AA)
        elif 'SASIR' in level_name or 'AGZ' in level_name:
            cv2.circle(img, (cx - 45, cy - 35), 20, color, 3, cv2.LINE_AA)
            cv2.circle(img, (cx + 45, cy - 35), 20, color, 3, cv2.LINE_AA)
            mouth_r = 50 if 'AGZ' in level_name else 25
            cv2.circle(img, (cx, cy + 45), mouth_r, color, 5, cv2.LINE_AA)
        elif 'KIRP' in level_name:
            if 'SAG' in level_name:
                cv2.line(img, (cx + 25, cy - 35), (cx + 65, cy - 35), color, 5, cv2.LINE_AA)
                cv2.circle(img, (cx - 40, cy - 30), 15, color, -1, cv2.LINE_AA)
            else:
                cv2.line(img, (cx - 65, cy - 35), (cx - 25, cy - 35), color, 5, cv2.LINE_AA)
                cv2.circle(img, (cx + 40, cy - 30), 15, color, -1, cv2.LINE_AA)
            cv2.ellipse(img, (cx, cy + 25), (55, 25), 0, 0, 180, color, 5, cv2.LINE_AA)
        elif 'KAPAT' in level_name:
            cv2.line(img, (cx - 65, cy - 35), (cx - 25, cy - 35), color, 5, cv2.LINE_AA)
            cv2.line(img, (cx + 25, cy - 35), (cx + 65, cy - 35), color, 5, cv2.LINE_AA)
            cv2.ellipse(img, (cx, cy + 25), (40, 10), 0, 0, 180, color, 5, cv2.LINE_AA)
        elif 'SISIR' in level_name:
            cv2.circle(img, (cx - 40, cy - 30), 15, color, -1, cv2.LINE_AA)
            cv2.circle(img, (cx + 40, cy - 30), 15, color, -1, cv2.LINE_AA)
            cv2.circle(img, (cx, cy + 50), 40, color, 4, cv2.LINE_AA)

    def draw(self, img, face_data):
        level = self.levels[self.current_level_idx]
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (self.w, self.h), (15, 10, 25), -1)
        cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)
        
        # --- LOGO VE BASLIK (Üst Orta) ---
        lx, ly = self.w // 2 - 180, 35
        cv2.circle(img, (lx, ly), 10, (255, 255, 255), -1, cv2.LINE_AA)
        finger_colors = [(0,0,255), (0,255,255), (0,255,0), (255,0,0), (255,0,255)]
        for i, color in enumerate(finger_colors):
            angle = -160 + i * 40
            rad = np.deg2rad(angle)
            fx, fy = int(lx + np.cos(rad) * 18), int(ly + np.sin(rad) * 18)
            cv2.line(img, (lx, ly), (fx, fy), color, 4, cv2.LINE_AA)
        draw_neon_text(img, "MINIK ELLER ATOLYESI", self.w // 2 - 155, 45, cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 100, 255), 1)

        # 1. Puan Paneli (Sadece Yıldız İkonu ve Rakam)
        draw_glass_panel(img, 40, 20, 180, 60, 15, color=level['color'], alpha=0.3)
        if self.icon_star is not None:
            # Yıldız ikonu
            img[30:70, 50:90] = cv2.max(img[30:70, 50:90], self.icon_star)
        cv2.putText(img, f"{self.score}", (100, 62), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
        
        # Seviye ilerleme (Alt barda küçük noktalar şeklinde)
        for i in range(len(self.levels)):
            color = level['color'] if i <= self.current_level_idx else (100, 100, 100)
            cv2.circle(img, (60 + i*20, 100), 5, color, -1, cv2.LINE_AA)
        
        # 2. MERKEZİ EMOJİ
        scale = 1.0 + (self.pulse * 0.3)
        target_size = int(120 * scale)
        current_color = level['color'] if self.is_success else tuple(int((c+255)/2) for c in level['color'])
        self.draw_target_emoji(img, level['name'], self.w//2, self.h//2, target_size, current_color)
        
        if self.is_success:
            draw_neon_text(img, "HARIKASIN!", self.w//2 - 100, self.h//2 + 220, cv2.FONT_HERSHEY_DUPLEX, 1.2, level['color'], 3)

        return img
