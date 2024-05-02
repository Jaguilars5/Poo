from Client.customer import RegularClient, VipClient
from Company.company import Company
from Components.components import Menu, gotoxy, Valida
from functools import reduce
from Interface.crudInterface import CrudInterface
from Json.jsonClass import JsonFile
from Product.product import Product
from Sales.sales import Sale
from Utilities.utilities import borrarPantalla, green_color, reset_color, blue_color, purple_color, red_color

import datetime
import json
import os
import time

# Obtiene la ruta del archivo actual
ruta_script = os.path.abspath(__file__)  # Ruta absoluta del script
ruta_padre = os.path.dirname(os.path.dirname(ruta_script))


class CrudSales(CrudInterface):

    def create(self):
        validar = Valida()
        borrarPantalla()

        print('\033c', end='')  # Limpia la pantalla

        # Imprime la cabecera de la venta
        gotoxy(1, 1)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(20, 2)
        print(blue_color + "Registro de Venta")
        gotoxy(10, 3)
        print(blue_color + Company.get_business_name())
        gotoxy(10, 4)
        print(f"Factura#: F0999999 {' ' * 3} Fecha: {datetime.datetime.now()}")
        gotoxy(10, 5)
        print("Subtotal:")
        gotoxy(10, 6)
        print("Descuento:")
        gotoxy(10, 7)
        print("Iva     :")
        gotoxy(10, 8)
        print("Total   :")
        gotoxy(10,9)
        print("Cedula   :")
        dni = validar.cedula(" ",20,9) # Solicita el número de cédula del cliente

        json_file = JsonFile(ruta_padre + '/Data/clients.json')

        client = json_file.find("dni", dni)  # Busca al cliente por su número de cédula
        if not client:
            gotoxy(1, 10)
            print("Cliente no existe")
            return
        client = client[0]
        if client['valor'] == 0.1:
            cli = RegularClient(client['nombre'],client['apellido'], client['dni'], True)
        elif client['valor']==0:
            cli = RegularClient(client['nombre'],client['apellido'], client['dni'], False)
        elif client['valor']>0.1:
            cli = VipClient(client['nombre'],client['apellido'], client['dni'])

        sale = Sale(cli)  # Crea una venta asociada al cliente
        borrarPantalla()
        gotoxy(10, 5)
        print(cli.fullName())
        gotoxy(10, 6)
        print(green_color + "*" * 90 + reset_color)
        gotoxy(10, 7)
        print(purple_color + "Linea", "Id_Articulo", "Descripción", "Precio",
              "Cantidad".ljust(10), "Subtotal")
        gotoxy(10, 8)
        print(reset_color + "-" * 90)

        # Detalle de la venta
        follow = "s"
        line = 1

        while follow.lower() == "s":
            gotoxy(10, 9)
            print(f"{line}")
            gotoxy(18, 9)
            id = int(validar.solo_numeros("Error: Solo números", 19, 9))  # Solicita el ID del producto
            json_file = JsonFile(ruta_padre + '/Data/products.json')

            prods = json_file.find("id", id)  # Busca el producto por su ID

            if not prods:
                gotoxy(10, 10)
                print("Producto no existe")
                time.sleep(1)
            else:
                prods = prods[0]
                product = Product(prods["id"], prods["description"], prods["price"],
                                  prods["stock"])  # Crea un producto
                gotoxy(31,9)
                print(product.description)
                gotoxy(41,9)
                print(product.price)
                qyt = int(validar.solo_numeros("Error: Solo números", 50, 9))  # Solicita la cantidad de producto
                subtotal = product.price * qyt
                gotoxy(60,9)
                print(str(qyt), subtotal)
                sale.add_detail(product, qyt)  # Agrega el detalle de la venta
                follow = input("¿Desea agregar otro producto? (s/n): ").lower()
                if follow == "s":
                    print(green_color + "✔" + reset_color)
                    line += 1
                else:

                    print(f"Subtotal: {round(sale.subtotal, 2)}")
                    print(f"Descuento: {round(sale.discount, 2)}")
                    print(f"Iva     : {round(sale.iva, 2)}")
                    print(f"Total   : {round(sale.total, 2)}")

        #! TOdo
        print(red_color + "¿Está seguro de grabar la venta? (s/n): ", end='')
        procesar = input().lower()  # Pregunta si se quiere grabar la venta
        if procesar == "s":
            print("😊 Venta Grabada satisfactoriamente 😊" + reset_color)
            json_file = JsonFile(ruta_padre + '/Data/invoices.json')
            invoices = json_file.read()
            if invoices:
                ult_invoices = invoices[-1]["factura"] + 1
            else:
                ult_invoices = 1
            data = sale.getJson()
            data["factura"] = ult_invoices
            invoices.append(data)
            json_file = JsonFile(ruta_padre + '/Data/invoices.json')
            json_file.save(invoices)
        else:
            print("🤣 Venta Cancelada 🤣" + reset_color)
        time.sleep(2)

    def update(self):
        validar = Valida()
        borrarPantalla()
        print('\033c', end='')

        json_file_invoices_data = JsonFile(ruta_padre + '/Data/invoices.json')
        invoices = json_file_invoices_data.read()

        # Mostrar las facturas disponibles
        opciones = [f"{factura['factura']}) Factura: #{factura['factura']}" for factura in invoices]
        menu_factura = Menu("Menu Facturas", opciones,5,5)
        print("Seleccione la factura que desea modificar:")
        selected_invoice_str = menu_factura.menu()

        # Obtener el número de factura seleccionada
        selected_invoice_num = int(selected_invoice_str)

        # Buscar la factura seleccionada
        selected_invoice_index = None

        for index, factura in enumerate(invoices):
            if factura['factura'] == selected_invoice_num:
                selected_invoice_index = index
                break
        borrarPantalla()
        if selected_invoice_index is not None:
            selected_invoice = invoices[selected_invoice_index]
            print("Factura:", selected_invoice['factura'])
            print("Fecha:", selected_invoice['Fecha'])
            print("Cliente:", selected_invoice['cliente'])
            print("Subtotal:", selected_invoice['subtotal'])
            print("Descuento:", selected_invoice['descuento'])
            print("IVA:", selected_invoice['iva'])
            print("Total:", selected_invoice['total'])
            print("Detalles:")
            for detalle in selected_invoice['detalle']:
                print("\tProducto:", detalle['producto'])
                print("\tPrecio:", detalle['price'])
                print("\tCantidad:", detalle['cantidad'])
            print()

            # Permitir al usuario seleccionar qué desea modificar
            menu_update = Menu("¿Qué opción desea modificar?", ["1) Cliente", "2) Detalles"], 10, 15)

            selected_update = menu_update.menu()

            if selected_update == "1":
                borrarPantalla()
                dni = validar.cedula("Ingresa el numero cédula del cliente:",42,1)  # Solicita el número de cédula del cliente

                json_file_client_data = JsonFile(ruta_padre + '/Data/clients.json')

                client = json_file_client_data.find("dni", dni)  # Busca al cliente por su número de cédula

                if not client:
                    gotoxy(1, 10)
                    print("Cliente no existe")
                    return
                client = client[0]
                if client['valor'] == 0.1:
                    cli = RegularClient(client['nombre'],client['apellido'], client['dni'], True)
                elif client['valor']==0:
                    cli = RegularClient(client['nombre'],client['apellido'], client['dni'], False)
                elif client['valor']>0.1:
                    cli = VipClient(client['nombre'],client['apellido'], client['dni'])

                sale = Sale(cli)

                json_file = JsonFile(ruta_padre + '/Data/products.json')

                products = []

                for detalle in selected_invoice['detalle']:
                    prods_by_description = json_file.find('description', detalle['producto'])
                    products.append(prods_by_description[0]['id'])

                for i, product in enumerate(products):
                    print()

                    prods = json_file.find("id", product)  # Busca el producto por su ID

                    if not prods:
                        print("Producto no existe")
                        time.sleep(1)
                    else:
                        prods = prods[0]

                        product = Product(prods["id"], prods["description"], prods["price"],
                                          prods["stock"])  # Crea un producto

                        print(product.description.ljust(30), str(product.price).ljust(10), end=' ')

                        product_quantity = selected_invoice['detalle'][i][
                            'cantidad']  # Solicita la cantidad de producto

                        subtotal = product.price * product_quantity

                        print(str(product_quantity).ljust(10), subtotal)

                        sale.add_detail(product, product_quantity)  # Agrega el detalle de la venta

                        print(f"Subtotal: {round(sale.subtotal, 2)}")

                        print(f"Descuento: {round(sale.discount, 2)}")

                        print(f"Iva     : {round(sale.iva, 2)}")

                        print(f"Total   : {round(sale.total, 2)}")

                print(red_color + "¿Está seguro de actualizar el cliente? (s/n): ", end='')

                procesar = input().lower()  # Pregunta si se quiere grabar la venta
                if procesar == "s":
                    print("😊 Actualización Grabada satisfactoriamente 😊" + reset_color)
                    data = sale.getJson()
                    data["factura"] = selected_invoice['factura']
                    invoices[selected_invoice_index] = data
                    json_file = JsonFile(ruta_padre + '/Data/invoices.json')
                    json_file.save(invoices)
                else:
                    print("🤣 Actualización Cancelada 🤣" + reset_color)
                time.sleep(2)

            elif selected_update == "2":
                borrarPantalla()
                json_file_client_data = JsonFile(ruta_padre + '/Data/clients.json')

                cliente = selected_invoice['cliente']
                primera_palabra = cliente.split()[0]

                client = json_file_client_data.find("nombre",primera_palabra)  # Busca al cliente por su número de cédula

                if not client:
                    gotoxy(1, 10)
                    print("Cliente no existe")
                    return
                client = client[0]
                if client['valor'] == 0.1:
                    cli = RegularClient(client['nombre'],client['apellido'], client['dni'], True)
                elif client['valor']==0:
                    cli = RegularClient(client['nombre'],client['apellido'], client['dni'], False)
                elif client['valor']>0.1:
                    cli = VipClient(client['nombre'],client['apellido'], client['dni'])

                sale = Sale(cli)

                # Detalle de la venta
                borrarPantalla()
                gotoxy(10, 5)
                print(cli.fullName())
                gotoxy(10, 6)
                print(green_color + "*" * 90 + reset_color)
                gotoxy(10, 7)
                print(purple_color + "Linea", "Id_Articulo", "Descripción", "Precio",
                    "Cantidad".ljust(10), "Subtotal")
                gotoxy(10, 8)
                print(reset_color + "-" * 90)

                # Detalle de la venta
                follow = "s"
                line = 1

                while follow.lower() == "s":
                    gotoxy(10, 9)
                    print(f"{line}")
                    gotoxy(18, 9)
                    id = int(validar.solo_numeros("Error: Solo números", 19, 9))  # Solicita el ID del producto
                    json_file = JsonFile(ruta_padre + '/Data/products.json')

                    prods = json_file.find("id", id)  # Busca el producto por su ID

                    if not prods:
                        gotoxy(10, 10)
                        print("Producto no existe")
                        time.sleep(1)
                    else:
                        prods = prods[0]
                        product = Product(prods["id"], prods["description"], prods["price"],
                                        prods["stock"])  # Crea un producto
                        gotoxy(31,9)
                        print(product.description)
                        gotoxy(41,9)
                        print(product.price)
                        qyt = int(validar.solo_numeros("Error: Solo números", 50, 9))  # Solicita la cantidad de producto
                        subtotal = product.price * qyt
                        gotoxy(60,9)
                        print(str(qyt), subtotal)
                        sale.add_detail(product, qyt)  # Agrega el detalle de la venta
                        follow = input("¿Desea agregar otro producto? (s/n): ").lower()
                        if follow == "s":
                            print(green_color + "✔" + reset_color)
                            line += 1
                        else:

                            print(f"Subtotal: {round(sale.subtotal, 2)}")
                            print(f"Descuento: {round(sale.discount, 2)}")
                            print(f"Iva     : {round(sale.iva, 2)}")
                            print(f"Total   : {round(sale.total, 2)}")


                print(red_color + "¿Está seguro de grabar la venta? (s/n): ", end='')
                procesar = input().lower()  # Pregunta si se quiere grabar la venta
                if procesar == "s":
                    print("😊 Actualización Grabada satisfactoriamente 😊" + reset_color)
                    data = sale.getJson()
                    data["factura"] = selected_invoice['factura']
                    invoices[selected_invoice_index] = data
                    json_file = JsonFile(ruta_padre + '/Data/invoices.json')
                    json_file.save(invoices)
                else:
                    print("🤣 Venta Cancelada 🤣" + reset_color)
                time.sleep(2)

            else:
                print("Opción no válida.")

        else:
            print("Factura no encontrada.")

    def delete(self):
        # Cargar datos de facturas desde el archivo JSON
        with open(ruta_padre + '/Data/invoices.json', 'r') as json_file:
            invoices = json.load(json_file)

        # Mostrar las facturas disponibles
        opciones = [f"{factura['factura']}) Factura: #{factura['factura']}" for factura in invoices]
        menu_delete = Menu("Menu Eliminar", opciones, 20, 10)

        print("Seleccione la factura que desea modificar:")
        selected_invoice_str = menu_delete.menu()
        selected_invoice_num = int(selected_invoice_str.split(')')[0])

        # Buscar la factura seleccionada
        selected_invoice_index = None
        for index, factura in enumerate(invoices):
            if factura['factura'] == selected_invoice_num:
                selected_invoice_index = index
                break

        if selected_invoice_index is not None:
            # Mostrar detalles de la factura seleccionada
            selected_invoice = invoices[selected_invoice_index]
            print("Factura:", selected_invoice['factura'])
            print("Fecha:", selected_invoice['Fecha'])
            print("Cliente:", selected_invoice['cliente'])
            print("Subtotal:", selected_invoice['subtotal'])
            print("Descuento:", selected_invoice['descuento'])
            print("IVA:", selected_invoice['iva'])
            print("Total:", selected_invoice['total'])
            print("Detalles:")
            for detalle in selected_invoice['detalle']:
                print("\tProducto:", detalle['producto'])
                print("\tPrecio:", detalle['price'])
                print("\tCantidad:", detalle['cantidad'])
            print()

            print("¿Está seguro de eliminar la venta? (s/n): ", end='')
            procesar = input().lower()  # Pregunta si se quiere grabar la venta
            if procesar == "s":
                # Eliminar la factura seleccionada de la lista
                del invoices[selected_invoice_index]

                # Escribir los datos actualizados de vuelta al archivo JSON
                with open(ruta_padre + '/Data/invoices.json', 'w') as json_file:
                    json.dump(invoices, json_file, indent=2)
                    print("Factura eliminada exitosamente.")
            else:
                print("🤣 Venta Cancelada 🤣")
        else:
            print("Factura no encontrada.")

        time.sleep(2)

    def consult(self):
        print('\033c', end='')
        print(green_color + "█" * 90)
        print("██" + " " * 34 + "Consulta de Venta" + " " * 35 + "██")
        invoice = input("Ingrese Factura: ")
        if invoice.isdigit():
            invoice = int(invoice)
            json_file = JsonFile(ruta_padre + '/Data/invoices.json')
            invoices = json_file.find("factura", invoice)
            print(f"Impresión de la Factura#{invoice}")
            print(invoices)
        else:
            json_file = JsonFile(ruta_padre + '/Data/invoices.json')
            invoices = json_file.read()
            print("Consulta de Facturas")
            for fac in invoices:
                print(f"{fac['factura']}   {fac['Fecha']}   {fac['cliente']}   {fac['total']}")

            suma = reduce(lambda total, invoice: round(total + invoice["total"], 2), invoices, 0)
            totales_map = list(map(lambda invoice: invoice["total"], invoices))
            total_client = list(filter(lambda invoice: invoice["cliente"] == "Dayanna Vera", invoices))

            max_invoice = max(totales_map)
            min_invoice = min(totales_map)
            tot_invoices = sum(totales_map)
            print("filter cliente: ", total_client)
            print(f"map Facturas:{totales_map}")
            print(f"              max Factura:{max_invoice}")
            print(f"              min Factura:{min_invoice}")
            print(f"              sum Factura:{tot_invoices}")
            print(f"              reduce Facturas:{suma}")
        x = input("presione una tecla para continuar...")
