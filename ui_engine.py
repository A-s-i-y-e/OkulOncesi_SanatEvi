import cv2
import numpy as np
import random

def _draw_rounded_rect(img, x, y, w, h, r, color, thickness=-1):
    cv2.rectangle(img, (x + r, y), (x + w - r, y + h), color, thickness)
    cv2.rectangle(img, (x, y + r), (x + w, y + h - r), color, thickness)
    cv2.circle(img, (x + r, y + r), r, color, thickness)
    cv2.circle(img, (x + w - r, y + r), r, color, thickness)
    cv2.circle(img, (x + r, y + h - r), r, color, thickness)
    cv2.circle(img, (x + w - r, y + h - r), r, color, thickness)

def draw_glass_panel(img, x, y, w, h, r, color=(255, 255, 255), alpha=0.15, blur_k=(45, 45)):
    if x < 0 or y < 0 or x + w > img.shape[1] or y + h > img.shape[0]: return
    
    # Extract ROI
    roi = img[y:y+h, x:x+w].copy()
    blurred_roi = cv2.GaussianBlur(roi, blur_k, 0)
    img[y:y+h, x:x+w] = blurred_roi
    
    # Create translucent color overlay
    overlay = img.copy()
    _draw_rounded_rect(overlay, x, y, w, h, r, color, -1)
    
    # White glowing sharp edge for frosted glass effect
    _draw_rounded_rect(overlay, x, y, w, h, r, (255, 255, 255), 1)
    
    cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)

def draw_neon_text(img, text, x, y, font, scale, color, thickness_base=2):
    # Outer glow
    cv2.putText(img, text, (x, y), font, scale, color, thickness_base + 8, cv2.LINE_AA)
    # Inner bright glow
    bright_color = (min(255, color[0]+100), min(255, color[1]+100), min(255, color[2]+100))
    cv2.putText(img, text, (x, y), font, scale, bright_color, thickness_base + 3, cv2.LINE_AA)
    # Core pure white
    cv2.putText(img, text, (x, y), font, scale, (255, 255, 255), thickness_base, cv2.LINE_AA)

def draw_glowing_rect(img, x, y, w, h, r, color, thickness=2, glow_radius=10, intensity_mult=1.0):
    overlay = img.copy()
    for i in range(glow_radius, 0, -2):
        alpha = 0.05 * intensity_mult * (glow_radius / max(1, i))
        _draw_rounded_rect(overlay, x - i, y - i, w + i*2, h + i*2, r + int(i/2), color, thickness=i*2)
        cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0, img)
    # Pure white core
    _draw_rounded_rect(img, x, y, w, h, r, (255, 255, 255), thickness)


class ParticleSystem:
    def __init__(self, w, h, num_particles=60):
        self.w = w
        self.h = h
        self.particles = []
        for _ in range(num_particles):
            self.particles.append(self._create_particle())

    def _create_particle(self):
        return {
            'x': random.uniform(0, self.w),
            'y': random.uniform(0, self.h),
            'vx': random.uniform(-0.6, 0.6),
            'vy': random.uniform(-1.0, -0.2), # Float slowly upward
            'r': random.uniform(2, 7),
            'color': random.choice([(255, 200, 150), (150, 255, 255), (200, 150, 255), (100, 255, 150)]),
            'alpha': random.uniform(0.1, 0.5)
        }

    def update_and_draw(self, img):
        overlay = img.copy()
        for p in self.particles:
            p['x'] += p['vx']
            p['y'] += p['vy']
            
            # Wraparound
            if p['y'] < -15:
                p['y'] = self.h + 15
                p['x'] = random.uniform(0, self.w)
            if p['x'] < -15:
                p['x'] = self.w + 15
            elif p['x'] > self.w + 15:
                p['x'] = -15
                
            color = p['color']
            # Draw glowing particle
            cv2.circle(overlay, (int(p['x']), int(p['y'])), int(p['r']*3), color, -1)
            cv2.circle(img, (int(p['x']), int(p['y'])), int(p['r']), (255, 255, 255), -1)
            
        cv2.addWeighted(overlay, 0.25, img, 0.75, 0, img)
