from Client.customer import RegularClient
from Company.company import Company
from Components.components import Menu, gotoxy, Valida
from Interface.crudInterface import CrudInterface
from Json.jsonClass import JsonFile
from Product.product import Product
from Utilities.utilities import (blue_color,borrarPantalla,green_color,purple_color,red_color,reset_color)

import datetime
import json
import os
import time


ruta_script = os.path.abspath(__file__)  # Ruta absoluta del script
ruta_padre = os.path.dirname(os.path.dirname(ruta_script))
class CrudProducts(CrudInterface):
    def create(self):
        validar=Valida()
        borrarPantalla()
        gotoxy(14,1);print(blue_color + Company.get_business_name())
        gotoxy(3,2);print(blue_color+"-"*90 + reset_color)
        gotoxy(20,3);print(blue_color + "Registro de Productos")


        gotoxy(8,5); print('Ingrese el producto: ')
        gotoxy(8,6); print('Ingrese el price del producto:')
        gotoxy(8,7); print('Ingrese el stock del producto:')

        gotoxy(30,5); description = validar.solo_letras("","Descripción Invalida",31,5)
        gotoxy(40,6); price = validar.solo_decimales("","Precio invalido")
        gotoxy(39,8); stock = validar.solo_numeros("Stock invalido",40,7)

        # Obtener el último ID almacenado en el archivo JSON
        json_file = JsonFile(ruta_padre + '/Data/products.json')
        products = json_file.read()
        if products:
            last_id = products[-1]["id"] + 1
        else:
            last_id=1

        # Incrementar el ID para el nuevo producto
        new_product = Product(last_id, description, price, stock)

        # Verificar si ya existe un producto con la misma descripción
        buscar_producto = json_file.find('description',description)

        if buscar_producto:
            gotoxy(10,9); print(f'El producto {description} ya esta registrado.')
            time.sleep(3)
            return
        else:
            products.append(new_product.getJson())
            json_file.save(products)
            gotoxy(10,9);print('El producto se ha registrado con éxito!')
            time.sleep(4)


    def update(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color + "*" * 90 + reset_color)
        gotoxy(20,2)
        print(blue_color + "Actualizar productos")
        gotoxy(10,3)
        print(blue_color + Company.get_business_name())
        gotoxy(10,5)
        id = int(input('Ingrese el ID del producto que va a actualizar: '))
        json_file = JsonFile(ruta_padre + '/Data/products.json')
        products = json_file.read()

        found_product = None
        for product in products:
            if product['id'] == id:
                found_product = product
                break

        if found_product:
            gotoxy(10,6)
            print(f'Su producto es: {found_product}')
            gotoxy(10,7)
            menu_actualizar_producto=Menu("Qué va a actualizar?",["1) Nombre del producto.","2) precio del producto.","3) Stock del producto."],10,8)
            opciones_actualizar_producto=menu_actualizar_producto.menu()
            if opciones_actualizar_producto == "1":
                gotoxy(10,15)
                new_name = input('Ingrese el nuevo nombre del producto: ')
                existing_product = next((prod for prod in products if prod['description'].lower() == new_name.lower() and prod['id'] != id), None)
                if existing_product:
                    gotoxy(10,16)
                    print(f"Este producto ya existe con el ID {existing_product['id']}.")
                else:
                    found_product['description'] = new_name
            elif opciones_actualizar_producto == "2":
                gotoxy(10,15)
                new_price = input('Ingrese el nuevo precio del producto: ')
                found_product['price'] = float(new_price)
            elif opciones_actualizar_producto == "3":
                gotoxy(10,15)
                new_stock = input('Ingrese el nuevo stock del producto: ')
                found_product['stock'] = int(new_stock)

            # Guardar los cambios en el archivo JSON
            json_file.save(products)
            gotoxy(10,16)
            print("Producto actualizado exitosamente!")
        else:
            gotoxy(10,16)
            print("Producto no encontrado.")
        time.sleep(3)

    
    def delete(self):
        borrarPantalla()
        print('\033c', end='')
        print(green_color + "*" * 90 + reset_color)
        gotoxy(20,2)
        print(blue_color + "Eliminar productos")
        gotoxy(10,3)
        print(blue_color + Company.get_business_name())
        gotoxy(10,5)
        id = int(input('Ingrese el ID del producto que va a actualizar: '))
        json_file = JsonFile(ruta_padre + '/Data/products.json')
        products = json_file.read()
        
        found_product = None
        for product in products:
            if product['id'] == id:
                found_product = product
                products.remove(product)

        
        if found_product:
            gotoxy(10,6)
            print(f"Su producto es: {found_product}")
            gotoxy(10,7)
            respuesta = input('Esta seguro de eliminar este producto? (s/n): ').lower()
            if respuesta == 's':
                gotoxy(10,8)
                print('Se elimino su producto')
                for i, product in enumerate(products):
                    product['id'] = i + 1
                
                json_file.save(products)
                gotoxy(10,9)
                print('Se actualizaron los ID de los productos')
                time.sleep(3)
            else:
                gotoxy(10,9)
                print('Cancelando eliminación...')
                time.sleep(3)
        else:
            gotoxy(10,9)
            print('Producto no encontrado')
            time.sleep(3)
                
    
    def consult(self):
        print('\033c', end='')
        gotoxy(2,1);print(green_color+"█"*90)
        gotoxy(2,2);print("██"+" "*34+"Consulta de Productos"+" "*35+"██")
        gotoxy(2,4);id = int(input("Ingrese ID del producto: "))
        json_file = JsonFile(ruta_padre+'/Data/products.json')
        products = json_file.find("id", id)
        
        if products:
            for product in products:
                print("-" * 30)
                print(f'ID: {product["id"]}')
                print(f'Descripcion: {product["description"]}')
                print(f'Precio: {product["price"]}')
                print(f'Stock: {product["stock"]}')
                print("-" * 30)
                
            time.sleep(3)
        else:
            print("Producto no encontrado.")
            time.sleep(3)
        input("Presione una tecla para continuar...")