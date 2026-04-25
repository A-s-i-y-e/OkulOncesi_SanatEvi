import cv2
import numpy as np
from ui_engine import draw_glass_panel, draw_glowing_rect, _draw_rounded_rect, draw_neon_text

class DrawingUI:
    def __init__(self, w, h):
        self.w = w
        self.h = h

        # İkonları yükle
        self.icon_next = cv2.imread('icon_next.png')
        if self.icon_next is not None: self.icon_next = cv2.resize(self.icon_next, (40, 40))
        self.icon_prev = cv2.imread('icon_prev.png')
        if self.icon_prev is not None: self.icon_prev = cv2.resize(self.icon_prev, (40, 40))

        self.colors = [
            (0, 0, 255), (0, 165, 255), (0, 255, 255), (0, 255, 0),
            (255, 0, 0), (255, 0, 255), (0, 0, 0), (255, 255, 255)
        ]
        self.active_color_idx = 0

        self.tools = {
            'draw':  {'color': (50, 200, 50),  'label': ''},
            'erase': {'color': (50, 50, 200),  'label': ''},
            'star':  {'color': (200, 200, 50), 'label': ''},
            'triangle':{'color':(200, 100, 200),'label':''},
            'clear': {'color': (50, 50, 50),   'label': ''},
            'save':  {'color': (200, 100, 50), 'label': ''}
        }
        self.active_tool = 'draw'
        self.brush_size = 12

    def get_active_color(self):
        return self.colors[self.active_color_idx]

    def next_color(self):
        self.active_color_idx = (self.active_color_idx + 1) % len(self.colors)

    def prev_color(self):
        self.active_color_idx = (self.active_color_idx - 1) % len(self.colors)

    def set_tool(self, tool_name):
        if tool_name in self.tools:
            self.active_tool = tool_name

    def increase_brush(self, step=4):
        self.brush_size = min(60, self.brush_size + step)

    def decrease_brush(self, step=4):
        self.brush_size = max(4, self.brush_size - step)

    def _draw_logo(self, frame, x, y):
        """Uygulama logosunu (Rengarenk El) çizer."""
        # Avuç içi
        cv2.circle(frame, (x, y), 15, (255, 255, 255), -1, cv2.LINE_AA)
        # Parmaklar (Rengarenk)
        finger_colors = [(0,0,255), (0,255,255), (0,255,0), (255,0,0), (255,0,255)]
        for i, color in enumerate(finger_colors):
            angle = -160 + i * 40
            rad = np.deg2rad(angle)
            fx = int(x + np.cos(rad) * 25)
            fy = int(y + np.sin(rad) * 25)
            cv2.line(frame, (x, y), (fx, fy), color, 6, cv2.LINE_AA)

    def draw_ui(self, frame):
        # 1. BAŞLIK VE LOGO (Üst Orta)
        self._draw_logo(frame, self.w // 2 - 220, 45)
        draw_neon_text(frame, "MINIK ELLER ATOLYESI", self.w // 2 - 180, 60, cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 100, 255), 2)

        # 2. Renk Paleti (Üst Panel)
        draw_glass_panel(frame, 20, 10, 600, 70, 20, color=(100, 100, 100), alpha=0.3)
        px, py = 40, 20
        gap = 60
        for i, c in enumerate(self.colors):
            cx, cy = px + i * gap + 25, py + 25
            if i == self.active_color_idx:
                draw_glowing_rect(frame, cx-25, cy-25, 50, 50, r=25, color=c, thickness=3, glow_radius=15)
                cv2.circle(frame, (cx, cy), 20, (255, 255, 255), 4, cv2.LINE_AA)
            else:
                cv2.circle(frame, (cx, cy), 20, c, -1, cv2.LINE_AA)

        # --- İLERİ / GERİ OKLARI ---
        if self.icon_prev is not None:
            # Geri Oku (Sol)
            bx, by = 10, 25
            draw_glass_panel(frame, bx, by, 40, 40, 10, color=(255, 100, 255), alpha=0.3)
            frame[by+5:by+45, bx:bx+40] = cv2.max(frame[by+5:by+45, bx:bx+40], self.icon_prev[:, :40])
            
        if self.icon_next is not None:
            # Ileri Oku (Sag)
            bx, by = 630, 25
            draw_glass_panel(frame, bx, by, 40, 40, 10, color=(100, 255, 100), alpha=0.3)
            frame[by+5:by+45, bx:bx+40] = cv2.max(frame[by+5:by+45, bx:bx+40], self.icon_next[:, :40])

        # 3. Sol Araç Çubuğu
        toolbar_h = len(self.tools) * 90 + 100
        draw_glass_panel(frame, 20, 100, 100, toolbar_h, 20, color=(50, 50, 150), alpha=0.2)
        x_base, y_base = 30, 110
        gap_y = 90
        for tool_id, tool_info in self.tools.items():
            bx, by = x_base, y_base
            bw, bh = 80, 70
            is_active = (tool_id == self.active_tool)
            if is_active:
                draw_glowing_rect(frame, bx, by, bw, bh, 15, color=(0, 255, 255), thickness=3, glow_radius=10)
            _draw_rounded_rect(frame, bx, by, bw, bh, 15, tool_info['color'], -1)
            _draw_rounded_rect(frame, bx, by, bw, bh, 15, (255, 255, 255), 2)
            ic_x, ic_y = bx + bw//2, by + bh//2
            if tool_id == 'draw':
                cv2.circle(frame, (ic_x, ic_y), 15, self.get_active_color(), -1, cv2.LINE_AA)
            elif tool_id == 'erase':
                cv2.rectangle(frame, (ic_x-15, ic_y-15), (ic_x+15, ic_y+15), (255, 255, 255), -1)
            elif tool_id == 'star':
                cv2.putText(frame, "*", (ic_x-12, ic_y+20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (255, 255, 0), 3)
            elif tool_id == 'triangle':
                pts = np.array([[ic_x, ic_y-15], [ic_x-15, ic_y+15], [ic_x+15, ic_y+15]], np.int32)
                cv2.fillPoly(frame, [pts], (255, 255, 255), lineType=cv2.LINE_AA)
            elif tool_id == 'clear':
                cv2.rectangle(frame, (ic_x-12, ic_y-5), (ic_x+12, ic_y+15), (255,255,255), 2)
                cv2.line(frame, (ic_x-15, ic_y-5), (ic_x+15, ic_y-5), (255,255,255), 2)
            elif tool_id == 'save':
                cv2.rectangle(frame, (ic_x-15, ic_y-10), (ic_x+15, ic_y+15), (255,255,255), 2)
                cv2.circle(frame, (ic_x, ic_y+5), 6, (255,255,255), 2)
            y_base += gap_y

        # Sihir Modu
        mbx, mby = 30, y_base
        mbw, mbh = 80, 70
        magic_on = getattr(self, 'magic_active', False)
        if magic_on: draw_glowing_rect(frame, mbx, mby, mbw, mbh, 15, color=(255, 100, 255), thickness=3, glow_radius=15)
        _draw_rounded_rect(frame, mbx, mby, mbw, mbh, 15, (40, 40, 40), -1)
        _draw_rounded_rect(frame, mbx, mby, mbw, mbh, 15, (255, 255, 255), 2)
        cv2.putText(frame, "S", (mbx + 25, mby + 50), cv2.FONT_HERSHEY_DUPLEX, 1.2, (255, 50, 255), 2)

    def check_magic_hover(self, pt):
        if pt is None: return False
        x, y = pt
        y_magic = 110 + len(self.tools) * 90
        return 30 <= x <= 110 and y_magic <= y <= y_magic + 70

    def check_color_hover(self, pt):
        if pt is None: return False
        x, y = pt
        if y < 90:
            px, py, gap = 40, 20, 60
            for i in range(len(self.colors)):
                cx, cy = px + i * gap + 25, py + 25
                if np.hypot(x - cx, y - cy) < 25:
                    self.active_color_idx = i
                    return True
        return False

    def check_tool_hover(self, pt):
        if pt is None: return None
        x, y = pt
        if x < 120 and 100 <= y <= 100 + len(self.tools)*90:
            idx = (y - 110) // 90
            tools_keys = list(self.tools.keys())
            if 0 <= idx < len(tools_keys):
                return tools_keys[idx]
        return None
