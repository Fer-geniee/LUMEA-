import mysql.connector
from mysql.connector import Error
import sqlite3

def conectar_mysql():
    "Estableciendo la conexion con la base de datos"
    try:  
        conexion = mysql.connector.connect(
            host='127.0.0.1',  # Es el servidor local, nos sirve para conectarnos a una base de datos que está en nuestra propia computadora
            port=3306,
            user='root',  # Según lo que investigué, es el usuario por defecto 
            password='Coco2021'  # Contraseña de MySQL 
        )
        if conexion.is_connected():
            print("Conexión a MySQL exitosa!")
            return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None 


class BaseDatos: 
    def __init__(self): # esta función __init__ es un método especial de python, se ejecuta cada vez que tenemos una nueva instancia de la clase BaseDatos. Se encarga de hacer la conexión a la base de datos. 
        # Conectando a MySQL
        self.conexion = conectar_mysql()
        # Si la conexión falla por algún motivo, nos aseguramos de que no explote, o manejamos el error:
        if self.conexion is None:
            print("No se pudo conectar a MySQL. Revisa tu servidor.")
        else:
            self.crear_tablas()
    
    def crear_tablas(self): # Método para crear las tablas necesarias en la base de datos
        cursor = self.conexion.cursor() # Crea un cursor para ejecutar comandos SQL en la base de datos
        
        cursor.execute('CREATE DATABASE IF NOT EXISTS lumea_db') # Crea la base de datos si no existe
        cursor.execute('USE lumea_db') # Selecciona la base de datos para usarla

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
     ## MÓDULO DE HIDRATACIÓN --- TABLAS 
     # Utilizamos AUTOINCREMENT para que cada vaso de agua sea una nueva fila en la tabla, con un ID único que se incrementa automáticamente cada vez que se agrega un nuevo registro de hidratación. Esto facilita el seguimiento de cada vaso de agua consumido por el usuario.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hidratacion (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE DEFAULT (CURRENT_DATE),      
                cantidad_mL INT
                )
        ''') # Ejecuta el comando SQL para crear la tabla de hidratación si no existe
     ## TABLAS DE SUEÑO 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sueño (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE DEFAULT (CURRENT_DATE),      
                horas_sueño FLOAT,
                calidad_sueño VARCHAR(255)
            )
        ''') # Ejecuta el comando SQL para crear la tabla de sueño si no existe
     ## TABLAS DE ACTIVIDAD FÍSICA
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS actividad_fisica (
                id INT AUTO_INCREMENT PRIMARY KEY,
                fecha DATE DEFAULT (CURRENT_DATE),      
                tipo_actividad VARCHAR(200),
                duracion_minutos INT,
                intensidad VARCHAR(50)
            )
        ''') # Ejecuta el comando SQL para crear la tabla de actividad física si no existe
 # 6. TABLA MAESTRA DE ALIMENTOS (DICCIONARIO GLOBAL DE LUMEA)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tabla_alimentos (
                alimento_codigo VARCHAR(100) PRIMARY KEY,
                nombre_pantalla VARCHAR(100),
                calorias INT,
                es_saludable INT
            )
        ''')


        self.conexion.commit() # commit es confirmar, lo que hace es guardar los cambios 
        cursor.close()
        print("🏛️ Estructura de tablas verificada en MySQL.")
## __MÓDULO PERFIL___ 
    def guardar_perfil(self, nombre, email, edad, genero, peso, altura):
        cursor = self.conexion.cursor() # Crea un cursor para ejecutar comandos SQL en la base de datos
    # INSERT OR REPLACE: Si el ID 1 ya existe, entonces lo borrará y lo reemplazará con los nuevos datos.
    # para evitar que se dupliquen usuarios. 
        cursor.execute('DELETE FROM perfil WHERE id = 1') ## Para que no se dupliquen usuarios 
        cursor.execute('''
            INSERT OR REPLACE INTO perfil (id, nombre, email, edad, genero, peso, altura)
                   VALUES (1, %s, %s, %s, %s, %s, %s)
        ''', (nombre, email, edad, genero, peso, altura)) # Ejecuta el comando SQL para insertar o reemplazar un registro en la tabla de perfil con los datos proporcionados.
        self.conexion.commit() # Guarda los cambios realizados en la base de datos después de ejecutar el comando SQL para insertar o reemplazar un registro en la tabla de perfil. Esto asegura que los datos se guarden correctamente en la base de datos.
        cursor.close() # Cierra el cursor después de ejecutar la consulta para liberar recursos

    def obtener_perfil(self, nombre, email, edad, genero, peso, altura):
        cursor = self.conexion.cursor() # Crea un cursor para ejecutar comandos en la base de datos
        cursor.execute('SELECT * FROM perfil WHERE id = 1') # Ejecuta el comando SQL para seleccionar los datos del perfil con ID 1 de la tabla de perfil.
        resultados = cursor.fetchall() # Devuelve una lista con todas las filas guardadas
        cursor.close() # Cierra el cursor 
        return resultados # Devuelve la lista de resultados obtenidos de la consulta
                        
    def registrar_comida(self, alimento, certeza, calorias, es_balanceado):
        """Inserta un nuevo registro de comida detectada en la base de datos."""
        if not self.conexion or not self.conexion.is_connected():
            print("⚠️ No hay conexión activa a MySQL para registrar el alimento.")
            return
        try:
            cursor = self.conexion.cursor() # El comando que sigue sirve para insertar un nuevo registro en la tabla historial_comida de la base de datos MySQL.
            sql = ''' 
                INSERT INTO historial_comida (alimento_detectado, certeza_ia, calorias_aprox, balanceado)
                VALUES (%s, %s, %s, %s)
            '''
            valores = (alimento, certeza, calorias, es_balanceado)
            cursor.execute(sql, valores)
            self.conexion.commit()  # Confirma los cambios en el disco de tu Mac
            cursor.close()
            print("💾 ¡Registro guardado con éxito en tu servidor MySQL (lumea_db)!")  
        except Error as e:
            print(f"❌ Error al insertar datos en MySQL: {e}")
        cursor.close()
    
    def obtener_historial_comida(self):
        if not self.conexion or not self.conexion.is_connected():
            return []
        try:
            # Usamos dictionary=True para que Flask reciba los datos ordenados con sus nombres
            cursor = self.conexion.cursor(dictionary=True)
            cursor.execute('SELECT * FROM historial_comida')
            resultados = cursor.fetchall()
            cursor.close()  # Ahora sí se cierra correctamente
            return resultados  
        except Exception as e:
            print(f"Error al obtener historial: {e}")
            return []
    
    def obtener_informacion_alimento(self, codigo_alimento):
        """Busca en la tabla maestra las calorías y el nombre estético del alimento."""
        if not self.conexion or not self.conexion.is_connected():
            return None

        try:
            cursor = self.conexion.cursor(dictionary=True) # Devuelve el resultado como diccionario
            sql = "SELECT nombre_pantalla, calorias, es_saludable FROM tabla_alimentos WHERE alimento_codigo = %s"
            cursor.execute(sql, (codigo_alimento,))
            resultado = cursor.fetchone()
            cursor.close()
            return resultado
        except mysql.connector.Error as e:
            print(f"❌ Error al consultar tabla_alimentos: {e}")
            return None
        



if __name__ == "__main__": # Solo se ejecutará esta parte si el archivo lo hace directamente
    #Básicamente estamos diciendo que 
    # la función __name__ es una variable especial en Python que se asigna automáticamente al nombre del módulo o archivo.
    
    print("Iniciando prueba de conexión...")
    db = BaseDatos()
    if db.conexion:
        print("¡Base de Datos instanciada correctamente!")
    else:
        print("¡Algo falló en la conexión!")



      
