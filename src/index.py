from varasto import Varasto

mehua = Varasto(100.0)
olutta = Varasto(100.0, 20.2)

def op1():
    mehua.lisaa_varastoon(50.7)
    print(f"Mehuvarasto: {mehua}")
    print("Otetaan 3.14")
    mehua.ota_varastosta(3.14)
    print(f"Mehuvarasto: {mehua}")

    print("Virhetilanteita:")
    print("Varasto(-100.0);")
    huono = Varasto(-100.0)
    print(huono)

    print("Varasto(100.0, -50.7)")

def op2():
    huono = Varasto(100.0, -50.7)
    print(huono)

    print(f"Olutvarasto: {olutta}")
    print("olutta.lisaa_varastoon(1000.0)")
    olutta.lisaa_varastoon(1000.0)
    print(f"Olutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.lisaa_varastoon(-666.0)")
    mehua.lisaa_varastoon(-666.0)
    print(f"Mehuvarasto: {mehua}")

def op3():
    print(f"Olutvarasto: {olutta}")
    print("olutta.ota_varastosta(1000.0)")
    saatiin = olutta.ota_varastosta(1000.0)
    print(f"saatiin {saatiin}")
    print(f"Olutvarasto: {olutta}")

    print(f"Mehuvarasto: {mehua}")
    print("mehua.otaVarastosta(-32.9)")
    saatiin = mehua.ota_varastosta(-32.9)
    print(f"saatiin {saatiin}")
    print(f"Mehuvarasto: {mehua}")

def main():
    print(f'''
          Luonnin jälkeen:\n
          Mehuvarasto: {mehua}\n
          Olutvarasto: {olutta}\n 

          Olut getterit:\n
          saldo = {olutta.saldo}\n
          saldo = {olutta.saldo}\n
          paljonko_mahtuu = {olutta.paljonko_mahtuu()}\n

          Mehu setterit:\n
          Lisätään 50.7\n
          ''')

    op1()
    
    op2()

    op3()


if __name__ == "__main__":
    main()
