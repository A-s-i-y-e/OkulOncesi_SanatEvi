import cv2
import numpy as np
import time
from ui_engine import draw_glass_panel, draw_neon_text, draw_glowing_rect, ParticleSystem

class MainMenu:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.particles = ParticleSystem(width, height, 80)
        
        self.btn_w, self.btn_h = 320, 140
        self.gap_x, self.gap_y = 60, 40
        self.total_w = (self.btn_w * 2) + self.gap_x
        self.total_h = (self.btn_h * 2) + self.gap_y
        self.start_x = (self.w - self.total_w) // 2
        self.start_y = (self.h - self.total_h) // 2 + 50
        
        self.buttons = {
            'draw': {
                'row': 0, 'col': 0,
                'color': (70, 200, 255),
                'text': 'SERBEST CIZIM',
                'hover_anim': 0.0,
                'progress': 0.0
            },
            'template': {
                'row': 0, 'col': 1,
                'color': (255, 180, 50),
                'text': 'SABLON BOYAMA',
                'hover_anim': 0.0,
                'progress': 0.0
            },
            'game': {
                'row': 1, 'col': 0,
                'color': (255, 120, 100),
                'text': 'BALON PATLAT',
                'hover_anim': 0.0,
                'progress': 0.0
            },
            'pose_game': {
                'row': 1, 'col': 1,
                'color': (100, 255, 100),
                'text': 'ELMA YAKALA',
                'hover_anim': 0.0,
                'progress': 0.0
            }
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

        draw_neon_text(frame, "OKUL ONCESI SANAT EVI", self.w // 2 - 380, 100, cv2.FONT_HERSHEY_DUPLEX, 1.8, (255, 100, 200), thickness_base=3)
        draw_neon_text(frame, "Holografik Arayuz Devrede...", self.w // 2 - 180, 150, cv2.FONT_HERSHEY_DUPLEX, 0.8, (100, 255, 255), thickness_base=1)

        selected_btn = None
        
        for key, info in self.buttons.items():
            bx = self.start_x + info['col'] * (self.btn_w + self.gap_x)
            by = self.start_y + info['row'] * (self.btn_h + self.gap_y)
            bw = self.btn_w
            bh = self.btn_h
            
            is_hovered = False
            for p in cursor_poses:
                cx, cy = p
                if bx <= cx <= bx + bw and by <= cy <= by + bh:
                    is_hovered = True
                    break

            if is_hovered:
                info['hover_anim'] = min(1.0, info['hover_anim'] + dt * 8.0)
                info['progress'] += dt
                if info['progress'] > 1.2:
                    selected_btn = key
            else:
                info['hover_anim'] = max(0.0, info['hover_anim'] - dt * 5.0)
                info['progress'] = max(0.0, info['progress'] - dt * 2.0)

            anim = info['hover_anim']
            scale_pixels = int(anim * 15)
            cbx = bx - scale_pixels
            cby = by - scale_pixels
            cbw = bw + scale_pixels * 2
            cbh = bh + scale_pixels * 2

            draw_glass_panel(frame, cbx, cby, cbw, cbh, r=25, color=info['color'], alpha=0.15 + anim*0.1)

            if anim > 0.05:
                draw_glowing_rect(frame, cbx, cby, cbw, cbh, r=25, color=info['color'], thickness=max(1, int(3*anim)), glow_radius=int(10 + anim*15), intensity_mult=anim)

            text_sz, _ = cv2.getTextSize(info['text'], cv2.FONT_HERSHEY_DUPLEX, 0.9, 2)
            tx = cbx + (cbw - text_sz[0]) // 2
            ty = cby + (cbh + text_sz[1]) // 2
            
            if anim > 0.4:
                draw_neon_text(frame, info['text'], tx, ty, cv2.FONT_HERSHEY_DUPLEX, 0.9, info['color'], thickness_base=2)
            else:
                cv2.putText(frame, info['text'], (tx, ty), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)

            prog = info['progress']
            if prog > 0:
                bar_ratio = min(1.0, prog / 1.2)
                bar_w = int((cbw - 40) * bar_ratio)
                cv2.rectangle(frame, (cbx + 20, cby + cbh - 20), (cbx + 20 + bar_w, cby + cbh - 10), info['color'], -1)
                
        for p in cursor_poses:
            cx, cy = p
            draw_neon_text(frame, "+", cx-15, cy+15, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), thickness_base=2)

        return selected_btn
