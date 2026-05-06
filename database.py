import sqlite3

class BaseDatos: 
    def __init__(self):
        # Se supone que ahora estamos creando una conexión a una base de datos SQLite llamada 'lumea.db'
        self.conexion = sqlite3.connect('lumea.db') # Establece la conexión a la base de datos
        self.crear_tablas() # Llama al método para crear las tablas necesarias en la base de datos
    
    def crear_tablas(self): # Método para crear las tablas necesarias en la base de datos
        cursor = self.conexion.cursor() # Crea un cursor para ejecutar comandos SQL en la base de datos
        # Es la tabla de usuarios para el módulo del perfil 
       # El comando SQL para crear la tabla de usuarios, si la tabla no existe ya. La tabla tiene tres columnas: id (clave primaria autoincremental), nombre (texto no nulo) y email (texto no nulo) 
       
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT,
                email TEXT,
                edad INTEGER, 
                genero TEXT, 
                peso REAL,
                altura INTEGER
            )
        ''') # Ejecuta el comando SQL para crear la tabla de usuarios si no existe
    
     
     ## MÓDULO DE HIDRATACIÓN --- TABLAS 
     # Utilizamos AUTOINCREMENT para que cada vaso de agua sea una nueva fila en la tabla, con un ID único que se incrementa automáticamente cada vez que se agrega un nuevo registro de hidratación. Esto facilita el seguimiento de cada vaso de agua consumido por el usuario.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hidratacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE DEFAULT CURRENT_DATE,      
                cantidad_mL INTEGER
                )
        ''') # Ejecuta el comando SQL para crear la tabla de hidratación si no existe


## TABLAS DE SUEÑO 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sueño (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE DEFAULT CURRENT_DATE,      
                horas_sueño REAL,
                calidad_sueño TEXT
            )
        ''') # Ejecuta el comando SQL para crear la tabla de sueño si no existe


## TABLAS DE ACTIVIDAD FÍSICA
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS actividad_fisica (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE DEFAULT CURRENT_DATE,      
                tipo_actividad TEXT,
                duracion_minutos INTEGER,
                intensidad TEXT
            )
        ''') # Ejecuta el comando SQL para crear la tabla de actividad física si no existe
 
        self.conexion.commit() # commit es confirmar, lo que hace es guardar los cambios 
# realizados en la base de datos después de ejecutar el comando SQL para crear la tabla de usuarios. 
# Esto asegura que la tabla se cree correctamente en la base de datos.
      

## __MÓDULO PERFIL___ 
def guardar_perfil(self, nombre, email, edad, genero, peso, altura):
    cursor = self.conexion.cursor() # Crea un cursor para ejecutar comandos SQL en la base de datos
    # INSERT OR REPLACE: Si el ID 1 ya existe, entonces lo borrará y lo reemplazará con los nuevos datos.
    # para evitar que se dupliquen usuarios. 
    cursor.execute('''
            INSERT OR REPLACE INTO perfil (id, nombre, email, edad, genero, peso, altura)
                   VALUES (1, ?, ?, ?, ?, ?, ?)
        ''', (nombre, email, edad, genero, peso, altura)) # Ejecuta el comando SQL para insertar o reemplazar un registro en la tabla de perfil con los datos proporcionados.
    self.conexion.commit() # Guarda los cambios realizados en la base de datos después de ejecutar el comando SQL para insertar o reemplazar un registro en la tabla de perfil. Esto asegura que los datos se guarden correctamente en la base de datos.
        
def obtener_perfil(self):
    cursor = self.conexion.cursor() # Crea un cursor para ejecutar comandos SQL en la base de datos
    cursor.execute('SELECT * FROM perfil WHERE id = 1') # Ejecuta el comando SQL para seleccionar los datos del perfil con ID 1 de la tabla de perfil.
    return cursor.fetchone() # Devuelve el resultado de la consulta como una "tupla", que es una lista de los datos. Si no se encuentra ningún registro con ID 1, devolverá None.