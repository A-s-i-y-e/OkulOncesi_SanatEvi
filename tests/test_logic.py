import unittest
import numpy as np
import sys
import os

# Proje dizinini ekle
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from hand_detector import HandDetector
from canvas import DrawingCanvas
from ui_engine import ParticleSystem

class TestMinikEllerAtolyesi(unittest.TestCase):
    
    def setUp(self):
        self.w, self.h = 1280, 720
        
    def test_hand_detector_init(self):
        """Yapay zeka modülünün doğru yüklenip yüklenmediğini test eder."""
        detector = HandDetector()
        self.assertIsNotNone(detector)
        print("\n[OK] HandDetector başarıyla başlatıldı.")

    def test_canvas_creation(self):
        """Çizim tuvalinin doğru boyutlarda oluşturulduğunu test eder."""
        canvas = DrawingCanvas(self.w, self.h)
        self.assertEqual(canvas._canvas.shape[:2], (self.h, self.w))
        print("[OK] DrawingCanvas doğru boyutlarda oluşturuldu.")

    def test_particle_system(self):
        """Parçacık motorunun çalıştığını test eder."""
        ps = ParticleSystem(self.w, self.h, num_particles=10)
        self.assertEqual(len(ps.particles), 10)
        
        test_frame = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        ps.update_and_draw(test_frame)
        self.assertFalse(np.all(test_frame == 0)) # Kare artık tamamen siyah olmamalı
        print("[OK] ParticleSystem görsel üretim testi başarılı.")

if __name__ == '__main__':
    unittest.main()
