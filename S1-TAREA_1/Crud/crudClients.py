from Client.customer import RegularClient, VipClient
from Company.company import Company
from Components.components import Menu, gotoxy, Valida
from Interface.crudInterface import CrudInterface
from Json.jsonClass import JsonFile
from Product.product import Product
from Sales.sales import Sale
from Utilities.utilities import (borrarPantalla,green_color,reset_color,blue_color,purple_color,red_color)

import datetime
import json
import os
import time


# Obtiene la ruta del archivo actual

ruta_script = os.path.abspath(__file__)  # Ruta absoluta del script

ruta_padre = os.path.dirname(os.path.dirname(ruta_script))


class CrudClients(CrudInterface):

    def create(self):
        borrarPantalla()
        validar = Valida()
        menu_create_client = Menu("Crear CLiente", ["1)Ciente Regular", "2)Cliente VIP"],10,5)
        menu_create_client_options = menu_create_client.menu()
        json_file = JsonFile(ruta_padre + "/Data/clients.json")

        if menu_create_client_options == "1":
            borrarPantalla()
            gotoxy(20,4)
            print("Crear Cliente")
            gotoxy(10,5)
            dni = validar.cedula("Ingresa el numero cédula para registrar al cliente:",62,5)

            client = json_file.find("dni", dni)

            if client:
                gotoxy(10,6)
                print("Ya existe un cliente con el numero de cedula ingresado")
                time.sleep(3)
                return
            first_name = validar.solo_letras("Ingrese el nombre del cliente:","Solo se admiten letras",10,6)

            last_name = validar.solo_letras("Ingrese el Apellido del cliente:","Solo se admiten letras",10,7)

            menu_card = Menu("Agregar tarjeta", ["1)Si", "2)No"],10,8)

            option_card = menu_card.menu()

            if option_card == "1":
                card = True
            elif option_card == "2":
                card = False
            else:
                print("Opción invalida")
                return

            cli = RegularClient(first_name, last_name, dni, card)
            gotoxy(10,14)
            print(red_color + "¿Está seguro de guardar al cliente? (s/n): ", end="")
            procesar = input().lower()

            if procesar == "s":
                gotoxy(10,15)
                print("😊 Cliente Grabado satisfactoriamente 😊" + reset_color)
                cliente = json_file.read()

                data = cli.getJson()

                cliente.append(data)

                json_file.save(cliente)

            else:
                gotoxy(10,15)
                print("🤣 Creación de cliente cancelada 🤣" + reset_color)
            time.sleep(2)
            
        elif menu_create_client_options == "2":
            borrarPantalla()
            gotoxy(20,4)
            print("Crear Cliente")
            gotoxy(10,5)
            dni = validar.cedula("Ingresa el numero cédula para registrar al cliente:",62,5)

            client = json_file.find("dni", dni)

            if client:
                gotoxy(10,6)
                print("Ya existe un cliente con el numero de cedula ingresado")
                time.sleep(3)
                return
            first_name = validar.solo_letras("Ingrese el nombre del cliente:","Solo se admiten letras",10,6)

            last_name = validar.solo_letras("Ingrese el Apellido del cliente:","Solo se admiten letras",10,7)
            
            cli = VipClient(first_name, last_name, dni)

            gotoxy(10,14)
            print(red_color + "¿Está seguro de guardar al cliente? (s/n): ", end="")
            procesar = input().lower()

            if procesar == "s":
                gotoxy(10,15)
                print("😊 Cliente Grabado satisfactoriamente 😊" + reset_color)
                cliente = json_file.read()

                data = cli.getJson()

                cliente.append(data)

                json_file.save(cliente)

            else:
                gotoxy(10,15)
                print("🤣 Creación de cliente cancelada 🤣" + reset_color)
            time.sleep(2)

    def update(self):
        borrarPantalla()
        validar = Valida()
        json_file = JsonFile(ruta_padre + "/Data/clients.json")
        gotoxy(20,4)
        print(red_color+"Actualizar Cliente"+reset_color)
        gotoxy(10,5)
        dni = validar.cedula("Ingresa el numero cédula para buscar al cliente:",58,5)
        client_data_search = json_file.find("dni", dni)
        client_data=json_file.read()
        if not client_data_search:
            gotoxy(10,6) 
            print("El cliente que se quiere modificar no existe")
            time.sleep(3)
            return
        selected_client_index = None

        for index, client in enumerate(client_data):
            if client['dni'] == dni:
                selected_client_index = index
                break

        if selected_client_index is not None:
            selected_client = client_data[selected_client_index]
            gotoxy(10,6)
            print("Dni:", selected_client['dni'])
            gotoxy(10,7)
            print("Nombre:", selected_client['nombre'])
            gotoxy(10,8)
            print("Apellido:", selected_client['apellido'])
            gotoxy(10,9)
            print("Valor:", selected_client['valor'])

        confirm=Menu("Modificar este cliente:",["1)Si","2)No"],10,11)
        confirm_options=confirm.menu()
        if confirm_options == "1":
            borrarPantalla()
            menu_update_clients = Menu("Actualizar Cliente",
                                       ["1)Actualizar cedula", "2)Actualizar Nombre", "3)Actualizar Apellido",
                                        "4)Cambiar a Regular", "5)Cambiar a VIP"],10,4)
            menu_update_clients_options = menu_update_clients.menu()
            
            if menu_update_clients_options == "1":
                borrarPantalla()
                gotoxy(20,4)
                print(red_color+"Actualizar Cedula"+reset_color)
                gotoxy(10,5)   
                new_dni = validar.cedula("Ingresa el numero cédula para actualizar al cliente:",62,5)
                
                client_data1 = json_file.find("dni", new_dni)
                
                if client_data1:
                    gotoxy(10, 6);print("Ya existe un cliente con el numero de cedula ingresado")
                    return
                
                if selected_client['valor'] == 0.1:
                    new_cli = RegularClient(selected_client['nombre'],selected_client['apellido'], new_dni, True)
                elif selected_client['valor']==0:
                    new_cli = RegularClient(selected_client['nombre'],selected_client['apellido'], new_dni, False)
                elif selected_client['valor']>0.1:
                    new_cli = VipClient(selected_client['nombre'],selected_client['apellido'], new_dni)
                
                gotoxy(10,7)   
                print(red_color + "¿Está seguro de actualizar al cliente? (s/n): ", end="")

                procesar = input().lower()

                if procesar == "s":
                    gotoxy(10,8)
                    print("😊 Actualización Grabada satisfactoriamente 😊" + reset_color)
                    data = new_cli.getJson()
                    cliente = json_file.read()
                    cliente[selected_client_index] = data
                    json_file = JsonFile(ruta_padre + '/Data/clients.json')
                    json_file.save(cliente)
                else:
                    gotoxy(10,8)
                    print("🤣 Actualización Cancelada 🤣" + reset_color)
                time.sleep(5)
                
            elif menu_update_clients_options == "2":
                borrarPantalla()
                gotoxy(20,4)
                print(red_color+"Actualizar nombre"+reset_color)
                new_first_name = validar.solo_letras("Ingrese el nuevo nombre  del cliente:","Solo se admiten letras",10,5)
                if selected_client['valor'] == 0.1:
                    new_cli = RegularClient(new_first_name,selected_client['apellido'], selected_client['dni'], True)
                elif selected_client['valor']==0:
                    new_cli = RegularClient(new_first_name,selected_client['apellido'], selected_client['dni'], False)
                elif selected_client['valor']>0.1:
                    new_cli = VipClient(new_first_name,selected_client['apellido'], selected_client['dni'])
                gotoxy(10,7)
                print(red_color + "¿Está seguro de actualizar al cliente? (s/n): ", end="")

                procesar = input().lower()

                if procesar == "s":
                    gotoxy(10,8)
                    print("😊 Actualización Grabada satisfactoriamente 😊" + reset_color)
                    data = new_cli.getJson()
                    cliente = json_file.read()
                    cliente[selected_client_index] = data
                    json_file = JsonFile(ruta_padre + '/Data/clients.json')
                    json_file.save(cliente)
                else:
                    gotoxy(10,8)
                    print("🤣 Actualización Cancelada 🤣" + reset_color)
                time.sleep(10)
            
            elif menu_update_clients_options == "3":
                borrarPantalla()
                gotoxy(20,4)
                print(red_color+"Actualizar Apellido"+reset_color)
                new_last_name = validar.solo_letras("Ingrese el nuevo nombre  del cliente:","Solo se admiten letras",10,5)
                
                if selected_client['valor'] == 0.1:
                    new_cli = RegularClient(selected_client['nombre'],new_last_name, selected_client['dni'], True)
                elif selected_client['valor']==0:
                    new_cli = RegularClient(selected_client['nombre'],new_last_name, selected_client['dni'], False)
                elif selected_client['valor']>0.1:
                    new_cli = VipClient(selected_client['nombre'],new_last_name, selected_client['dni'])
                gotoxy(10,8)
                print(red_color + "¿Está seguro de actualizar al cliente? (s/n): ", end="")

                procesar = input().lower()

                if procesar == "s":
                    gotoxy(10,9)
                    print("😊 Actualización Grabada satisfactoriamente 😊" + reset_color)
                    data = new_cli.getJson()
                    cliente = json_file.read()
                    cliente[selected_client_index] = data
                    json_file = JsonFile(ruta_padre + '/Data/clients.json')
                    json_file.save(cliente)
                else:
                    gotoxy(10,9)
                    print("🤣 Actualización Cancelada 🤣" + reset_color)
                time.sleep(10)

            elif menu_update_clients_options == "4":
                borrarPantalla()
                gotoxy(20,4)
                print(red_color+"Cambiar a Regular"+reset_color)
                if selected_client['valor']<=0.1:
                    gotoxy(10,4)
                    print("La cedula del cliente ingresado no corresponde a un cliente VIP")
                    time.sleep(5)
                    return
                
                menu_card = Menu("Agregar tarjeta", ["1)Si", "2)No"],10,6)

                option_card = menu_card.menu()

                if option_card == "1":
                    card = True
                elif option_card == "2":
                    card = False
                else:
                    gotoxy(10,9)
                    print("Opción invalida")
                    return 
                new_cli = RegularClient(selected_client['nombre'],selected_client['apellido'], selected_client['dni'],card)   
                gotoxy(10,13)
                print(red_color + "¿Está seguro de actualizar al cliente? (s/n): ", end="")

                procesar = input().lower()

                if procesar == "s":
                    gotoxy(10,14)
                    print("😊 Actualización Grabada satisfactoriamente 😊" + reset_color)
                    data = new_cli.getJson()
                    cliente = json_file.read()
                    cliente[selected_client_index] = data
                    json_file = JsonFile(ruta_padre + '/Data/clients.json')
                    json_file.save(cliente)
                else:
                    gotoxy(10,14)
                    print("🤣 Actualización Cancelada 🤣" + reset_color)
                time.sleep(10)
            
            elif menu_update_clients_options == "5":
                borrarPantalla()
                gotoxy(20,4)
                print(red_color+"Cambiar a VIP"+reset_color)
                if selected_client['valor']>0.1:
                    gotoxy(10,4)
                    print("La cedula del cliente ingresado no corresponde a un cliente Regular")
                    time.sleep(5)
                    return
                 
                
                new_cli = VipClient(selected_client['nombre'],selected_client['apellido'], selected_client['dni'])
                
                gotoxy(10,8)
                print(red_color + "¿Está seguro de actualizar al cliente? (s/n): ", end="")

                procesar = input().lower()

                if procesar == "s":
                    gotoxy(10,9)
                    print("😊 Actualización Grabada satisfactoriamente 😊" + reset_color)
                    data = new_cli.getJson()
                    cliente = json_file.read()
                    cliente[selected_client_index] = data
                    json_file = JsonFile(ruta_padre + '/Data/clients.json')
                    json_file.save(cliente)
                else:
                    gotoxy(10,9)
                    print("🤣 Actualización Cancelada 🤣" + reset_color)
                time.sleep(10)
            
        elif confirm_options == "2":
            borrarPantalla()
            print("Regresando...")
            time.sleep(5)
            return
        else:
            print("Opción Invalida")
            return

    def delete(self):
        borrarPantalla()
        validar = Valida()
        gotoxy(10,5)
        dni = validar.cedula("Ingresa el numero cédula para buscar al cliente:",58,5)
        json_file = JsonFile(ruta_padre + "/Data/clients.json")
        client_data=json_file.read()

        found_dni = json_file.find('dni',dni)

        if found_dni:
            gotoxy(10,6)
            print(found_dni)
            gotoxy(10,7)
            option = input('Esta seguro de eliminar a su cliente? (s/n): ').lower()
            if option == "s":
                client_data.remove(found_dni[0]) 
                json_file.save(client_data)
                gotoxy(10,8)
                print("El cliente ha sido eliminado correctamente.")
                time.sleep(3)
            else:
                gotoxy(10,8)
                print("Operación cancelada...")
                time.sleep(3)
                return
        else:
            gotoxy(10,8)
            print("No se encontró ningún cliente con el DNI proporcionado.")
            time.sleep(3)

    def consult(self):
        borrarPantalla()
        validar = Valida()
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Cliente"+" "*35+"██")
        gotoxy(10,5)
        dni = validar.cedula("Ingresa el numero cédula para buscar al cliente:",58,5)
        json_file = JsonFile(ruta_padre + "/Data/clients.json")
        client_data=json_file.read()

        found_dni = json_file.find('dni',dni)
        if client_data:
            for client in client_data:
                gotoxy(10,6)
                print(f'DNI: {client["dni"]}')
                gotoxy(10,7)
                print(f'Nombre: {client["nombre"]}')
                gotoxy(10,8)
                print(f'Apellido: {client["apellido"]}')
                gotoxy(10,9)
                print(f'Descuento: {client["valor"]}')
                gotoxy(10,10)
                print("-" * 30) 
            time.sleep(3)
        else:
            print("Cliente no encontrado.")
            time.sleep(3)
        input("Presione una tecla para continuar...")
        print(reset_color)
        