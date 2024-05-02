from Components.components import Menu
from Crud.crudClients import CrudClients
from Crud.crudProducts import CrudProducts
from Crud.crudSales import CrudSales
from Utilities.utilities import borrarPantalla
import time  


def MenuMain():

    menuOption = ""

    while menuOption != "4":

        borrarPantalla()

        menu_main = Menu(
            "Menu Facturación",["1) Clientes", "2) Productos", "3) Ventas", "4) Salir"],
            10,
            5,
        )

        menuOption = menu_main.menu()

        if menuOption == "1":

            clientOption = ""

            while clientOption != "5":

                borrarPantalla()

                menu_clients = Menu(
                    "Menu Cientes",["1) Ingresar","2) Actualizar","3) Eliminar","4) Consultar","5) Salir"],
                    10,
                    5,
                )

                clientOption = menu_clients.menu()
                client = CrudClients()

                if clientOption == "1":

                    client.create()

                elif clientOption == "2":
                    client.update()


                elif clientOption == "3":
                    client.delete()

                elif clientOption == "4":
                    client.consult()

                print("Regresando al menu Clientes...")

                # time.sleep(2)

        elif menuOption == "2":

            productOption = ""

            while productOption != "5":

                borrarPantalla()

                product = CrudProducts()
                
                menu_products = Menu(
                    "Menu Productos",
                    [
                        "1) Ingresar",
                        "2) Actualizar",
                        "3) Eliminar",
                        "4) Consultar",
                        "5) Salir",
                    ],
                    10,
                    5,
                )

                productOption = menu_products.menu()

                if productOption == "1":
                    product.create()

                elif productOption == "2":
                    product.update()

                elif productOption == "3":
                    product.delete()

                elif productOption == "4":
                    product.consult()

        elif menuOption == "3":

            salesMenu = ""

            while salesMenu != "5":

                borrarPantalla()

                sales = CrudSales()

                menu_sales = Menu(
                    "Menu Ventas",
                    [
                        "1) Registro Venta",
                        "2) Consultar",
                        "3) Modificar",
                        "4) Eliminar",
                        "5) Salir",
                    ],
                    10,
                    5,
                )

                salesMenu = menu_sales.menu()

                if salesMenu == "1":

                    sales.create()

                elif salesMenu == "2":

                    sales.consult()

                    time.sleep(2)

                elif salesMenu == "3":

                    sales.update()

                    time.sleep(2)

                elif salesMenu == "4":

                    sales.delete()

                    time.sleep(2)

        print("Regresando al menu Principal...")

        # time.sleep(2)

    borrarPantalla()

    input("Presione una tecla para salir...")

    borrarPantalla()
