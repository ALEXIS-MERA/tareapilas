from pasajero import Pasajero


class MiPila:
    """Pila (LIFO) hecha a mano sobre un arreglo de tamaño fijo.

    datos -> [fondo, ..., TOPE, None, None]
    TOPE  -> datos[cantidad - 1]  (el último que entró: el único que se ve y el único que sale)

    ⛔ Mismas prohibiciones que MiLista: sin append, pop, insert, remove, index,
       sort, reverse, copy, len(), in, slicing ni comprensiones.
    """

    def __init__(self, capacidad=10):
        self.datos = [None] * capacidad
        self.capacidad = capacidad
        self.cantidad = 0

    # ------------------------------------------------------------------
    # YA RESUELTOS + MEJORA FINAL DE LA FASE 1 (no permitir repetidos)
    # ------------------------------------------------------------------
    def apilar(self, pasajero):
        if self.cantidad == self.capacidad:
            print("  ⚠ La pila está llena")
            return False
        if self.buscar(pasajero.numero) != -1:        # MEJORA: números únicos
            print(f"  ⚠ Ya existe un pasajero con el número {pasajero.numero}")
            return False
        self.datos[self.cantidad] = pasajero          # el nuevo queda encima: es el TOPE
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):
        if self.cantidad == 0:
            print("  (pila vacía)")
            return
        for i in range(self.cantidad - 1, -1, -1):
            if i == self.cantidad - 1:
                print(f"  [{i}] {self.datos[i]}  ← TOPE")
            elif i == 0:
                print(f"  [{i}] {self.datos[i]}  ← FONDO")
            else:
                print(f"  [{i}] {self.datos[i]}")

    # ------------------------------------------------------------------
    # MÉTODOS BÁSICOS (tabla 3) · recorren del tope al fondo
    # ------------------------------------------------------------------
    def desapilar(self):
        """Saca SOLO el tope. No se corre nada. Retorna el pasajero o None."""
        if self.cantidad == 0:
            return None
        pasajero = self.datos[self.cantidad - 1]
        self.datos[self.cantidad - 1] = None
        self.cantidad = self.cantidad - 1
        return pasajero

    def ver_tope(self):
        if self.cantidad == 0:
            return None
        return self.datos[self.cantidad - 1]

    def buscar(self, numero, mostrar=False):
        """Búsqueda lineal del TOPE al FONDO. Retorna la posición o -1.
        Con mostrar=True imprime el recorrido (Elena → Beto → ...)."""
        if mostrar:
            print("  Revisó: ", end="")
        for i in range(self.cantidad - 1, -1, -1):
            if mostrar:
                if i != self.cantidad - 1:
                    print(" → ", end="")
                print(self.datos[i].nombre, end="")
            if self.datos[i].numero == numero:
                if mostrar:
                    print()
                return i
        if mostrar:
            print()
        return -1

    def modificar(self, numero, nuevo_destino, nuevo_asiento):
        """Reutiliza buscar. Nadie cambia de lugar. Retorna True/False."""
        pos = self.buscar(numero)
        if pos == -1:
            return False
        self.datos[pos].destino = nuevo_destino
        self.datos[pos].asiento = nuevo_asiento
        return True

    def eliminar_por_numero(self, numero):
        """No se puede sacar del medio: se desapila hacia una pila auxiliar
        hasta encontrarlo, se descarta y se vuelve a apilar lo de la auxiliar.
        El orden original se mantiene. Retorna el pasajero eliminado o None."""
        aux = MiPila(self.capacidad)
        eliminado = None
        while self.cantidad > 0 and eliminado is None:
            p = self.desapilar()
            if p.numero == numero:
                eliminado = p                          # se descarta
            else:
                aux.apilar(p)
        while aux.cantidad > 0:                        # se devuelven en su orden
            self.apilar(aux.desapilar())
        return eliminado

    def copiar(self):
        """Nueva pila: apila del fondo al tope (0 → cantidad-1) para que el tope sea el mismo."""
        nueva = MiPila(self.capacidad)
        for i in range(self.cantidad):
            nueva.apilar(self.datos[i])
        return nueva

    def longitud(self):
        return self.cantidad

    def esta_vacia(self):
        return self.cantidad == 0

    # ------------------------------------------------------------------
    # 🔧 AVANZADO · solo se toca el tope; todo con pilas auxiliares
    # ------------------------------------------------------------------
    def _vaciar_en(self, destino):
        """Pasa todo el contenido a otra pila (se invierte el orden)."""
        while self.cantidad > 0:
            destino.apilar(self.desapilar())

    def _ordenar(self, ascendente, campo):
        """Ordena EN SITIO con una pila auxiliar (ordenamiento por inserción).
        ascendente=True  -> al listar (tope → fondo) los valores SUBEN: el tope es el menor.
        ascendente=False -> al listar los valores BAJAN: el tope es el mayor."""
        aux = MiPila(self.capacidad)
        while self.cantidad > 0:
            x = self.desapilar()
            if ascendente:
                while aux.cantidad > 0 and getattr(aux.ver_tope(), campo) > getattr(x, campo):
                    self.apilar(aux.desapilar())
            else:
                while aux.cantidad > 0 and getattr(aux.ver_tope(), campo) < getattr(x, campo):
                    self.apilar(aux.desapilar())
            aux.apilar(x)
        aux._vaciar_en(self)                           # al volver se invierte: queda el orden pedido

    def ordenar_asc(self):
        """Ordena por n.º de pasajero: al listar de tope a fondo sale 1001, 1002, 1004..."""
        self._ordenar(True, "numero")

    def ordenar_desc(self):
        """Ordena por n.º de pasajero: al listar de tope a fondo sale 1009, 1005, 1004..."""
        self._ordenar(False, "numero")

    def buscar_binaria(self, cedula):
        """Búsqueda binaria por cédula. Trabaja sobre una COPIA ordenada por cédula,
        así la pila original no se altera. Retorna el Pasajero o None."""
        copia = self.copiar()
        copia._ordenar(False, "cedula")                # tope = mayor -> datos[0..] queda ascendente
        bajo = 0
        alto = copia.cantidad - 1
        while bajo <= alto:
            medio = (bajo + alto) // 2
            actual = copia.datos[medio]
            if actual.cedula == cedula:
                return actual
            if actual.cedula < cedula:
                bajo = medio + 1
            else:
                alto = medio - 1
        return None

    def reversar(self):
        """Invierte la pila EN SITIO con dos pilas auxiliares (3 traspasos)."""
        aux1 = MiPila(self.capacidad)
        aux2 = MiPila(self.capacidad)
        self._vaciar_en(aux1)
        aux1._vaciar_en(aux2)
        aux2._vaciar_en(self)

    def filtrar_mayores_de_edad(self):
        """Nueva pila solo con mayores de edad, en el mismo orden relativo."""
        aux = MiPila(self.capacidad)
        for i in range(self.cantidad - 1, -1, -1):     # tope → fondo
            if self.datos[i].es_mayor_de_edad():
                aux.apilar(self.datos[i])
        nueva = MiPila(self.capacidad)
        aux._vaciar_en(nueva)                          # se invierte otra vez: orden original
        return nueva

    def nombres_en_mayusculas(self):
        """Nueva pila con COPIAS de los pasajeros con el nombre en MAYÚSCULAS."""
        aux = MiPila(self.capacidad)
        for i in range(self.cantidad - 1, -1, -1):     # tope → fondo
            p = self.datos[i]
            aux.apilar(Pasajero(p.numero, p.nombre.upper(), p.cedula, p.edad,
                                p.fecha_vuelo, p.destino, p.asiento))
        nueva = MiPila(self.capacidad)
        aux._vaciar_en(nueva)
        return nueva
