"""
gesture_icons.py
El jest ikonlarını OpenCV ile çizen modül.
Her araç ve rengin yanında küçük görsel ipuçları gösterir.
"""

import cv2
import numpy as np


# Arka plan renkleri (BGR)
ICON_BG_COLOR = (40, 40, 40)
ICON_HAND_COLOR = (220, 220, 220)
ICON_ACTIVE_COLOR = (0, 220, 100)


def _draw_rounded_rect(img, x, y, w, h, r, color, thickness=-1):
    """Yuvarlatılmış köşeli dikdörtgen çizer."""
    cv2.rectangle(img, (x + r, y), (x + w - r, y + h), color, thickness)
    cv2.rectangle(img, (x, y + r), (x + w, y + h - r), color, thickness)
    cv2.circle(img, (x + r, y + r), r, color, thickness)
    cv2.circle(img, (x + w - r, y + r), r, color, thickness)
    cv2.circle(img, (x + r, y + h - r), r, color, thickness)
    cv2.circle(img, (x + w - r, y + h - r), r, color, thickness)


import urllib.request
import os

# Emoji haritası (Twemoji unicode karşılıkları)
EMOJI_MAP = {
    'draw': '1f446',     # ☝️
    'erase': '270c',     # ✌️
    'clear': '1f590',    # 🖐️
    'save': '1f44d',     # 👍
    'color': '1f44a',    # 👊
    'triangle': '1f91f', # 🤟 Spiderman
    'star': '1f918'      # 🤘 Rock
}

# Cache for loaded images
_emoji_cache = {}

def _ensure_emoji_downloaded(gesture: str):
    """Google/Twitter Twemoji CDN'den yüksek kaliteli emoji PNG'lerini indirir."""
    if gesture not in EMOJI_MAP:
        return None
    
    emoji_code = EMOJI_MAP[gesture]
    assets_dir = os.path.join(os.path.dirname(__file__), "assets", "emojis")
    os.makedirs(assets_dir, exist_ok=True)
    
    filepath = os.path.join(assets_dir, f"{emoji_code}.png")
    
    if not os.path.exists(filepath):
        # 72x72 px yüksek kalite Twemoji
        url = f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{emoji_code}.png"
        try:
            print(f"[BİLGİ] İkon indiriliyor: {gesture}...")
            urllib.request.urlretrieve(url, filepath)
        except Exception as e:
            print(f"[HATA] İkon indirilemedi: {e}")
            return None
            
    return filepath

def _get_emoji_image(gesture: str, size: int):
    """Emojiyi okur, boyutlandırır ve cache'de tutar."""
    cache_key = f"{gesture}_{size}"
    if cache_key in _emoji_cache:
        return _emoji_cache[cache_key]
        
    filepath = _ensure_emoji_downloaded(gesture)
    if not filepath or not os.path.exists(filepath):
        return None
        
    # BGRA olarak oku (saydamlık kanalı ile), Unicode dizinleri icin np kullan
    import numpy as np
    img = cv2.imdecode(np.fromfile(filepath, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if img is None:
        return None
        
    # İstenen boyuta getir (biraz kenar boşluğu bırakarak)
    target_size = int(size * 0.8)
    img_resized = cv2.resize(img, (target_size, target_size), interpolation=cv2.INTER_AREA)
    
    _emoji_cache[cache_key] = img_resized
    return img_resized

def _overlay_transparent(background, overlay, x, y):
    """Arka plana saydam PNG ekler."""
    bg_h, bg_w, bg_c = background.shape
    h, w, c = overlay.shape
    
    if x >= bg_w or y >= bg_h: return background
    if x + w > bg_w: w = bg_w - x
    if y + h > bg_h: h = bg_h - y
    if w <= 0 or h <= 0: return background
    
    overlay_img = overlay[:h, :w]
    
    # Sadece 4 kanallı resimlerde Alpha blend yap
    if c == 4:
        alpha = overlay_img[:, :, 3] / 255.0
        alpha_inv = 1.0 - alpha
        
        for c_idx in range(3):
            background[y:y+h, x:x+w, c_idx] = (alpha * overlay_img[:, :, c_idx] +
                                              alpha_inv * background[y:y+h, x:x+w, c_idx])
    else:
        background[y:y+h, x:x+w] = overlay_img
        
    return background

def draw_gesture_icon(frame, gesture: str, x: int, y: int, size: int = 50, active: bool = False):
    """
    Verilen konuma (x, y) jest ikonu çizer. Şematik çizim yerine gerçek Twemoji kullanır.
    """
    # Arka plan kutusu
    bg_color = ICON_ACTIVE_COLOR if active else ICON_BG_COLOR
    _draw_rounded_rect(frame, x, y, size, size, 6, bg_color)

    # İkonu al ve yerleştir
    emoji_img = _get_emoji_image(gesture, size)
    if emoji_img is not None:
        eh, ew = emoji_img.shape[:2]
        # Kutunun tam ortasına hizala
        offset_x = x + (size - ew) // 2
        offset_y = y + (size - eh) // 2
        _overlay_transparent(frame, emoji_img, offset_x, offset_y)
    
    # Aktif kenarlık
    if active:
        cv2.rectangle(frame, (x, y), (x + size, y + size),
                      (0, 255, 120), 3, cv2.LINE_AA)


def draw_gesture_label(frame, gesture: str, x: int, y: int, font_scale: float = 0.4):
    """
    Jestin kısa açıklamasını yazar.
    """
    labels = {
        'draw':  '1 Parmak',
        'erase': '2 Parmak',
        'clear': 'Acik El',
        'save':  'Bas Parmak',
        'star':  'Rock Eli',
        'triangle': 'Orumcek Adam',
        'color': 'Yumruk',
        'none':  '',
    }
    text = labels.get(gesture, '')
    if text:
        cv2.putText(frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX,
                    font_scale, (200, 200, 200), 1, cv2.LINE_AA)


def draw_active_gesture_display(frame, gesture: str, x: int, y: int, size: int = 80):
    """
    Ekranın köşesinde büyük 'aktif jest' göstergesi çizer.
    """
    if gesture == 'none' or gesture is None:
        return

    # Yarı saydam arka plan
    overlay = frame.copy()
    cv2.rectangle(overlay, (x - 10, y - 10),
                  (x + size + 10, y + size + 35), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.65, frame, 0.35, 0, frame)

    draw_gesture_icon(frame, gesture, x, y, size, active=True)

    title = {
        'draw': 'CIZIM',
        'erase': 'SILGI',
        'clear': 'TEMIZLE',
        'save': 'KAYDET',
        'star': 'YILDIZ',
        'triangle': 'UCGEN',
        'color': 'RENK',
    }.get(gesture, '')

    cv2.putText(frame, title, (x, y + size + 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 120), 2, cv2.LINE_AA)
