from Utilities.utilities import borrarPantalla, gotoxy
import time
from Utilities.utilities import borrarPantalla, green_color, reset_color, blue_color, purple_color, red_color


class Menu:
    def __init__(self, titulo="", opciones=[], col=6, fil=1):
        self.titulo = titulo
        self.opciones = opciones
        self.col = col
        self.fil = fil

    def menu(self):
        gotoxy(self.col, self.fil);
        print(self.titulo)
        self.col += 2
        for opcion in self.opciones:
            self.fil += 1
            gotoxy(self.col, self.fil);
            print(opcion)
        gotoxy(self.col, self.fil + 2)
        opc = input(f"Elija opcion[1...{len(self.opciones)}]: ")
        return opc


class Valida:
    def solo_numeros(self, mensajeError, col, fil):
        while True:
            gotoxy(col, fil)
            valor = input()
            try:
                if int(valor) > 0:
                    break
            except:
                gotoxy(col, fil);
                print(mensajeError)
                time.sleep(1)
                gotoxy(col, fil);
                print(" " * 20)
        return valor

    def solo_letras(self, mensaje, mensajeError,col,fill):
        while True:
            gotoxy(col,fill)
            valor = str(input("{} ".format(mensaje)))
            if valor.isalpha():
                break
            else:
                gotoxy(col+1,fill+1)
                print("{} ".format(mensajeError))
        return valor

    def solo_decimales(self,mensaje, mensajeError):
        valor = str(input("{} ".format(mensaje)))
        try:
            valor = float(valor)
            if valor > float(0):
                return valor
            else:
                print("{} ".format(mensajeError))
                return solo_decimales(mensaje, mensajeError)
        except:
            print("{} ".format(mensajeError))
            return solo_decimales(mensaje, mensajeError)

    def cedula(self,mensaje,col,fil):
        while True:
            print(blue_color + f"{mensaje}")
            gotoxy(col,fil)
            cedula = input(purple_color)
            
            if len(cedula) == 10 and cedula.isdigit():
                coeficientes = [2, 1, 2, 1, 2, 1, 2, 1, 2]
                suma = 0
                
                for i in range(9):
                    digito = int(cedula[i]) * coeficientes[i]
                    if digito > 9:
                        digito -= 9
                    suma += digito
                
                total = suma % 10
                if total != 0:
                    total = 10 - total
                
                # Verifica si el dígito de control es igual al último dígito del DNI
                if total == int(cedula[9]):
                    return cedula
            
            print(purple_color + "El formato del DNI es incorrecto.")


class otra:
    pass


if __name__ == '__main__':
    # instanciar el menu
    opciones_menu = ["1. Entero", "2. Letra", "3. Decimal"]
    menu = Menu(titulo="-- Mi Menú --", opciones=opciones_menu, col=10, fil=5)
    # llamada al menu
    opcion_elegida = menu.menu()
    print("Opción escogida:", opcion_elegida)
    valida = Valida()
    if (opciones_menu == 1):
        numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
        print("Número validado:", numero_validado)

    numero_validado = valida.solo_numeros("Mensaje de error", 10, 10)
    print("Número validado:", numero_validado)

    letra_validada = valida.solo_letras("Ingrese una letra:", "Mensaje de error")
    print("Letra validada:", letra_validada)

    decimal_validado = valida.solo_decimales("Ingrese un decimal:", "Mensaje de error")
    print("Decimal validado:", decimal_validado)