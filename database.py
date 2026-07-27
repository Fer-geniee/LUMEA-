import mysql.connector
from mysql.connector import Error
import sqlite3

def conectar_mysql():
    "Estableciendo la conexion con la base de datos"
    try:  
        conexion = mysql.connector.connect(
            host='127.0.0.1',  # Servidor local 
            port=3306,
            user='root',  
            password='Coco2021'  
        )
        if conexion.is_connected():
            print("Conexión a MySQL lista")
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None 


class BaseDatos: 
    def __init__(self):
        self.conexion = conectar_mysql()
        if self.conexion is None:
            print("No se pudo conectar a MySQL. Revisa el servidor.")
        else:
            self.crear_tablas()
    
    def crear_tablas(self): 
        cursor = self.conexion.cursor() 
        
        cursor.execute('CREATE DATABASE IF NOT EXISTS lumea_db') 
        cursor.execute('USE lumea_db') 

               # 1. TABLA DE REGISTRO COMIDA
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
     ## TABLAS DE REGISTRO HIDRATACION   
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hidratacion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE DEFAULT (CURRENT_DATE),      
                cantidad_mL INT
                )
        ''') 
     ## TABLAS REGISTRO DE SUEÑO 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sueño (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE DEFAULT (CURRENT_DATE),      
                horas_sueño FLOAT,
                calidad_sueño VARCHAR(255)
            )
        ''') 
     ## TABLAS DE ACTIVIDAD FÍSICA
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS actividad_fisica (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE DEFAULT (CURRENT_DATE),      
                tipo_actividad VARCHAR(200),
                duracion_minutos INT,
                intensidad VARCHAR(50)
            )
        ''') 
 # 6. TABLA MAESTRA DE ALIMENTOS (DICCIONARIO GLOBAL DE LUMEA)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla_alimentos (
                alimento_codigo VARCHAR(100) PRIMARY KEY,
                nombre_pantalla VARCHAR(100),
                calorias INT,
                es_saludable INT
            )
        ''')
        self.conexion.commit() 
        cursor.close()
        print("🏛️ Estructura de tablas verificada en MySQL.")
        
## __MÓDULO PERFIL___ 
    def guardar_perfil(self, nombre, email, edad, genero, peso, altura):
        cursor = self.conexion.cursor() 
        cursor.execute('DELETE FROM perfil WHERE id = 1')  
        cursor.execute('''
            INSERT OR REPLACE INTO perfil (id, nombre, email, edad, genero, peso, altura)
                   VALUES (1, %s, %s, %s, %s, %s, %s)
        ''', (nombre, email, edad, genero, peso, altura)) # Ejecuta el comando SQL para insertar o reemplazar un registro en la tabla de perfil con los datos proporcionados.
        self.conexion.commit()
        cursor.close() 

    def obtener_perfil(self, nombre, email, edad, genero, peso, altura):
        cursor = self.conexion.cursor()
        cursor.execute('SELECT * FROM perfil WHERE id = 1') 
        resultados = cursor.fetchall() 
        cursor.close() 
        return resultados 
                        
    def registrar_comida(self, alimento, certeza, calorias, es_balanceado):
        """Inserta un nuevo registro de comida detectada en la base de datos."""
        if not self.conexion or not self.conexion.is_connected():
            print("No hay conexión activa a MySQL para registrar el alimento.")
            return
        try:
            cursor = self.conexion.cursor() 
            sql = ''' 
                INSERT INTO historial_comida (alimento_detectado, certeza_ia, calorias_aprox, balanceado)
                VALUES (%s, %s, %s, %s)
            '''
            valores = (alimento, certeza, calorias, es_balanceado)
            cursor.execute(sql, valores)
            self.conexion.commit()  
            cursor.close()
            print("Registro guardado")  
        except Error as e:
            print(f"Error al insertar datos en MySQL: {e}")
        cursor.close()
    
    def obtener_historial_comida(self):
        if not self.conexion or not self.conexion.is_connected():
            return []
        try:
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute('SELECT * FROM historial_comida')
            resultados = cursor.fetchall()
            cursor.close() 
            return resultados  
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            return []
    
    def obtener_informacion_alimento(self, codigo_alimento):
        """Busca en la tabla maestra las calorías y el nombre del alimento."""
        if not self.conexion or not self.conexion.is_connected():
            return None

        try:
            cursor = self.conexion.cursor(dictionary=True) 
            sql = "SELECT nombre_pantalla, calorias, es_saludable FROM tabla_alimentos WHERE alimento_codigo = %s"
            cursor.execute(sql, (codigo_alimento,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except mysql.connector.Error as e:
            print(f" Error al consultar tabla_alimentos: {e}")
            return None
        



if __name__ == "__main__":
    print("Iniciando prueba")
    db = BaseDatos()
    if db.conexion:
        print("Conexión exitosa")
    else:
        print("Error en la conexión")


