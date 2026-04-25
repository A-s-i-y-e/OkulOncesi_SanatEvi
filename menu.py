import cv2
import numpy as np
import time
from ui_engine import draw_glass_panel, draw_neon_text, draw_glowing_rect, ParticleSystem

class MainMenu:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        self.particles = ParticleSystem(width, height, 80)
        
        self.btn_w, self.btn_h = 320, 120
        self.gap_x, self.gap_y = 60, 25
        self.total_w = (self.btn_w * 2) + self.gap_x
        self.total_h = (self.btn_h * 3) + (self.gap_y * 2)
        self.start_x = (self.w - self.total_w) // 2
        self.start_y = (self.h - self.total_h) // 2 + 60
        
        self.buttons = {
            'draw': {
                'row': 0, 'col': 0,
                'color': (70, 200, 255),
                'text': 'CIZIM',
                'icon_type': 'pencil',
                'hover_anim': 0.0,
                'progress': 0.0
            },
            'template': {
                'row': 0, 'col': 1,
                'color': (255, 180, 50),
                'text': 'BOYAMA',
                'icon_type': 'bear',
                'hover_anim': 0.0,
                'progress': 0.0
            },
            'game': {
                'row': 1, 'col': 0,
                'color': (255, 120, 100),
                'text': 'BALON',
                'icon_type': 'balloon',
                'hover_anim': 0.0,
                'progress': 0.0
            },
            'pose_game': {
                'row': 1, 'col': 1,
                'color': (100, 255, 100),
                'text': 'ELMA',
                'icon_type': 'apple',
                'hover_anim': 0.0,
                'progress': 0.0
            },
            'emotion_game': {
                'row': 2, 'col': 0,
                'color': (255, 255, 100),
                'text': 'DUYGU AYNASI',
                'icon_type': 'smiley',
                'hover_anim': 0.0,
                'progress': 0.0,
                'is_centered': True
            }
        }
        self.last_time = time.time()

    def _draw_button_icon(self, frame, x, y, size, color, icon_type):
        """Her buton tipi için özel ikon çizer."""
        cx, cy = x + size // 2, y + size // 2
        r = size // 3
        
        if icon_type == 'pencil': # Çizim İkonu
            cv2.line(frame, (cx-r, cy+r), (cx+r, cy-r), color, 4, cv2.LINE_AA)
            cv2.circle(frame, (cx+r, cy-r), 10, color, -1, cv2.LINE_AA)
        elif icon_type == 'bear': # Şablon İkonu
            cv2.circle(frame, (cx, cy), r, color, 3, cv2.LINE_AA)
            cv2.circle(frame, (cx-r, cy-r), r//2, color, 3, cv2.LINE_AA)
            cv2.circle(frame, (cx+r, cy-r), r//2, color, 3, cv2.LINE_AA)
        elif icon_type == 'balloon': # Balon İkonu
            cv2.ellipse(frame, (cx, cy-10), (r, r+10), 0, 0, 360, color, 3, cv2.LINE_AA)
            cv2.line(frame, (cx, cy+r), (cx, cy+r+20), color, 2, cv2.LINE_AA)
        elif icon_type == 'apple': # Elma İkonu
            cv2.circle(frame, (cx-10, cy+5), r, color, -1, cv2.LINE_AA)
            cv2.circle(frame, (cx+10, cy+5), r, color, -1, cv2.LINE_AA)
            cv2.line(frame, (cx, cy-r), (cx+10, cy-r-15), (100, 255, 100), 4, cv2.LINE_AA)
        elif icon_type == 'smiley': # Duygu İkonu
            cv2.circle(frame, (cx, cy), r, color, 3, cv2.LINE_AA)
            cv2.circle(frame, (cx-15, cy-10), 5, color, -1, cv2.LINE_AA)
            cv2.circle(frame, (cx+15, cy-10), 5, color, -1, cv2.LINE_AA)
            cv2.ellipse(frame, (cx, cy+10), (20, 15), 0, 0, 180, color, 3, cv2.LINE_AA)

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
            cbx, cby, cbw, cbh = bx - scale_pixels, by - scale_pixels, bw + scale_pixels * 2, bh + scale_pixels * 2

            draw_glass_panel(frame, cbx, cby, cbw, cbh, r=25, color=info['color'], alpha=0.15 + anim*0.1)

            # --- İKON VE METİN ---
            icon_size = 60
            self._draw_button_icon(frame, cbx + (cbw - icon_size)//2, cby + 10, icon_size, info['color'], info['icon_type'])
            
            text_sz, _ = cv2.getTextSize(info['text'], cv2.FONT_HERSHEY_DUPLEX, 0.7, 2)
            tx, ty = cbx + (cbw - text_sz[0]) // 2, cby + cbh - 15
            
            if anim > 0.4:
                draw_neon_text(frame, info['text'], tx, ty, cv2.FONT_HERSHEY_DUPLEX, 0.7, info['color'], thickness_base=2)
            else:
                cv2.putText(frame, info['text'], (tx, ty), cv2.FONT_HERSHEY_DUPLEX, 0.7, (255, 255, 255), 1, cv2.LINE_AA)

            prog = info['progress']
            if prog > 0:
                bar_ratio = min(1.0, prog / 1.2)
                bar_w = int((cbw - 40) * bar_ratio)
                cv2.rectangle(frame, (cbx + 20, cby + cbh - 10), (cbx + 20 + bar_w, cby + cbh - 5), info['color'], -1)
                
        for p in cursor_poses:
            cx, cy = p
            draw_neon_text(frame, "+", cx-15, cy+15, cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), thickness_base=2)

        return selected_btn
