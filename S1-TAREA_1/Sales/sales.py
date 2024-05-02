from Sales.saleDetail import SaleDetail
from Interface.calculationsInterface import CalculationsInterface
from Utilities.utilities import green_color, reset_color, blue_color, purple_color

from datetime import date
import os


class SaleDetail:
    _line = 0

    def __init__(self, product, quantity):
        SaleDetail._line += 1
        self.__id = SaleDetail._line
        self.product = product
        self.price = product.price
        self.quantity = quantity

    @property
    def id(self):
        # Getter para obtener el valor del límite de crédito del cliente VIP
        return self.__id

    def __repr__(self):
        # Método especial para representar la clase Cliente como una cadena
        return f'{self.id} {self.product.description} {self.price} {self.quantity}'


class Sale(CalculationsInterface):
    next = 0
    FACTOR_IVA = 0.12

    def __init__(self, client):
        Sale.next += 1
        self.__invoice = Sale.next
        self.date = date.today()
        self.client = client
        self.subtotal = 0
        self.percentage_discount = client.discount
        self.discount = 0
        self.iva = 0
        self.total = 0
        self.sale_detail = []

    @property
    def invoice(self):
        # Getter para obtener el valor del límite de crédito del cliente VIP
        return self.__invoice

    def __repr__(self):
        # Método especial para representar la clase Cliente como una cadena
        return f'Factura# {self.invoice} {self.date} {self.client.fullName()} {self.total}'

    def cal_iva(self, iva=0.12, valor=0):
        return round(valor * iva, 2)

    def cal_discount(self, valor=0, discount=0):
        return valor * discount

    def add_detail(self, prod, qty):
        detail = SaleDetail(prod, qty)
        self.subtotal += round(detail.price * detail.quantity, 2)
        self.discount = self.cal_discount(self.subtotal, self.percentage_discount)
        self.iva = self.cal_iva(Sale.FACTOR_IVA, self.subtotal - self.discount)
        self.total = round(self.subtotal + self.iva - self.discount, 2)
        self.sale_detail.append(detail)

    def print_invoice(self, company):

        os.system('cls')
        print('\033c', end='')
        print(green_color + "*" * 70 + reset_color)
        print(blue_color + f"Empresa: {company.business_name} Ruc: {company.ruc}", end='')
        print(" Factura#:{:7}Fecha:{}".format(self.invoice, self.date))
        self.client.show()
        print(green_color + "*" * 70 + reset_color)
        print(purple_color + "Linea Articulo Precio Cantidad Subtotal")
        for det in self.sale_detail:
            print(
                blue_color + f"{det.id:5} {det.product.description:6} {det.price:7} {det.quantity:2} {det.price * det.quantity:14}")
        print(green_color + "*" * 70 + reset_color)
        print(purple_color + " " * 23, "Subtotal:  ", str(self.subtotal))
        print(" " * 23, "Descuento: ", str(self.discount))
        print(" " * 23, "Iva:       ", str(self.iva))
        print(" " * 23, "Total:     ", str(self.total) + reset_color)

    def getJson(self):
        # Método especial para representar la clase venta como diccionario
        invoice = {"factura": self.invoice, "Fecha": self.date.strftime("%Y-%m-%d")
            , "cliente": self.client.fullName(), "subtotal": self.subtotal, "descuento": self.discount, "iva": self.iva,
                   "total": self.total, "detalle": []}
        for det in self.sale_detail:
            invoice["detalle"].append(
                {"producto": det.product.description,
                 "price": det.price,
                 "cantidad": det.quantity}
            )
        return invoice


