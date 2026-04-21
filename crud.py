import os
import psycopg2
from psycopg2 import extras, sql
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(db_url)

def leer_texto(mensaje):
    return input(mensaje).strip()

def leer_numero(mensaje, tipo=float):
    while True:
        try:
            valor = input(mensaje)
            if not valor: return None
            return tipo(valor)
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")

def seleccionar_tabla():
    tablas = {
        "1": "instalaciones",
        "2": "talleres",
        "3": "concesionarias",
        "4": "clubes",
        "5": "participantes",
        "6": "eventos",
        "7": "carros"
    }
    print("\n--- SELECCIONE TABLA ---")
    for k, v in tablas.items():
        print(f"{k}. {v.capitalize()}")
    op = input("\nOpción: ")
    return tablas.get(op)

def crear_registro():
    tabla = seleccionar_tabla()
    if not tabla: return
    
    campos = []
    valores = []

    if tabla == "instalaciones":
        campos = ["nombre", "ubicacion", "capacidad"]
        valores = [leer_texto("Nombre: "), leer_texto("Ubicación: "), leer_numero("Capacidad: ", int)]
    elif tabla == "talleres":
        campos = ["nombre", "especialidad"]
        valores = [leer_texto("Nombre: "), leer_texto("Especialidad: ")]
    elif tabla == "participantes":
        campos = ["nombre", "presupuesto", "correo"]
        valores = [leer_texto("Nombre: "), leer_numero("Presupuesto: "), leer_texto("Correo: ")]
    elif tabla == "eventos":
        campos = ["nombre", "fecha", "tipo", "id_instalacion"]
        valores = [leer_texto("Nombre: "), leer_texto("Fecha (AAAA-MM-DD): "), 
                   leer_texto("Tipo: "), leer_numero("ID Instalación: ", int)]
    elif tabla == "carros":
        campos = ["marca", "modelo", "anio", "precio", "estado"]
        valores = [leer_texto("Marca: "), leer_texto("Modelo: "), leer_numero("Año: ", int), 
                   leer_numero("Precio: "), leer_texto("Estado: ")]

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                # La clave aquí es usar sql.Identifier para que Python respete los nombres de tabla
                query = sql.SQL("INSERT INTO {t} ({f}) VALUES ({v})").format(
                    t=sql.Identifier(tabla),
                    f=sql.SQL(', ').join(map(sql.Identifier, campos)),
                    v=sql.SQL(', ').join(sql.Placeholder() * len(valores))
                )
                cur.execute(query, valores)
                conn.commit()
                print(f"\nÉxito: Registro añadido a '{tabla}'.")
    except Exception as e:
        print(f"\nError: {e}")

def main():
    while True:
        print("\n1. Insertar | 2. Consultar | 5. Salir")
        op = input("Seleccione: ")
        if op == "1": crear_registro()
        elif op == "5": break

if __name__ == "__main__":
    main()
