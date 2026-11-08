"""Main program demonstrating the Varasto class."""

from varasto import Varasto

mehua = Varasto(100.0)
olutta = Varasto(100.0, 20.2)


def op1():
    """Demonstrate basic storage operations."""
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")

    print("Virhetilanteita:\nVarasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)

    print("Varasto(100.0, -50.7)")


def op2():
    """Demonstrate invalid additions and initial balances."""
    huono = Varasto(100.0, -50.7)
    print(huono)

    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}\nmehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")


def op3():
    """Demonstrate removing amounts from storage."""
    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}\nOlutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.ota_varastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")


def main():
    """Run the storage demonstrations."""
    print(f'''
         Luonnin jälkeen:

         Mehuvarasto: {mehua}

         Olutvarasto: {olutta}

         Olut getterit:
         saldo = {olutta.saldo}
         saldo = {olutta.saldo}
         paljonko_mahtuu = {olutta.paljonko_mahtuu()}

         Mehu setterit:
         Lisätään 50.7
         ''')

    op1()
    op2()
    op3()


if __name__ == "__main__":
    main()
