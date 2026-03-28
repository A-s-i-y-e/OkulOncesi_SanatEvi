"""
game.py
Eğitici oyun modu: Balon Patlatma
"""

import cv2
import numpy as np
import random
import time
import math
from ui_engine import draw_glass_panel, draw_neon_text, draw_glowing_rect

class BalloonGame:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        
        self.balloons = []
        self.score = 0
        self.missed = 0
        self.last_spawn_time = time.time()
        self.spawn_interval = 1.5 
        self.popped_particles = [] 
        
        self.game_start_time = time.time()
        self.max_time = 60 

        self.bg_frame = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        self._generate_background()

    def _generate_background(self):
        self.bg_frame[:] = (20, 15, 30) 
        cv2.circle(self.bg_frame, (150, 100), 200, (60, 20, 80), -1)   
        cv2.circle(self.bg_frame, (350, 250), 300, (20, 50, 100), -1)  
        cv2.circle(self.bg_frame, (self.w - 200, 150), 250, (50, 10, 50), -1) 
        self.bg_frame = cv2.GaussianBlur(self.bg_frame, (251, 251), 0)

    def _spawn_balloon(self):
        radius = random.randint(40, 70)
        x = random.randint(radius, self.w - radius)
        y = self.h + radius
        speed = random.uniform(3.0, 7.0)
        color = (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
        
        self.balloons.append({
            'x': x, 'y': y, 'r': radius,
            'color': color, 'speed': speed
        })

    def _create_particles(self, x, y, color):
        for _ in range(15):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(5, 12)
            self.popped_particles.append({
                'x': x, 'y': y,
                'vx': math.cos(angle) * speed,
                'vy': math.sin(angle) * speed,
                'r': random.randint(3, 8),
                'color': color,
                'life': 1.0 
            })

    def check_hit(self, cursor_poses):
        if not cursor_poses: return
        hit = False
        for cx, cy in cursor_poses:
            for i in range(len(self.balloons)-1, -1, -1):
                b = self.balloons[i]
                dist = math.hypot(b['x'] - cx, b['y'] - cy)
                if dist <= b['r']:
                    self.score += 1
                    self._create_particles(b['x'], b['y'], b['color'])
                    self.balloons.pop(i)
                    hit = True
                    break 

        if hit and self.score > 0 and self.score % 5 == 0:
            self.spawn_interval = max(0.5, self.spawn_interval - 0.1)

    def draw_game(self, frame, cursor_poses):
        now = time.time()
        elapsed = now - self.game_start_time
        remaining = max(0, int(self.max_time - elapsed))

        cv2.addWeighted(self.bg_frame, 0.85, frame, 0.15, 0, frame)

        if now - self.last_spawn_time > self.spawn_interval:
            self._spawn_balloon()
            self.last_spawn_time = now

        for i in range(len(self.balloons)-1, -1, -1):
            b = self.balloons[i]
            b['y'] -= b['speed'] 
            
            cv2.line(frame, (int(b['x']), int(b['y'] + b['r'])), 
                     (int(b['x']), int(b['y'] + b['r'] + 30)), (255, 255, 255), 2)
                     
            cv2.circle(frame, (int(b['x']), int(b['y'])), int(b['r'] * 1.3), b['color'], -1)
            overlay = frame.copy()
            cv2.circle(overlay, (int(b['x']), int(b['y'])), int(b['r'] * 1.3), (0,0,0), -1)
            cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)
            
            cv2.circle(frame, (int(b['x']), int(b['y'])), b['r'], b['color'], -1)
            cv2.circle(frame, (int(b['x']), int(b['y'])), b['r'], (255, 255, 255), 2) 
            
            cv2.ellipse(frame, (int(b['x'] - b['r']*0.3), int(b['y'] - b['r']*0.3)), 
                        (int(b['r']*0.4), int(b['r']*0.15)), -40, 0, 180, (255, 255, 255), 4)

            if b['y'] + b['r'] < 0:
                self.missed += 1
                self.balloons.pop(i)

        for i in range(len(self.popped_particles)-1, -1, -1):
            p = self.popped_particles[i]
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.5 
            p['life'] -= 0.05
            
            if p['life'] <= 0:
                self.popped_particles.pop(i)
                continue
                
            cv2.circle(frame, (int(p['x']), int(p['y'])), p['r'], p['color'], -1)

        self.check_hit(cursor_poses)

        # UI
        draw_glass_panel(frame, 20, 20, 280, 70, 20, (200, 200, 255), 0.15)
        draw_glass_panel(frame, self.w - 300, 20, 280, 70, 20, (200, 200, 255), 0.15)

        draw_neon_text(frame, f"SKOR: {self.score}", 40, 68, cv2.FONT_HERSHEY_DUPLEX, 1.3, (255, 50, 150), 3)
        draw_neon_text(frame, f"SURE: {remaining}s", self.w - 280, 68, cv2.FONT_HERSHEY_DUPLEX, 1.3, (0, 255, 255), 3)

        if cursor_poses:
            for cx, cy in cursor_poses:
                spin_angle = int((now * 90) % 360)
                cv2.ellipse(frame, (cx, cy), (25, 25), spin_angle, 0, 90, (0, 255, 255), 3, cv2.LINE_AA)
                cv2.ellipse(frame, (cx, cy), (25, 25), spin_angle + 180, 0, 90, (0, 255, 255), 3, cv2.LINE_AA)
                cv2.circle(frame, (cx, cy), 8, (255, 100, 255), -1, cv2.LINE_AA)
                cv2.circle(frame, (cx, cy), 3, (255, 255, 255), -1, cv2.LINE_AA)

        if remaining == 0:
            over_txt = f"SURE BITTI! Skor: {self.score}"
            tz, _ = cv2.getTextSize(over_txt, cv2.FONT_HERSHEY_DUPLEX, 1.3, 3)
            tx = (self.w - tz[0]) // 2
            ty = self.h // 2
            
            bw, bh = max(600, tz[0] + 100), 200
            bx, by = (self.w - bw) // 2, ty - 80
            draw_glass_panel(frame, bx, by, bw, bh, 40, (50, 20, 100), 0.4)

            draw_neon_text(frame, over_txt, tx, ty - 10, cv2.FONT_HERSHEY_DUPLEX, 1.3, (0, 255, 255), 3)
            
            sub_txt = "Menu icin [M]"
            sz, _ = cv2.getTextSize(sub_txt, cv2.FONT_HERSHEY_DUPLEX, 0.9, 2)
            cv2.putText(frame, sub_txt, ((self.w - sz[0]) // 2, ty + 60), 
                        cv2.FONT_HERSHEY_DUPLEX, 0.9, (200, 200, 200), 2, cv2.LINE_AA)
            self.spawn_interval = 999 

        return frame
