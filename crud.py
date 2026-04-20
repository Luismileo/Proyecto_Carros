import os
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

# 1. Configuración de conexión
load_dotenv()
db_url = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(db_url)

# --- OPERACIONES CRUD (CARROS) ---

def crear_carro():
    print("\n--- Agregar Nuevo Carro ---")
    marca = input("Marca: ")
    modelo = input("Modelo: ")
    anio = int(input("Año: "))
    precio = float(input("Precio: "))
    estado = input("Estado (Exposición/Venta/Compra): ")
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO Carros (marca, modelo, anio, precio, estado) VALUES (%s, %s, %s, %s, %s)",
            (marca, modelo, anio, precio, estado)
        )
        conn.commit()
        print("✅ Carro agregado con éxito.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

def leer_carros():
    print("\n--- Lista de Carros ---")
    conn = get_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("SELECT * FROM Carros ORDER BY id_carro ASC")
    rows = cur.fetchall()
    
    if not rows:
        print("No hay carros registrados.")
    for row in rows:
        print(f"ID: {row['id_carro']} | {row['marca']} {row['modelo']} ({row['anio']}) - ${row['precio']} [{row['estado']}]")
    
    cur.close()
    conn.close()

def actualizar_carro():
    leer_carros()
    id_carro = int(input("\nIngrese el ID del carro a actualizar: "))
    nuevo_precio = float(input("Nuevo precio: "))
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE Carros SET precio = %s WHERE id_carro = %s", (nuevo_precio, id_carro))
        conn.commit()
        print("✅ Precio actualizado.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

def eliminar_carro():
    leer_carros()
    id_carro = int(input("\nIngrese el ID del carro a eliminar: "))
    
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Carros WHERE id_carro = %s", (id_carro,))
        conn.commit()
        print("✅ Carro eliminado.")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        cur.close()
        conn.close()

# --- CONSULTAS DEL PROFESOR ---

def ejecutar_consultas_especiales():
    conn = get_connection()
    cur = conn.cursor()
    
    print("\n--- RESULTADOS DE LAS CONSULTAS DEL PROYECTO ---")
    
    # Consulta 1: Ventas por Concesionaria
    print("\n1. Ventas por Concesionaria:")
    cur.execute("""
        SELECT c.nombre, SUM(v.monto) FROM Concesionarias c 
        JOIN Ventas v ON c.id_concesionaria = v.id_concesionaria 
        GROUP BY c.nombre ORDER BY 2 DESC
    """)
    for r in cur.fetchall(): print(f"- {r[0]}: ${r[1]}")

    # Consulta 3: Catalogación (Exposición > 2022)
    print("\n2. Carros de Exposición (>2022):")
    cur.execute("SELECT marca, modelo FROM Carros WHERE estado = 'Exposición' AND anio > 2022")
    for r in cur.fetchall(): print(f"- {r[0]} {r[1]}")

    # Consulta 5: Participantes Gasto > 30k
    print("\n3. Participantes con gasto > $30,000:")
    cur.execute("""
        SELECT p.nombre, SUM(v.monto) FROM Participantes p 
        JOIN Ventas v ON p.id_participante = v.id_participante_comprador 
        GROUP BY p.nombre HAVING SUM(v.monto) > 30000
    """)
    for r in cur.fetchall(): print(f"- {r[0]}: ${r[1]}")

    cur.close()
    conn.close()

# --- MENÚ PRINCIPAL ---

def main():
    while True:
        print("\n================================")
        print("   SISTEMA CARROS Y CARRERAS")
        print("================================")
        print("1. Agregar Carro (Create)")
        print("2. Ver Carros (Read)")
        print("3. Actualizar Precio (Update)")
        print("4. Eliminar Carro (Delete)")
        print("5. EJECUTAR REPORTES DEL PROFE")
        print("6. Salir")
        
        op = input("\nSeleccione una opción: ")
        
        if op == "1": crear_carro()
        elif op == "2": leer_carros()
        elif op == "3": actualizar_carro()
        elif op == "4": eliminar_carro()
        elif op == "5": ejecutar_consultas_especiales()
        elif op == "6": break
        else: print("Opción no válida.")

if __name__ == "__main__":
    main()