import unittest
from vekalet_logic import VekaletUcretiHesaplayici

class TestVekaletUpdate(unittest.TestCase):
    def setUp(self):
        self.calc = VekaletUcretiHesaplayici()

    def test_dilimler_updated(self):
        # Expected new dilimler (Amount, Rate) for 2025
        expected_dilimler = [
            (600000, 0.16),
            (600000, 0.15),
            (1200000, 0.14),
            (1200000, 0.13),
            (1800000, 0.11),
            (2400000, 0.08),
            (3000000, 0.05),
            (3600000, 0.03),
            (4200000, 0.02),
            (float('inf'), 0.01)
        ]

        # Check if length matches
        self.assertEqual(len(self.calc.dilimler), len(expected_dilimler), "Dilim sayısı uyuşmuyor")

        # Check values
        for i, (amount, rate) in enumerate(expected_dilimler):
            self.assertEqual(self.calc.dilimler[i][0], amount, f"Dilim {i} miktar hatalı")
            self.assertEqual(self.calc.dilimler[i][1], rate, f"Dilim {i} oran hatalı")

    def test_asgari_ucretler_updated(self):
        # Sample check for some key updated values for 2025
        # "Asliye Mahkemeleri" -> 45000 (was 30000 in 2024)
        self.assertEqual(self.calc.asgari_ucretler.get("Asliye Mahkemeleri"), 45000, "Asliye Mahkemeleri asgari ücreti güncellenmemiş")
        # "Sulh Hukuk Mahkemeleri" -> 30000 (was 18000 in 2024)
        self.assertEqual(self.calc.asgari_ucretler.get("Sulh Hukuk Mahkemeleri"), 30000, "Sulh Hukuk Mahkemeleri asgari ücreti güncellenmemiş")
        # "Ağır Ceza Mahkemeleri" -> 65000 (was 48000 in 2024)
        self.assertEqual(self.calc.asgari_ucretler.get("Ağır Ceza Mahkemeleri"), 65000, "Ağır Ceza Mahkemeleri asgari ücreti güncellenmemiş")

    def test_calculation(self):
        # Test calculation with a value that falls into the second tier
        # Value: 1,000,000 TL
        # Calculation:
        # First 600,000 * 0.16 = 96,000
        # Remaining 400,000 * 0.15 = 60,000
        # Total = 156,000

        ucret, _ = self.calc.nispi_vekalet_ucreti_hesapla(1000000, "Asliye Mahkemeleri")
        self.assertEqual(ucret, 156000, f"1.000.000 TL için hesaplama hatalı. Beklenen: 156000, Hesaplanan: {ucret}")

if __name__ == '__main__':
    unittest.main()
