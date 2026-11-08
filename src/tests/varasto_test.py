"""Tests for the Varasto class."""

import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    """Tests for storage functionality."""

    def setUp(self):
        """Create a new storage for each test."""
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        """Test that a new storage is empty."""
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        """Test that a new storage has the correct capacity."""
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        """Test that adding increases the balance."""
        self.varasto.lisaa_varastoon(8)
        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        """Test that adding decreases the available capacity."""
        self.varasto.lisaa_varastoon(8)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        """Test that removing returns the correct amount."""
        self.varasto.lisaa_varastoon(8)
        saatu_maara = self.varasto.ota_varastosta(2)
        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        """Test that removing increases the available capacity."""
        self.varasto.lisaa_varastoon(8)
        self.varasto.ota_varastosta(2)
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_negative_varasto(self):
        """Test that negative capacity is set to zero."""
        varasto = Varasto(-10)
        self.assertAlmostEqual(varasto.tilavuus, 0)

    def test_negative_alkusaldo(self):
        """Test that negative initial balance is set to zero."""
        varasto = Varasto(10, -10)
        self.assertAlmostEqual(varasto.saldo, 0)

    def test_big_alkusaldo(self):
        """Test that initial balance cannot exceed capacity."""
        varasto = Varasto(10, 11)
        self.assertAlmostEqual(varasto.saldo, varasto.tilavuus)

    def test_negative_lisays(self):
        """Test that a negative addition does not change the balance."""
        self.varasto.lisaa_varastoon(-5)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_liian_iso_lisays(self):
        """Test that adding too much fills the storage."""
        self.varasto.lisaa_varastoon(20)
        self.assertAlmostEqual(
            self.varasto.saldo, self.varasto.tilavuus
        )

    def test_negative_ottaminen(self):
        """Test that removing a negative amount changes nothing."""
        self.varasto.lisaa_varastoon(6)
        saatu_maara = self.varasto.ota_varastosta(-5)
        self.assertAlmostEqual(saatu_maara, 0)
        self.assertAlmostEqual(self.varasto.saldo, 6)

    def test_liian_iso_ottaminen(self):
        """Test that removing too much empties the storage."""
        self.varasto.lisaa_varastoon(6)
        saatu_maara = self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(saatu_maara, 6)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_merkkijonoesitys(self):
        """Test the string representation of the storage."""
        self.varasto.lisaa_varastoon(3)
        self.assertEqual(
            str(self.varasto), "saldo = 3, vielä tilaa 7"
        )


if __name__ == "__main__":
    unittest.main()
