import cv2
import numpy as np
import time
import os
from ui_engine import draw_glass_panel, draw_neon_text, draw_glowing_rect, ParticleSystem

class MainMenu:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.particles = ParticleSystem(width, height, 80)
        
        self.btn_w, self.btn_h = 280, 220
        self.gap_x, self.gap_y = 60, 30
        self.total_w = (self.btn_w * 2) + self.gap_x
        self.total_h = (self.btn_h * 3) + (self.gap_y * 2)
        self.start_x = (self.w - self.total_w) // 2
        self.start_y = (self.h - self.total_h) // 2 + 60
        
        # İkonları yükle
        self.icons = {}
        icon_files = {
            'draw': 'icon_brush.png',
            'template': 'icon_bear.png',
            'game': 'icon_balloon.png',
            'pose_game': 'icon_apple.png',
            'emotion_game': 'icon_smiley.png'
        }
        
        for key, fname in icon_files.items():
            if os.path.exists(fname):
                img = cv2.imread(fname)
                if img is not None:
                    self.icons[key] = cv2.resize(img, (160, 160)) # Boyutu biraz küçülttük (Güvenli alan)
            else:
                self.icons[key] = None

        self.buttons = {
            'draw': {'row': 0, 'col': 0, 'color': (70, 200, 255), 'hover_anim': 0.0, 'progress': 0.0},
            'template': {'row': 0, 'col': 1, 'color': (255, 180, 50), 'hover_anim': 0.0, 'progress': 0.0},
            'game': {'row': 1, 'col': 0, 'color': (255, 120, 100), 'hover_anim': 0.0, 'progress': 0.0},
            'pose_game': {'row': 1, 'col': 1, 'color': (100, 255, 100), 'hover_anim': 0.0, 'progress': 0.0},
            'emotion_game': {'row': 2, 'col': 0, 'color': (255, 255, 100), 'hover_anim': 0.0, 'progress': 0.0, 'is_centered': True}
        }
        self.last_time = time.time()

    def draw_menu(self, frame, cursor_poses):
        now = time.time()
        dt = now - self.last_time
        if dt > 0.5: dt = 0.05
        self.last_time = now

        blurred_bg = cv2.GaussianBlur(frame, (99, 99), 0)
        black_overlay = np.zeros_like(frame)
        frame[:] = cv2.addWeighted(blurred_bg, 0.4, black_overlay, 0.6, 0)
        self.particles.update_and_draw(frame)

        draw_neon_text(frame, "MINIK ELLER ATOLYESI", self.w // 2 - 380, 100, cv2.FONT_HERSHEY_DUPLEX, 1.8, (255, 100, 200), thickness_base=3)

        selected_btn = None
        
        for key, info in self.buttons.items():
            if info.get('is_centered'):
                bx = (self.w - self.btn_w) // 2
            else:
                bx = self.start_x + info['col'] * (self.btn_w + self.gap_x)
                
            by = self.start_y + info['row'] * (self.btn_h + self.gap_y)
            bw, bh = self.btn_w, self.btn_h
            
            is_hovered = False
            for p in cursor_poses:
                if bx <= p[0] <= bx + bw and by <= p[1] <= by + bh:
                    is_hovered = True; break

            if is_hovered:
                info['hover_anim'] = min(1.0, info['hover_anim'] + dt * 8.0)
                info['progress'] += dt
                if info['progress'] > 1.2: selected_btn = key
            else:
                info['hover_anim'] = max(0.0, info['hover_anim'] - dt * 5.0)
                info['progress'] = max(0.0, info['progress'] - dt * 2.0)

            anim = info['hover_anim']
            cbx, cby, cbw, cbh = bx - int(anim*15), by - int(anim*15), bw + int(anim*30), bh + int(anim*30)

            draw_glass_panel(frame, cbx, cby, cbw, cbh, r=30, color=info['color'], alpha=0.1 + anim*0.1)
            
            # --- GÜVENLİ İKON ÇİZİMİ ---
            icon = self.icons.get(key)
            if icon is not None:
                isize = 160
                ix, iy = cbx + (cbw - isize)//2, cby + (cbh - isize)//2
                
                # Ekran sınırlarını kontrol et
                x1, y1 = max(0, ix), max(0, iy)
                x2, y2 = min(self.w, ix + isize), min(self.h, iy + isize)
                
                if x2 > x1 and y2 > y1:
                    # İkonun ilgili kısmını kes (eğer ekrana tam sığmıyorsa)
                    icon_part = icon[(y1-iy):(y2-iy), (x1-ix):(x2-ix)]
                    roi = frame[y1:y2, x1:x2]
                    # Karıştırma
                    frame[y1:y2, x1:x2] = cv2.max(roi, icon_part)

            # İlerleme Çubuğu
            if info['progress'] > 0:
                bar_ratio = min(1.0, info['progress'] / 1.2)
                cv2.rectangle(frame, (cbx + 20, cby + cbh - 12), (cbx + 20 + int((cbw-40)*bar_ratio), cby + cbh - 5), info['color'], -1)
                
        for p in cursor_poses:
            draw_neon_text(frame, "+", p[0]-15, p[1]+15, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), thickness_base=2)

        return selected_btn
