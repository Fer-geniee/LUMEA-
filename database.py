import mysql.connector
from mysql.connector import Error
import io 
import csv 

def conectar_mysql():
    """Establece la conexión inicial con el servidor MySQL."""
    try:  
        conexion = mysql.connector.connect(
            host='127.0.0.1',  # Este servidor se tiene que cambiar cuando se presente. 
            port=3306,
            user='root',       
            password= '#####' # CREAR ARCHIVO ENV 
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None 

class BaseDatos: 
    def __init__(self):
        self.conexion = conectar_mysql()
        if self.conexion is None:
            print("No se pudo conectar a MySQL.")
        else:
            self.crear_tablas()

    def crear_tablas(self):
        """Crea la base de datos 'lumea_db' y las tablas necesarias."""
        if not self.conexion or not self.conexion.is_connected():
            return

        cursor = self.conexion.cursor()
        try:
            cursor.execute('CREATE DATABASE IF NOT EXISTS lumea_db')
            cursor.execute('USE lumea_db')

            # 1. TABLA DE TRACKER DE COMIDA
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS historial_comida (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha DATE DEFAULT (CURRENT_DATE),      
                    alimento_detectado VARCHAR(255),
                    certeza_ia FLOAT,
                    calorias_aprox INT,
                    balanceado INT -- 1 para Sí, 0 para No
                )
            ''')

            # 2. TABLA DE PERFIL DE USUARIO
            cursor.execute(''' 
                CREATE TABLE IF NOT EXISTS perfil (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100),
                    email VARCHAR(100),
                    edad INT, 
                    genero VARCHAR(20), 
                    peso FLOAT,
                    altura INT
                )
            ''') 

            # 3. TABLA DE HIDRATACIÓN
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS hidratacion (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha DATE DEFAULT (CURRENT_DATE),      
                    cantidad_mL INT
                )
            ''')

            # 4. TABLA DE SUEÑO 
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sueño (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha DATE DEFAULT (CURRENT_DATE),      
                    horas_sueño FLOAT,
                    calidad_sueño VARCHAR(255)
                )
            ''')

            # 5. TABLA DE ACTIVIDAD FÍSICA
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS actividad_fisica (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    fecha DATE DEFAULT (CURRENT_DATE),      
                    tipo_actividad VARCHAR(200),
                    duracion_minutos INT,
                    intensidad VARCHAR(50)
                )
            ''')

            # 6. TABLA MAESTRA DE ALIMENTOS
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tabla_alimentos (
                    alimento_codigo VARCHAR(100) PRIMARY KEY,
                    nombre_pantalla VARCHAR(100),
                    calorias INT,
                    es_saludable INT
                )
            ''')

            self.conexion.commit()
            print("Estructura de tablas verificada en MySQL (lumea_db).")
            self._poblar_alimentos_iniciales(cursor)

        except Error as e:
            print(f"Error al crear tablas en MySQL: {e}")
        finally:
            cursor.close()


# ==== Exportar datos desde EXCEL/CSV ====
    def cargar_alimentos_desde_csv(self, texto_csv):
        """Carga los alimentos desde un archivo CSV a la tabla maestra.
        (alimento_codigo, nombre_pantalla, calorias, es_saludable)
        """
        if not self.conexion or not self.conexion.is_connected():
            return False, "Sin conexión a MySQL"
        cursor = self.conexion.cursor()
        try:
            stream = io.StringIO(texto_csv, newline=None)
            lector = csv.DictReader(stream)
            registros = [] # verificar si el CSV tiene encabezados correctos
            for fila in lector: 
                codigo = fila.get('alimento_codigo', '').strip()
                nombre = fila.get('nombre_pantalla', '').strip()
                calorias = int(fila.get('calorias', 0)) 
                es_saludable = int(fila.get('es_saludable', 0))
                if codigo: 
                    registros.append((codigo, nombre, calorias, es_saludable))
            if not registros:
                return False, "CSV vacío o sin encabezados correctos"
            sql = '''
                INSERT INTO tabla_alimentos (alimento_codigo, nombre_pantalla, calorias, es_saludable)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    nombre_pantalla = VALUES(nombre_pantalla),
                    calorias = VALUES(calorias),
                    es_saludable = VALUES(es_saludable)
            '''
            cursor.executemany(sql, registros)
            self.conexion.commit()
            return True, f"{len(registros)} registros insertados/actualizados en tabla_alimentos."
        except Exception as e:
            return False, f"Error al cargar alimentos desde CSV: {e}"
        finally:
            cursor.close()

    # ================= MÓDULO PERFIL =================
    def guardar_perfil(self, nombre, email, edad, genero, peso, altura):
        """Guarda o actualiza el perfil principal (ID=1)."""
        if not self.conexion or not self.conexion.is_connected():
            return False
        cursor = self.conexion.cursor()
        try:
            sql = '''
                REPLACE INTO perfil (id, nombre, email, edad, genero, peso, altura)
                VALUES (1, %s, %s, %s, %s, %s, %s)
            '''
            cursor.execute(sql, (nombre, email, edad, genero, peso, altura))
            self.conexion.commit()
            print("Perfil guardado con éxito.")
            return True
        except Error as e:
            print(f"Error al guardar perfil: {e}")
            return False
        finally:
            cursor.close()

    def obtener_perfil(self):
        """CORRECCIÓN: Ya no exige parámetros para leer el perfil del usuario."""
        if not self.conexion or not self.conexion.is_connected():
            return None
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM perfil WHERE id = 1')
            resultado = cursor.fetchone()
            return resultado
        except Error as e:
            print(f" Error al obtener perfil: {e}")
            return None
        finally:
            cursor.close()

    # ================= MÓDULO HISTORIAL Y ALIMENTOS =================
    def registrar_comida(self, alimento, certeza, calorias, es_balanceado):
        """Inserta un registro de comida procesada por la IA."""
        if not self.conexion or not self.conexion.is_connected():
            print("No hay conexión activa a MySQL.")
            return False
        cursor = self.conexion.cursor()
        try:
            sql = ''' 
                INSERT INTO historial_comida (alimento_detectado, certeza_ia, calorias_aprox, balanceado)
                VALUES (%s, %s, %s, %s)
            '''
            valores = (alimento, certeza, calorias, es_balanceado)
            cursor.execute(sql, valores)
            self.conexion.commit()
            print("Registro guardado en MySQL")
            return True
        except Error as e:
            print(f"Error al insertar comida: {e}")
            return False
        finally:
            cursor.close() # C

    def obtener_historial_comida(self):
        """Obtiene todo el historial registrado en la BD."""
        if not self.conexion or not self.conexion.is_connected():
            return []
        cursor = self.conexion.cursor(dictionary=True)
        try:
            cursor.execute('SELECT * FROM historial_comida ORDER BY id DESC')
            return cursor.fetchall()
        except Error as e:
            print(f" Error al obtener historial: {e}")
            return []
        finally:
            cursor.close()

    def obtener_informacion_alimento(self, codigo_alimento):
        """Busca la información de la tabla maestra según la predicción de la IA."""
        if not self.conexion or not self.conexion.is_connected():
            return None
        cursor = self.conexion.cursor(dictionary=True)
        try:
            sql = "SELECT nombre_pantalla, calorias, es_saludable FROM tabla_alimentos WHERE alimento_codigo = %s"
            cursor.execute(sql, (codigo_alimento,))
            return cursor.fetchone()
        except Error as e:
            print(f"Error al consultar tabla_alimentos: {e}")
            return None
        finally:
            cursor.close()

    # ================= MÓDULOS SALUD =================
    def registrar_hidratacion(self, cantidad_ml):
        """Registra el agua."""
        if not self.conexion or not self.conexion.is_connected():
            return False
        cursor = self.conexion.cursor()
        try:
            cursor.execute("INSERT INTO hidratacion (cantidad_mL) VALUES (%s)", (cantidad_ml,))
            self.conexion.commit()
            return True
        except Error as e:
            print(f"Error en hidratación: {e}")
            return False
        finally:
            cursor.close()

if __name__ == "__main__":
    print("Iniciando prueba de conexión a MySQL...")
    db = BaseDatos()
    if db.conexion and db.conexion.is_connected():
        print("Base de datos lista")
    else:
        print("Verifica que el servidor esté activo")
