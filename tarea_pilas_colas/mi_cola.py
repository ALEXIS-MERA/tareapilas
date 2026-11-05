from pasajero import Pasajero
from mi_pila import MiPila


class MiCola:
    """Cola (FIFO) hecha a mano sobre un arreglo de tamaño fijo.

    datos  -> [FRENTE, ..., FINAL, None, None]
    FRENTE -> datos[0]             (el primero que llegó: el único que sale)
    FINAL  -> datos[cantidad - 1]  (los nuevos se ponen detrás de él)

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
    def encolar(self, pasajero):
        if self.cantidad == self.capacidad:
            print("  ⚠ La cola está llena")
            return False
        if self.buscar(pasajero.numero) != -1:        # MEJORA: números únicos
            print(f"  ⚠ Ya existe un pasajero con el número {pasajero.numero}")
            return False
        self.datos[self.cantidad] = pasajero          # se pone a la fila por detrás
        self.cantidad = self.cantidad + 1
        return True

    def listar(self):
        if self.cantidad == 0:
            print("  (cola vacía)")
            return
        for i in range(self.cantidad):
            if i == 0:
                print(f"  [{i}] {self.datos[i]}  ← FRENTE")
            elif i == self.cantidad - 1:
                print(f"  [{i}] {self.datos[i]}  ← FINAL")
            else:
                print(f"  [{i}] {self.datos[i]}")

    # ------------------------------------------------------------------
    # MÉTODOS BÁSICOS (tabla 3) · recorren del frente al final
    # ------------------------------------------------------------------
    def desencolar(self):
        """Saca SOLO el frente datos[0] y corre todos a la izquierda."""
        if self.cantidad == 0:
            return None
        pasajero = self.datos[0]
        for i in range(self.cantidad - 1):
            self.datos[i] = self.datos[i + 1]
        self.datos[self.cantidad - 1] = None
        self.cantidad = self.cantidad - 1
        return pasajero

    def ver_frente(self):
        if self.cantidad == 0:
            return None
        return self.datos[0]

    def buscar(self, numero, mostrar=False):
        """Búsqueda lineal del FRENTE al FINAL. Retorna la posición o -1.
        Con mostrar=True imprime el recorrido (Diana → Ana → ...)."""
        if mostrar:
            print("  Revisó: ", end="")
        for i in range(self.cantidad):
            if mostrar:
                if i != 0:
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
        """No se puede sacar del medio: se desencola cantidad veces; si no es el
        buscado se vuelve a encolar. La fila da una vuelta completa y conserva el orden.
        Retorna el pasajero eliminado o None."""
        eliminado = None
        total = self.cantidad
        for vuelta in range(total):
            p = self.desencolar()
            if p.numero == numero:
                eliminado = p                          # no se vuelve a encolar
            else:
                self.encolar(p)
        return eliminado

    def copiar(self):
        """Nueva cola; encola del frente al final."""
        nueva = MiCola(self.capacidad)
        for i in range(self.cantidad):
            nueva.encolar(self.datos[i])
        return nueva

    def longitud(self):
        return self.cantidad

    def esta_vacia(self):
        return self.cantidad == 0

    # ------------------------------------------------------------------
    # 🔧 AVANZADO · solo entra por el final y sale por el frente
    # ------------------------------------------------------------------
    def _ordenar(self, ascendente, campo):
        """Ordena EN SITIO por selección usando rotaciones de la fila y una cola auxiliar.
        ascendente=True  -> el frente es el menor.  False -> el frente es el mayor."""
        resultado = MiCola(self.capacidad)
        total = self.cantidad
        for ronda in range(total):
            # 1) una vuelta completa para encontrar el mejor candidato
            mejor = None
            vueltas = self.cantidad
            for i in range(vueltas):
                p = self.desencolar()
                if mejor is None:
                    mejor = p
                elif ascendente and getattr(p, campo) < getattr(mejor, campo):
                    mejor = p
                elif (not ascendente) and getattr(p, campo) > getattr(mejor, campo):
                    mejor = p
                self.encolar(p)
            # 2) otra vuelta: el mejor se pasa a la cola de resultado, los demás regresan
            vueltas = self.cantidad
            for i in range(vueltas):
                p = self.desencolar()
                if p is mejor:
                    resultado.encolar(p)
                else:
                    self.encolar(p)
        while resultado.cantidad > 0:
            self.encolar(resultado.desencolar())

    def ordenar_asc(self):
        """Ordena por n.º de pasajero: el frente es el menor (1001, 1002, 1004...)."""
        self._ordenar(True, "numero")

    def ordenar_desc(self):
        """Ordena por n.º de pasajero: el frente es el mayor (1009, 1005, 1004...)."""
        self._ordenar(False, "numero")

    def buscar_binaria(self, cedula):
        """Búsqueda binaria por cédula. Trabaja sobre una COPIA ordenada por cédula,
        así la cola original no se altera. Retorna el Pasajero o None."""
        copia = self.copiar()
        copia._ordenar(True, "cedula")
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
        """Invierte la cola EN SITIO con una pila auxiliar (LIFO invierte el orden)."""
        aux = MiPila(self.capacidad)
        while self.cantidad > 0:
            aux.apilar(self.desencolar())
        while aux.cantidad > 0:
            self.encolar(aux.desapilar())

    def filtrar_mayores_de_edad(self):
        """Nueva cola solo con mayores de edad, en el mismo orden."""
        nueva = MiCola(self.capacidad)
        for i in range(self.cantidad):
            if self.datos[i].es_mayor_de_edad():
                nueva.encolar(self.datos[i])
        return nueva

    def nombres_en_mayusculas(self):
        """Nueva cola con COPIAS de los pasajeros con el nombre en MAYÚSCULAS."""
        nueva = MiCola(self.capacidad)
        for i in range(self.cantidad):
            p = self.datos[i]
            nueva.encolar(Pasajero(p.numero, p.nombre.upper(), p.cedula, p.edad,
                                   p.fecha_vuelo, p.destino, p.asiento))
        return nueva
