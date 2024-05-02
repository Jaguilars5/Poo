class Product:

    next = 0


    def __init__(self, id=0, description="Ninguno", price=0, stock=0):

        # Método constructor para inicializar los atributos de la clase Cliente

        Product.next += 1


        self.__id = id  # Asigna el ID único a la
        self.description = description

        self.price = price

        self.__stock = stock


    @property

    def stock(self):

        # Getter para obtener el valor del atributo privado __stock

        return self.__stock


    def __repr__(self):

        # Método especial para representar la clase Cliente como una cadena

        return f'Producto:{self.__id} {self.description} {self.price} {self.stock}'


    def __str__(self):

        # Método especial para representar la clase Cliente como una cadena

        return f'Producto:{self.__id} {self.description} {self.price} {self.stock}'


    def getJson(self):

        # Método especial para representar la clase Cliente como una cadena

        return {"id": self.__id, "description": self.description, "price": self.price, "stock": self.stock}


    def show(self):

        # Método para imprimir los detalles del cliente en la consola


        print(f'{self.__id}  {self.description}           {self.price}  {self.stock}')



if __name__ == '__main__':

    # Se ejecuta solo si este script es el principal

    product1 = Product("Aceite", 2, 1000)

    product2 = Product("Colas", 3, 5000)

    product3 = Product("leche", 1, 300)

    # Muestra la información de la primera empresa

    products = []

    products.append(product1)

    products.append(product2)

    products.append(product3)

    # print(products)

    prods = []

    print('Id Descripción Precio stock')

    for prod in products:

        print(prod.getJson())

        prods.append(prod.getJson())

    print(prods)

