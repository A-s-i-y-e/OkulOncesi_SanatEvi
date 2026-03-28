import cv2
import numpy as np
import random
import time
from ui_engine import draw_glass_panel, draw_neon_text

class PoseAppleGame:
    def __init__(self, width, height):
        self.w = width
        self.h = height
        
        self.apples = []       
        self.score = 0
        self.last_spawn_time = time.time()
        self.spawn_interval = 2.0  
        self.popped_particles = [] 
        
        self.game_start_time = time.time()
        self.max_time = 60  

        self.bg_frame = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        self._generate_background()

        self.basket_w = 200
        self.basket_h = 100
        self.basket_y = self.h - 120

    def _generate_background(self):
        self.bg_frame[:] = (20, 50, 20)
        cv2.circle(self.bg_frame, (int(self.w*0.8), int(self.h*0.3)), 200, (30, 80, 40), -1)   
        cv2.circle(self.bg_frame, (int(self.w*0.2), int(self.h*0.5)), 300, (15, 60, 25), -1)  
        self.bg_frame = cv2.GaussianBlur(self.bg_frame, (251, 251), 0)

    def _spawn_apple(self):
        radius = random.randint(30, 45)
        x = random.randint(radius, self.w - radius)
        y = -radius
        speed = random.uniform(6.0, 12.0)
        color = (50, 50, 220) 
        
        self.apples.append({
            'x': x, 'y': y, 'r': radius,
            'color': color, 'speed': speed
        })

    def _create_particles(self, x, y, color):
        for _ in range(15):
            angle = random.uniform(0, 2 * np.pi)
            speed = random.uniform(5, 12)
            self.popped_particles.append({
                'x': x, 'y': y,
                'vx': np.cos(angle) * speed,
                'vy': np.sin(angle) * speed,
                'r': random.randint(3, 8),
                'color': color,
                'life': 1.0
            })

    def check_hit(self, bx, by, bw, bh):
        hit = False
        for i in range(len(self.apples)-1, -1, -1):
            a = self.apples[i]
            if (bx < a['x'] < bx + bw) and (by < a['y'] + a['r'] < by + bh):
                self.score += 1
                self._create_particles(a['x'], a['y'] + a['r'], (100, 255, 100))
                self.apples.pop(i)
                hit = True

        if hit and self.score > 0 and self.score % 5 == 0:
            self.spawn_interval = max(0.5, self.spawn_interval - 0.15)

    def draw_game(self, frame, nose_pos):
        now = time.time()
        elapsed = now - self.game_start_time
        remaining = max(0, int(self.max_time - elapsed))

        cv2.addWeighted(self.bg_frame, 0.85, frame, 0.15, 0, frame)

        if remaining > 0 and now - self.last_spawn_time > self.spawn_interval:
            self._spawn_apple()
            self.last_spawn_time = now

        bx = self.w // 2 - self.basket_w // 2
        by = self.basket_y
        if nose_pos:
            nx, ny = nose_pos
            bx = nx - self.basket_w // 2
            bx = max(0, min(self.w - self.basket_w, bx))

        self.check_hit(bx, by, self.basket_w, self.basket_h)

        for i in range(len(self.apples)-1, -1, -1):
            a = self.apples[i]
            a['y'] += a['speed'] 
            
            cv2.circle(frame, (int(a['x']), int(a['y'])), a['r'], a['color'], -1, cv2.LINE_AA)
            cv2.circle(frame, (int(a['x']), int(a['y'])), a['r'], (200, 200, 200), 2, cv2.LINE_AA)
            cv2.line(frame, (int(a['x']), int(a['y']-a['r'])), (int(a['x']+10), int(a['y']-a['r']-15)), (0, 100, 0), 4, cv2.LINE_AA)

            if a['y'] - a['r'] > self.h:
                self.apples.pop(i)

        for i in range(len(self.popped_particles)-1, -1, -1):
            p = self.popped_particles[i]
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vy'] += 0.5 
            p['life'] -= 0.05
            if p['life'] <= 0:
                self.popped_particles.pop(i)
                continue
            cv2.circle(frame, (int(p['x']), int(p['y'])), p['r'], p['color'], -1, cv2.LINE_AA)

        draw_glass_panel(frame, int(bx), int(by), self.basket_w, self.basket_h, 20, (100, 100, 255), 0.5)
        text_size, _ = cv2.getTextSize("SEPET", cv2.FONT_HERSHEY_DUPLEX, 1.0, 2)
        txt_x = int(bx + (self.basket_w - text_size[0]) // 2)
        txt_y = int(by + (self.basket_h + text_size[1]) // 2)
        cv2.putText(frame, "SEPET", (txt_x, txt_y), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)

        draw_glass_panel(frame, 20, 20, 280, 70, 20, (50, 200, 100), 0.15)
        draw_glass_panel(frame, self.w - 300, 20, 280, 70, 20, (50, 200, 100), 0.15)

        draw_neon_text(frame, f"SKOR: {self.score}", 40, 68, cv2.FONT_HERSHEY_DUPLEX, 1.3, (0, 255, 0), 3)
        draw_neon_text(frame, f"SURE: {remaining}s", self.w - 280, 68, cv2.FONT_HERSHEY_DUPLEX, 1.3, (0, 255, 255), 3)

        if remaining == 0:
            over_txt = f"SURE BITTI! Skor: {self.score}"
            tz, _ = cv2.getTextSize(over_txt, cv2.FONT_HERSHEY_DUPLEX, 1.3, 3)
            tx = (self.w - tz[0]) // 2
            ty = self.h // 2
            bw, bh = max(600, tz[0] + 100), 200
            bx_o, by_o = (self.w - bw) // 2, ty - 80
            draw_glass_panel(frame, int(bx_o), int(by_o), int(bw), int(bh), 40, (10, 50, 20), 0.4)
            draw_neon_text(frame, over_txt, tx, ty - 10, cv2.FONT_HERSHEY_DUPLEX, 1.3, (0, 255, 0), 3)
            
            sub_txt = "Menu icin [M]"
            sz, _ = cv2.getTextSize(sub_txt, cv2.FONT_HERSHEY_DUPLEX, 0.9, 2)
            cv2.putText(frame, sub_txt, ((self.w - sz[0]) // 2, ty + 60), 
                        cv2.FONT_HERSHEY_DUPLEX, 0.9, (200, 200, 200), 2, cv2.LINE_AA)

        return frame
