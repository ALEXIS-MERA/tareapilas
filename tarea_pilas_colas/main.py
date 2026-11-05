from pasajero import Pasajero
from mi_pila import MiPila
from mi_cola import MiCola

pila = MiPila(10)
cola = MiCola(10)


# ------------------------- funciones de apoyo ✅ -------------------------
def leer_entero(mensaje):
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("  Debe ser un número entero.")


def leer_pasajero():
    numero = leer_entero("  N.º de pasajero: ")
    nombre = input("  Nombre: ").strip()
    cedula = input("  Cédula: ").strip()
    edad = leer_entero("  Edad: ")
    fecha = input("  Fecha de vuelo (AAAA-MM-DD): ").strip()
    destino = input("  Destino: ").strip()
    asiento = input("  Asiento: ").strip().upper()
    return Pasajero(numero, nombre, cedula, edad, fecha, destino, asiento)


def datos_prueba():
    """Los 5 pasajeros de prueba en ORDEN DE LLEGADA (Diana llega primero, Elena última)."""
    return [
        Pasajero(1005, "Diana", "0923456789", 22, "2026-11-15", "Quito",  "12A"),
        Pasajero(1002, "Ana",   "0912345678", 28, "2026-11-15", "Lima",   "03C"),
        Pasajero(1009, "Luis",  "0987654321", 35, "2026-11-20", "Bogotá", "18F"),
        Pasajero(1004, "Beto",  "0934567890", 16, "2026-11-20", "Quito",  "07B"),
        Pasajero(1001, "Elena", "0901234567", 41, "2026-11-22", "Lima",   "01A"),
    ]


def mostrar_opciones(titulo, entrar, salir, ver):
    print(f"\n========== {titulo} ==========")
    print(f" 1. {entrar:<12}  2. Listar          3. {salir}")
    print(f" 4. {ver:<12}  5. Buscar          6. Modificar")
    print(" 7. Eliminar por número         8. Copiar")
    print(" 9. Longitud / ¿vacía?")
    print(" A. 🔧 Avanzado (ordenar, binaria, reversar, filtrar, mayúsculas)")
    print(" C. Cargar datos de prueba      0. Volver")


# ---------------------- 🔧 SUBMENÚ AVANZADO (sirve para pila y cola) ----------------------
def menu_avanzado(estructura, nombre):
    """Las dos clases tienen los mismos métodos avanzados, así que un solo submenú sirve."""
    while True:
        print(f"\n------ 🔧 AVANZADO · {nombre} ------")
        print(" 1. Ordenar ascendente        2. Ordenar descendente")
        print(" 3. Búsqueda binaria (cédula) 4. Reversar")
        print(" 5. Solo mayores de edad      6. Nombres en MAYÚSCULAS")
        print(" 0. Volver")
        op = input("Opción: ").strip()
        if op == "1":
            estructura.ordenar_asc()
            print("  ✓ Ordenada ascendente por n.º de pasajero:")
            estructura.listar()
        elif op == "2":
            estructura.ordenar_desc()
            print("  ✓ Ordenada descendente por n.º de pasajero:")
            estructura.listar()
        elif op == "3":
            cedula = input("  Cédula a buscar: ").strip()
            p = estructura.buscar_binaria(cedula)
            if p is None:
                print("  No existe esa cédula")
            else:
                print(f"  Encontrado: {p}")
        elif op == "4":
            estructura.reversar()
            print("  ✓ Reversada:")
            estructura.listar()
        elif op == "5":
            print("  Mayores de edad (la original no cambia):")
            estructura.filtrar_mayores_de_edad().listar()
        elif op == "6":
            print("  Nombres en mayúsculas (la original no cambia):")
            estructura.nombres_en_mayusculas().listar()
        elif op == "0":
            break
        else:
            print("  Opción no válida")


# ---------------------- MENÚ 1 · PILA ----------------------
def menu_pila():
    while True:
        mostrar_opciones("MENÚ 1 · PILA (LIFO)", "Apilar", "Desapilar", "Ver tope")
        op = input("Opción: ").strip().upper()
        if op == "1":
            pasajero = leer_pasajero()                       # 1. LEER
            if pila.apilar(pasajero):                        # 2. LLAMAR
                print("  ✓ Apilado: ahora es el tope")        # 3. MOSTRAR
        elif op == "2":
            pila.listar()
        elif op == "3":
            p = pila.desapilar()                             # 2. LLAMAR
            if p is None:                                    # 3. MOSTRAR
                print("  La pila está vacía")
            else:
                nuevo = pila.ver_tope()
                if nuevo is None:
                    print(f"  Salió: {p.nombre} · la pila quedó vacía")
                else:
                    print(f"  Salió: {p.nombre} · nuevo tope: {nuevo.nombre}")
        elif op == "4":
            p = pila.ver_tope()
            if p is None:
                print("  La pila está vacía")
            else:
                print(f"  Tope: {p.nombre} ({p.numero})")
        elif op == "5":
            numero = leer_entero("  N.º de pasajero a buscar: ")
            pos = pila.buscar(numero, True)
            if pos == -1:
                print("  No existe")
            else:
                print(f"  Encontrado en [{pos}]: {pila.datos[pos].nombre}")
        elif op == "6":
            numero = leer_entero("  N.º de pasajero a modificar: ")
            destino = input("  Nuevo destino: ").strip()
            asiento = input("  Nuevo asiento: ").strip().upper()
            if pila.modificar(numero, destino, asiento):
                print("  ✓ Modificado")
                pila.listar()
            else:
                print("  No existe")
        elif op == "7":
            numero = leer_entero("  N.º de pasajero a eliminar: ")
            p = pila.eliminar_por_numero(numero)
            if p is None:
                print("  No existe")
            else:
                print(f"  ✓ Eliminado: {p.nombre}")
                pila.listar()
        elif op == "8":
            copia = pila.copiar()
            print("  ✓ Copia creada:")
            copia.listar()
        elif op == "9":
            estado = "está vacía" if pila.esta_vacia() else "no está vacía"
            print(f"  Longitud: {pila.longitud()} · {estado}")
        elif op == "A":
            menu_avanzado(pila, "PILA")
        elif op == "C":
            nuevos = 0
            for p in datos_prueba():
                if pila.apilar(p):
                    nuevos = nuevos + 1
            print(f"  ✓ Datos de prueba apilados ({nuevos} nuevos)")
        elif op == "0":
            break
        else:
            print("  Opción no válida")


# ---------------------- MENÚ 2 · COLA ----------------------
def menu_cola():
    while True:
        mostrar_opciones("MENÚ 2 · COLA (FIFO)", "Encolar", "Desencolar", "Ver frente")
        op = input("Opción: ").strip().upper()
        if op == "1":
            pasajero = leer_pasajero()                       # 1. LEER
            if cola.encolar(pasajero):                       # 2. LLAMAR
                print("  ✓ Encolado: está al final")          # 3. MOSTRAR
        elif op == "2":
            cola.listar()
        elif op == "3":
            p = cola.desencolar()
            if p is None:
                print("  La cola está vacía")
            else:
                nuevo = cola.ver_frente()
                if nuevo is None:
                    print(f"  Salió: {p.nombre} · la cola quedó vacía")
                else:
                    print(f"  Salió: {p.nombre} · nuevo frente: {nuevo.nombre}")
        elif op == "4":
            p = cola.ver_frente()
            if p is None:
                print("  La cola está vacía")
            else:
                print(f"  Frente: {p.nombre} ({p.numero})")
        elif op == "5":
            numero = leer_entero("  N.º de pasajero a buscar: ")
            pos = cola.buscar(numero, True)
            if pos == -1:
                print("  No existe")
            else:
                print(f"  Encontrado en [{pos}]: {cola.datos[pos].nombre}")
        elif op == "6":
            numero = leer_entero("  N.º de pasajero a modificar: ")
            destino = input("  Nuevo destino: ").strip()
            asiento = input("  Nuevo asiento: ").strip().upper()
            if cola.modificar(numero, destino, asiento):
                print("  ✓ Modificado")
                cola.listar()
            else:
                print("  No existe")
        elif op == "7":
            numero = leer_entero("  N.º de pasajero a eliminar: ")
            p = cola.eliminar_por_numero(numero)
            if p is None:
                print("  No existe")
            else:
                print(f"  ✓ Eliminado: {p.nombre}")
                cola.listar()
        elif op == "8":
            copia = cola.copiar()
            print("  ✓ Copia creada:")
            copia.listar()
        elif op == "9":
            estado = "está vacía" if cola.esta_vacia() else "no está vacía"
            print(f"  Longitud: {cola.longitud()} · {estado}")
        elif op == "A":
            menu_avanzado(cola, "COLA")
        elif op == "C":
            nuevos = 0
            for p in datos_prueba():
                if cola.encolar(p):
                    nuevos = nuevos + 1
            print(f"  ✓ Datos de prueba encolados ({nuevos} nuevos)")
        elif op == "0":
            break
        else:
            print("  Opción no válida")


# ---------------------- MENÚ PRINCIPAL ✅ ----------------------
def main():
    while True:
        print("\n===== TAREA PILAS Y COLAS · PASAJEROS ✈ =====")
        print("1. Menú 1 · Pila")
        print("2. Menú 2 · Cola")
        print("3. Salir")
        op = input("Opción: ").strip()
        if op == "1":
            menu_pila()
        elif op == "2":
            menu_cola()
        elif op == "3":
            print("¡Hasta pronto!")
            break
        else:
            print("Opción no válida")


if __name__ == "__main__":
    main()
