import sqlite3
from datetime import datetime

def inicializar_db():
    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT NOT NULL,
            categoria TEXT NOT NULL,
            descripcion TEXT,
            monto REAL NOT NULL
        )
    ''')
    conexion.commit()
    conexion.close()

# Nevo gasto
def registrar_gasto():
    fecha = datetime.now().strftime("%Y-%m-%d")
    categoria = input("Categoría del gasto: ")
    descripcion = input("Descripción (opcional): ")
    monto = float(input("Monto del gasto: "))

    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO gastos (fecha, categoria, descripcion, monto)
        VALUES (?, ?, ?, ?)
    ''', (fecha, categoria, descripcion, monto))
    conexion.commit()
    conexion.close()

    print("Gasto registrado correctamente.")


# Generar reporte de gastos
def generar_reporte():
    print("\n--- Reporte de Gastos ---")
    print("1. Ver todos los gastos")
    print("2. Ver por fecha específica (YYYY-MM-DD)")
    opcion = input("Selecciona una opción: ")

    conexion = sqlite3.connect("gastos.db")
    cursor = conexion.cursor()

    if opcion == "1":
        cursor.execute("SELECT * FROM gastos ORDER BY fecha DESC")
    elif opcion == "2":
        fecha = input("Introduce la fecha (YYYY-MM-DD): ")
        cursor.execute("SELECT * FROM gastos WHERE fecha = ? ORDER BY id", (fecha,))
    else:
        print("Opción no valida, intente de Nuevo")
        conexion.close()
        return

    registros = cursor.fetchall()
    total = 0

    print("\nID | Fecha | Categoría | Descripción | Monto")
    print("-" * 60)
    for fila in registros:
        print(f"{fila[0]:<3} | {fila[1]} | {fila[2]:<12} | {fila[3]:<20} | ${fila[4]:.2f}")
        total += fila[4]

    print("-" * 60)
    print(f"Gastos Totales: ${total:.2f}")
    conexion.close()

#  Menú principal

def menu():
    inicializar_db()
    while True:
        print("\n===== GESTOR DE GASTOS =====")
        print("1. Registrar gasto")
        print("2. Generar reporte")
        print("3. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            registrar_gasto()
        elif opcion == "2":
            generar_reporte()
        elif opcion == "3":
            print("Salida.")
            break
        else:
            print("Opcion no valida, intente de Nuevo")


# main
if __name__ == "__main__":
    menu()