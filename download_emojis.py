import os
import urllib.request
import urllib.error

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

def download_all():
    assets_dir = os.path.join(os.path.dirname(__file__), "assets", "emojis")
    os.makedirs(assets_dir, exist_ok=True)
    
    print("Emojiler indiriliyor. Lutfen bekleyin...")
    for name, code in EMOJI_MAP.items():
        filepath = os.path.join(assets_dir, f"{code}.png")
        if not os.path.exists(filepath):
            url = f"https://cdnjs.cloudflare.com/ajax/libs/twemoji/14.0.2/72x72/{code}.png"
            try:
                print(f"[{name}] indiriliyor...")
                urllib.request.urlretrieve(url, filepath)
            except Exception as e:
                print(f"[HATA] {name} indirilemedi: {e}")
        else:
            print(f"[{name}] zaten mevcut.")
            
    print("Tum emojiler hazir!")

if __name__ == "__main__":
    download_all()
