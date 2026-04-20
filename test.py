import os
import psycopg2
from dotenv import load_dotenv

# Esto lee el archivo .env
load_dotenv()
db_url = os.getenv("DATABASE_URL")

try:
    # Intentamos conectar
    print("Conectando a Neon...")
    conn = psycopg2.connect(db_url)
    cur = conn.cursor()
    
    # Le pedimos la hora a la base de datos para probar
    cur.execute("SELECT NOW();")
    tiempo = cur.fetchone()
    
    print("✅ ¡CONEXIÓN EXITOSA!")
    print(f"La hora en el servidor de Neon es: {tiempo[0]}")
    
    cur.close()
    conn.close()

except Exception as e:
    print(f"❌ Error al conectar: {e}")