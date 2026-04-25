"""
emotion_game.py
Duygu Aynası Oyunu - Çocuğun ekrandaki ifadeleri taklit ederek 
seviye atladığı eğitici oyun.
"""

import cv2
import time
import random
from ui_engine import draw_neon_text, draw_glass_panel

class EmotionGame:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        
        # Oyun seviyeleri ve gereken duygu verileri
        self.levels = [
            {'name': 'MUTLU', 'emoji': '😊', 'target': 'smile', 'threshold': 0.6},
            {'name': 'SASKIN', 'emoji': '😮', 'target': 'jaw_open', 'threshold': 0.5},
            {'name': 'GOZ KIRP', 'emoji': '😉', 'target': 'blink_left', 'threshold': 0.7},
            {'name': 'TAMAMEN MUTLU', 'emoji': '😁', 'target': 'smile', 'threshold': 0.85}
        ]
        
        self.current_level_idx = 0
        self.score = 0
        self.level_start_time = time.time()
        self.success_time = 0
        self.is_success = False
        
        # Görsel efektler
        self.msg_color = (0, 255, 255)

    def update(self, face_data):
        """Yüz verilerine göre oyun durumunu günceller."""
        if self.is_success:
            if time.time() - self.success_time > 2.0: # 2 saniye başarı ekranı
                self.next_level()
            return

        level = self.levels[self.current_level_idx]
        target = level['target']
        threshold = level['threshold']
        
        # Kullanıcının performansı hedefi geçiyor mu?
        if face_data.get(target, 0) > threshold:
            self.is_success = True
            self.success_time = time.time()
            self.score += 10
            self.msg_color = (0, 255, 0) # Yeşil (Başarı)

    def next_level(self):
        self.current_level_idx = (self.current_level_idx + 1) % len(self.levels)
        self.is_success = False
        self.level_start_time = time.time()
        self.msg_color = (0, 255, 255)

    def draw(self, img):
        level = self.levels[self.current_level_idx]
        
        # 1. Oyun Paneli (Glassmorphism)
        draw_glass_panel(img, self.w//2 - 250, 50, 500, 200, 20, alpha=0.3)
        
        # 2. Görev Metni
        if not self.is_success:
            task_text = f"SIMDI: {level['name']} OL!"
            draw_neon_text(img, task_text, self.w//2 - 150, 120, cv2.FONT_HERSHEY_DUPLEX, 1.0, self.msg_color, 2)
            cv2.putText(img, "Hadi yapabilirsin!", (self.w//2 - 100, 160), cv2.FONT_HERSHEY_DUPLEX, 0.6, (200, 200, 200), 1)
        else:
            draw_neon_text(img, "HARIKASIN! :)", self.w//2 - 120, 140, cv2.FONT_HERSHEY_DUPLEX, 1.2, (0, 255, 0), 3)
            
        # 3. Skor
        cv2.putText(img, f"PUAN: {self.score}", (50, 50), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)
        
        # 4. Geri Dön Butonu Kılavuzu
        cv2.rectangle(img, (self.w - 180, 20), (self.w - 20, 70), (50, 50, 200), -1)
        cv2.putText(img, "MENU [M]", (self.w - 165, 55), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 2)

        return img
