"""
emotion_game.py
Duygu Aynası Oyunu - 8 Seviyeli, yavaş geçişli ve göstergeli sürüm.
"""

import cv2
import time
import numpy as np
from ui_engine import draw_neon_text, draw_glass_panel

class EmotionGame:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        
        # 8 Farklı Seviye ve Renk
        self.levels = [
            {'name': 'GULUMSE', 'target': 'smile', 'threshold': 0.45, 'color': (100, 255, 255)}, # Sarı
            {'name': 'SASIR', 'target': 'jaw_open', 'threshold': 0.30, 'color': (255, 150, 50)}, # Mavi
            {'name': 'SOL GOZ KIRP', 'target': 'blink_left', 'threshold': 0.6, 'color': (200, 100, 255)}, # Pembe
            {'name': 'YANAK SISIR', 'target': 'jaw_open', 'threshold': 0.1, 'color': (100, 255, 100)}, # Yeşil (Özel: Yanak yerine ağız serbest)
            {'name': 'SAG GOZ KIRP', 'target': 'blink_right', 'threshold': 0.6, 'color': (50, 200, 255)}, # Turuncu
            {'name': 'KOCAMAN GUL', 'target': 'smile', 'threshold': 0.80, 'color': (255, 100, 100)}, # Kırmızı
            {'name': 'AGZINI AC', 'target': 'jaw_open', 'threshold': 0.6, 'color': (100, 100, 255)}, # Mor
            {'name': 'GOZLERI KAPAT', 'target': 'blink_left', 'threshold': 0.8, 'color': (255, 255, 255)}, # Beyaz
        ]
        
        self.current_level_idx = 0
        self.score = 0
        self.is_success = False
        self.success_time = 0
        self.pulse = 0.0

    def update(self, face_data):
        if self.is_success:
            self.pulse = min(1.6, self.pulse + 0.08)
            # GEÇİŞ SÜRESİ: 2.5 saniye yapıldı (Daha yavaş)
            if time.time() - self.success_time > 2.5:
                self.next_level()
            return

        level = self.levels[self.current_level_idx]
        
        # Özel durum: Gözleri Kapat (İki göz birden)
        if level['name'] == 'GOZLERI KAPAT':
            if face_data.get('blink_left', 0) > 0.7 and face_data.get('blink_right', 0) > 0.7:
                self.trigger_success()
        else:
            if face_data.get(level['target'], 0) > level['threshold']:
                self.trigger_success()

    def trigger_success(self):
        self.is_success = True
        self.success_time = time.time()
        self.score += 20
        self.pulse = 1.0

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
            # Şişkin yanak efekti için geniş ağız
            cv2.circle(img, (cx, cy + 50), 40, color, 4, cv2.LINE_AA)

    def draw(self, img, face_data):
        level = self.levels[self.current_level_idx]
        
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (self.w, self.h), (15, 10, 25), -1)
        cv2.addWeighted(overlay, 0.4, img, 0.6, 0, img)
        
        # 1. Puan ve SEVİYE GÖSTERGESİ
        draw_glass_panel(img, 40, 20, 250, 70, 15, color=level['color'], alpha=0.3)
        cv2.putText(img, f"PUAN: {self.score}", (60, 50), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(img, f"SEVIYE: {self.current_level_idx + 1}/{len(self.levels)}", (60, 80), cv2.FONT_HERSHEY_DUPLEX, 0.5, (200, 200, 200), 1)
        
        # 2. MERKEZİ EMOJİ
        scale = 1.0 + (self.pulse * 0.3)
        target_size = int(120 * scale)
        current_color = level['color'] if self.is_success else tuple(int((c+255)/2) for c in level['color'])
        
        self.draw_target_emoji(img, level['name'], self.w//2, self.h//2, target_size, current_color)
        
        # 3. BAŞARI MESAJI (Daha belirgin)
        if self.is_success:
            draw_neon_text(img, "TEBRIKLER! YILDIZ KAZANDIN", self.w//2 - 200, self.h//2 + 220, cv2.FONT_HERSHEY_DUPLEX, 0.9, level['color'], 2)

        # 4. Cıkıs
        cv2.rectangle(img, (self.w - 180, 20), (self.w - 20, 70), (50, 50, 200), -1)
        cv2.putText(img, "CIKIS [M]", (self.w - 165, 55), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 2)

        return img
