import cv2
import numpy as np

class DrawingTemplates:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.thick = 6
        self.templates = {}
        self._generate_templates()
        self.template_names = list(self.templates.keys())
        self.active_template = self.template_names[0]

    def _base_img(self):
        img_fg = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        img_fg[:] = 255
        return img_fg

    def _generate_templates(self):
        self.templates['ayi'] = self._create_bear()
        self.templates['orman'] = self._create_forest()
        self.templates['park'] = self._create_park()
        self.templates['kedi'] = self._create_cat()
        self.templates['araba'] = self._create_car()
        self.templates['gemi'] = self._create_boat()
        self.templates['roket'] = self._create_rocket()
        self.templates['cicek'] = self._create_flower()
        self.templates['kelebek'] = self._create_butterfly()
        self.templates['ev'] = self._create_house()

    def _create_bear(self):
        img = self._base_img()
        color = (0, 0, 0)
        cx, cy = self.w // 2, self.h // 2 + 50
        cv2.circle(img, (cx, cy), 150, color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (cx - 100, cy - 120), 50, color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (cx + 100, cy - 120), 50, color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (cx - 50, cy - 30), 20, color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (cx + 50, cy - 30), 20, color, self.thick, cv2.LINE_AA)
        cv2.ellipse(img, (cx, cy + 40), (40, 30), 0, 0, 360, color, self.thick, cv2.LINE_AA)
        return img

    def _create_forest(self):
        img = self._base_img()
        color = (0, 0, 0)
        cv2.line(img, (0, self.h - 150), (self.w, self.h - 150), color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (150, 150), 80, color, self.thick, cv2.LINE_AA)
        for angle in range(0, 360, 45):
            rad = np.deg2rad(angle)
            cv2.line(img, (int(150 + 90 * np.cos(rad)), int(150 + 90 * np.sin(rad))),
                     (int(150 + 130 * np.cos(rad)), int(150 + 130 * np.sin(rad))), color, self.thick, cv2.LINE_AA)
        for tx in [250, 650, 1050]:
            cv2.rectangle(img, (tx, self.h - 150), (tx + 40, self.h - 300), color, self.thick, cv2.LINE_AA)
            cv2.circle(img, (tx + 20, self.h - 350), 100, color, self.thick, cv2.LINE_AA)
        return img

    def _create_park(self):
        img = self._base_img()
        color = (0, 0, 0)
        cv2.line(img, (0, self.h - 100), (self.w, self.h - 100), color, self.thick, cv2.LINE_AA)
        bx, by = 250, self.h - 350
        cv2.rectangle(img, (bx, by), (bx + 250, by + 250), color, self.thick, cv2.LINE_AA)
        pts = np.array([[bx - 30, by], [bx + 125, by - 150], [bx + 280, by]], np.int32)
        cv2.polylines(img, [pts], True, color, self.thick, cv2.LINE_AA)
        cv2.rectangle(img, (bx + 100, by + 120), (bx + 160, by + 250), color, self.thick, cv2.LINE_AA)
        cv2.rectangle(img, (bx + 30, by + 40), (bx + 80, by + 90), color, self.thick, cv2.LINE_AA)
        pts_path = np.array([[bx + 100, by + 250], [bx + 160, by + 250], [bx + 400, self.h], [bx - 50, self.h]], np.int32)
        cv2.polylines(img, [pts_path], True, color, self.thick, cv2.LINE_AA)
        for cx, cy in [(400, 150), (900, 100)]:
            cv2.ellipse(img, (cx, cy), (60, 30), 0, 0, 360, color, self.thick, cv2.LINE_AA)
            cv2.ellipse(img, (cx + 30, cy - 20), (50, 40), 0, 0, 360, color, self.thick, cv2.LINE_AA)
            cv2.ellipse(img, (cx - 30, cy - 10), (40, 30), 0, 0, 360, color, self.thick, cv2.LINE_AA)
        return img

    def _create_cat(self):
        img = self._base_img()
        color = (0, 0, 0)
        cx, cy = self.w // 2, self.h // 2 + 50
        cv2.circle(img, (cx, cy), 140, color, self.thick, cv2.LINE_AA)
        pts1 = np.array([[cx - 120, cy - 50], [cx - 140, cy - 200], [cx - 40, cy - 120]], np.int32)
        cv2.polylines(img, [pts1], True, color, self.thick, cv2.LINE_AA)
        pts2 = np.array([[cx + 120, cy - 50], [cx + 140, cy - 200], [cx + 40, cy - 120]], np.int32)
        cv2.polylines(img, [pts2], True, color, self.thick, cv2.LINE_AA)
        cv2.ellipse(img, (cx - 50, cy - 20), (20, 30), 0, 0, 360, color, self.thick, cv2.LINE_AA)
        cv2.ellipse(img, (cx + 50, cy - 20), (20, 30), 0, 0, 360, color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (cx, cy + 30), 10, color, self.thick, cv2.LINE_AA)
        cv2.line(img, (cx - 180, cy), (cx - 70, cy + 10), color, self.thick, cv2.LINE_AA)
        cv2.line(img, (cx - 180, cy + 30), (cx - 70, cy + 30), color, self.thick, cv2.LINE_AA)
        cv2.line(img, (cx + 180, cy), (cx + 70, cy + 10), color, self.thick, cv2.LINE_AA)
        cv2.line(img, (cx + 180, cy + 30), (cx + 70, cy + 30), color, self.thick, cv2.LINE_AA)
        return img

    def _create_car(self):
        img = self._base_img()
        color = (0, 0, 0)
        bx, by = self.w // 2 - 250, self.h // 2 + 50
        cv2.rectangle(img, (bx, by), (bx + 500, by + 100), color, self.thick, cv2.LINE_AA)
        pts = np.array([[bx + 100, by], [bx + 150, by - 100], [bx + 350, by - 100], [bx + 400, by]], np.int32)
        cv2.polylines(img, [pts], True, color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (bx + 100, by + 100), 50, color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (bx + 400, by + 100), 50, color, self.thick, cv2.LINE_AA)
        cv2.line(img, (bx + 250, by), (bx + 250, by - 100), color, self.thick, cv2.LINE_AA)
        return img

    def _create_boat(self):
        img = self._base_img()
        color = (0, 0, 0)
        bx, by = self.w // 2 - 150, self.h // 2 + 100
        pts = np.array([[bx - 100, by - 80], [bx + 400, by - 80], [bx + 300, by], [bx, by]], np.int32)
        cv2.polylines(img, [pts], True, color, self.thick, cv2.LINE_AA)
        cv2.line(img, (bx + 150, by - 80), (bx + 150, by - 300), color, self.thick, cv2.LINE_AA)
        pts_sail = np.array([[bx + 150, by - 300], [bx + 150, by - 100], [bx + 300, by - 100]], np.int32)
        cv2.polylines(img, [pts_sail], True, color, self.thick, cv2.LINE_AA)
        for x in range(100, 1100, 150):
            cv2.ellipse(img, (x, by + 50), (60, 20), 0, 180, 360, color, self.thick, cv2.LINE_AA)
        return img

    def _create_rocket(self):
        img = self._base_img()
        color = (0, 0, 0)
        cx, cy = self.w // 2, self.h // 2 - 50
        cv2.ellipse(img, (cx, cy), (60, 150), 0, 0, 360, color, self.thick, cv2.LINE_AA)
        pts1 = np.array([[cx - 60, cy + 80], [cx - 120, cy + 180], [cx - 40, cy + 140]], np.int32)
        cv2.polylines(img, [pts1], True, color, self.thick, cv2.LINE_AA)
        pts2 = np.array([[cx + 60, cy + 80], [cx + 120, cy + 180], [cx + 40, cy + 140]], np.int32)
        cv2.polylines(img, [pts2], True, color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (cx, cy - 40), 30, color, self.thick, cv2.LINE_AA)
        pts_flame = np.array([[cx - 30, cy + 145], [cx, cy + 250], [cx + 30, cy + 145]], np.int32)
        cv2.polylines(img, [pts_flame], True, color, self.thick, cv2.LINE_AA)
        for sx, sy in [(200, 150), (1000, 200), (300, 600), (900, 500)]:
            cv2.circle(img, (sx, sy), 10, color, -1)
        return img

    def _create_flower(self):
        img = self._base_img()
        color = (0, 0, 0)
        cx, cy = self.w // 2, self.h // 2 - 50
        for angle in range(0, 360, 45):
            rad = np.deg2rad(angle)
            px = int(cx + 80 * np.cos(rad))
            py = int(cy + 80 * np.sin(rad))
            cv2.circle(img, (px, py), 60, color, self.thick, cv2.LINE_AA)
        cv2.circle(img, (cx, cy), 60, color, self.thick, cv2.LINE_AA)
        cv2.line(img, (cx, cy + 130), (cx, cy + 350), color, self.thick, cv2.LINE_AA)
        cv2.ellipse(img, (cx + 50, cy + 250), (60, 20), 30, 0, 360, color, self.thick, cv2.LINE_AA)
        return img

    def _create_butterfly(self):
        img = self._base_img()
        color = (0, 0, 0)
        cx, cy = self.w // 2, self.h // 2
        cv2.ellipse(img, (cx, cy), (15, 80), 0, 0, 360, color, self.thick, cv2.LINE_AA)
        cv2.ellipse(img, (cx - 100, cy - 50), (100, 80), 30, 0, 360, color, self.thick, cv2.LINE_AA)
        cv2.ellipse(img, (cx + 100, cy - 50), (100, 80), -30, 0, 360, color, self.thick, cv2.LINE_AA)
        cv2.ellipse(img, (cx - 80, cy + 60), (70, 60), -30, 0, 360, color, self.thick, cv2.LINE_AA)
        cv2.ellipse(img, (cx + 80, cy + 60), (70, 60), 30, 0, 360, color, self.thick, cv2.LINE_AA)
        cv2.line(img, (cx - 5, cy - 80), (cx - 30, cy - 130), color, self.thick, cv2.LINE_AA)
        cv2.line(img, (cx + 5, cy - 80), (cx + 30, cy - 130), color, self.thick, cv2.LINE_AA)
        return img

    def _create_house(self):
        img = self._base_img()
        color = (0, 0, 0)
        bx, by = self.w // 2 - 150, self.h // 2
        cv2.rectangle(img, (bx, by), (bx + 300, by + 200), color, self.thick, cv2.LINE_AA) # Body
        pts = np.array([[bx - 20, by], [bx + 150, by - 150], [bx + 320, by]], np.int32)
        cv2.polylines(img, [pts], True, color, self.thick, cv2.LINE_AA) # Roof
        cv2.rectangle(img, (bx + 120, by + 80), (bx + 180, by + 200), color, self.thick, cv2.LINE_AA) # Door
        cv2.rectangle(img, (bx + 30, by + 30), (bx + 90, by + 90), color, self.thick, cv2.LINE_AA) # Window
        cv2.rectangle(img, (bx + 180, by + 30), (bx + 240, by + 90), color, self.thick, cv2.LINE_AA) # Window 2
        return img

    def get_template(self, name):
        return self.templates.get(name)
        
    def get_fill_mask(self, name):
        template = self.get_template(name)
        if template is None:
            return None
        mask = np.zeros((self.h + 2, self.w + 2), dtype=np.uint8)
        gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        lines = gray < 50 
        mask[1:-1, 1:-1][lines] = 1
        return mask

    def draw_template(self, frame, name):
        template = self.get_template(name)
        if template is not None:
            gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            mask = gray < 50
            frame[mask] = (0, 0, 0)
        return frame
