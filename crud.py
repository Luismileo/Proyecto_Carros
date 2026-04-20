import os
import psycopg2
from psycopg2 import extras
from dotenv import load_dotenv

# 1. Configuración de conexión
load_dotenv()
db_url = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(db_url)

# --- FUNCIONES AUXILIARES ---

def validar_estado():
    """Asegura que el estado sea uno de los permitidos por la base de datos."""
    validos = ["Exposición", "Venta", "Compra"]
    while True:
        valor = input(f"Estado ({'/'.join(validos)}): ").strip().capitalize()
        if valor in validos:
            return valor
        print(f"Error: El estado debe ser uno de estos: {validos}")

def leer_numero(mensaje, tipo=float):
    """Valida que la entrada sea un número para evitar que el programa se cierre."""
    while True:
        try:
            return tipo(input(mensaje))
        except ValueError:
            print(f"Error: Por favor, ingrese un número {'entero' if tipo == int else 'válido'}.")

# --- OPERACIONES CRUD MEJORADAS ---

def crear_carro():
    print("\n--- Agregar Nuevo Carro ---")
    marca = input("Marca: ").strip()
    modelo = input("Modelo: ").strip()
    anio = leer_numero("Año: ", int)
    precio = leer_numero("Precio: ")
    estado = validar_estado()
    
    # El bloque 'with' cierra la conexión y cursor automáticamente
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO Carros (marca, modelo, anio, precio, estado) VALUES (%s, %s, %s, %s, %s)",
                    (marca, modelo, anio, precio, estado)
                )
                conn.commit()
                print("Carro agregado con éxito.")
    except Exception as e:
        print(f"Error de base de datos: {e}")

def leer_carros():
    print("\n--- Lista de Carros ---")
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM Carros ORDER BY id_carro ASC")
                rows = cur.fetchall()
                
                if not rows:
                    print("No hay carros registrados.")
                    return False # Retornamos False para saber que no hay qué actualizar/eliminar
                
                for row in rows:
                    print(f"ID: {row['id_carro']} | {row['marca']} {row['modelo']} ({row['anio']}) - ${row['precio']:.2f} [{row['estado']}]")
                return True
    except Exception as e:
        print(f"Error al leer: {e}")
        return False

def actualizar_carro():
    if not leer_carros(): return
    
    id_carro = leer_numero("\nIngrese el ID del carro a actualizar: ", int)
    nuevo_precio = leer_numero("Nuevo precio: ")
    
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("UPDATE Carros SET precio = %s WHERE id_carro = %s", (nuevo_precio, id_carro))
                conn.commit()
                if cur.rowcount == 0:
                    print(f"No se encontró ningún carro con el ID {id_carro}.")
                else:
                    print("Precio actualizado correctamente.")
    except Exception as e:
        print(f"Error: {e}")

def eliminar_carro():
    if not leer_carros(): return
    
    id_carro = leer_numero("\nIngrese el ID del carro a eliminar: ", int)
    confirmar = input(f"¿Está seguro de eliminar el ID {id_carro}? (s/n): ").lower()
    
    if confirmar != 's':
        print("Operación cancelada.")
        return

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM Carros WHERE id_carro = %s", (id_carro,))
                conn.commit()
                if cur.rowcount == 0:
                    print(f"No se encontró el ID {id_carro}.")
                else:
                    print("Carro eliminado.")
    except Exception as e:
        print(f"Error: {e}")

# --- CONSULTAS DEL PROFESOR (SE MANTIENEN IGUAL PERO CON 'WITH') ---

def ejecutar_consultas_especiales():
    print("\n--- RESULTADOS DE LAS CONSULTAS DEL PROYECTO ---")
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # Consulta 1
                print("\n1. Ventas por Concesionaria:")
                cur.execute("""
                    SELECT c.nombre, SUM(v.monto) FROM Concesionarias c 
                    JOIN Ventas v ON c.id_concesionaria = v.id_concesionaria 
                    GROUP BY c.nombre ORDER BY 2 DESC
                """)
                for r in cur.fetchall(): print(f"- {r[0]}: ${r[1]:,.2f}")

                # Consulta 3
                print("\n2. Carros de Exposición (>2022):")
                cur.execute("SELECT marca, modelo FROM Carros WHERE estado = 'Exposición' AND anio > 2022")
                res2 = cur.fetchall()
                if not res2: print("- No hay resultados.")
                for r in res2: print(f"- {r[0]} {r[1]}")

                # Consulta 5
                print("\n3. Participantes con gasto > $30,000:")
                cur.execute("""
                    SELECT p.nombre, SUM(v.monto) FROM Participantes p 
                    JOIN Ventas v ON p.id_participante = v.id_participante_comprador 
                    GROUP BY p.nombre HAVING SUM(v.monto) > 30000
                """)
                for r in cur.fetchall(): print(f"- {r[0]}: ${r[1]:,.2f}")
    except Exception as e:
        print(f" Error en reportes: {e}")

# --- MENÚ PRINCIPAL ---

def main():
    while True:
        print("\n" + "="*32)
        print("   SISTEMA CARROS Y CARRERAS")
        print("="*32)
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
        elif op == "6": 
            print("Saliendo del sistema...")
            break
        else: print("Opción no válida.")

if __name__ == "__main__":
    main()
