"""Module for managing a storage."""

class Varasto:
    """Class representing a storage."""

    def __init__(self, tilavuus, alku_saldo=0):
        """Initialize the storage with a capacity and initial balance."""
        self.tilavuus = 0.0
        if tilavuus > 0.0:
            self.tilavuus = tilavuus

        if alku_saldo < 0.0:
            self.saldo = 0.0
        elif alku_saldo <= tilavuus:
            self.saldo = alku_saldo
        else:
            self.saldo = self.tilavuus

    def paljonko_mahtuu(self):
        """Return the remaining capacity."""
        return self.tilavuus - self.saldo

    def lisaa_varastoon(self, maara):
        """Add an amount to the storage."""
        if maara < 0:
            return

        if maara <= self.paljonko_mahtuu():
            self.saldo += maara
        else:
            self.saldo = self.tilavuus

    def ota_varastosta(self, maara):
        """Remove an amount and return how much was removed."""
        if maara < 0:
            return 0.0

        if maara > self.saldo:
            kaikki_mita_voidaan = self.saldo
            self.saldo = 0.0
            return kaikki_mita_voidaan

        self.saldo -= maara
        return maara

    def __str__(self):
        """Return a string representation of the storage."""
        return f"saldo = {self.saldo}, vielä tilaa {self.paljonko_mahtuu()}"
