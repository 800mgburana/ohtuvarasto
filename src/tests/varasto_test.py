import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        return None
        # self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_negative_varasto(self):
        varasto = Varasto(-10)
        self.assertAlmostEqual(varasto.tilavuus, 0)

    def test_negative_alkusaldo(self):
        varasto = Varasto(10, -10)
        self.assertAlmostEqual(varasto.saldo, 0)

    def test_big_alkusaldo(self):
        varasto = Varasto(10, 11)
        self.assertAlmostEqual(varasto.saldo, varasto.tilavuus)

    def test_negative_lisays(self):
        saatu_maara = self.varasto.lisaa_varastoon(-5)

        self.assertAlmostEqual(saatu_maara, None)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_liian_iso_lisays(self):
        self.varasto.lisaa_varastoon(20)
        self.assertAlmostEqual(self.varasto.saldo, self.varasto.tilavuus)

    def test_negative_ottaminen(self):
        self.varasto.lisaa_varastoon(6)

        saatu_maara = self.varasto.ota_varastosta(-5)

        self.assertAlmostEqual(saatu_maara, 0)
        self.assertAlmostEqual(self.varasto.saldo, 6)
    
    def test_liian_iso_ottaminen(self):
        self.varasto.lisaa_varastoon(6)
        saatu_maara = self.varasto.ota_varastosta(10)

        self.assertAlmostEqual(saatu_maara, 6)
        self.assertAlmostEqual(self.varasto.saldo, 0)
    
    def test_merkkijonoesitys(self):
        self.varasto.lisaa_varastoon(3)

        self.assertEqual(str(self.varasto), "saldo = 3, vielä tilaa 7")
