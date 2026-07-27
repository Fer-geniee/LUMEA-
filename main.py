import os # Es un módulo que proporciona una forma de interactuar con el sistema operativo, permitiendo realizar operaciones como leer y escribir archivos, manipular rutas de archivos, y obtener información del entorno del sistema. 
import keras
import numpy as np  
import tensorflow as tf 
from flask import Flask, request, jsonify # Flask es un microframework web para Python que permite crear aplicaciones web de manera sencilla. request se utiliza para manejar las solicitudes HTTP entrantes y jsonify se utiliza para convertir datos en formato JSON para enviarlos como respuesta.   
from flask_cors import CORS # Flask-CORS es una extensión de Flask que permite habilitar el intercambio de recursos de origen cruzado (CORS) en aplicaciones web, lo que permite que los navegadores realicen solicitudes a dominios diferentes al del servidor de la aplicación.
from werkzeug.utils import secure_filename # secure_filename es una función de la biblioteca Werkzeug que se utiliza para asegurar que los nombres de archivo sean seguros y válidos, evitando problemas de seguridad al guardar archivos en el servidor.
from database import BaseDatos # Importa la clase BaseDatos desde el módulo database, que probablemente contiene la lógica para interactuar con la base de datos de la aplicación.

# Inicializar Flask y habilitar CORS 
# Esto se hace para permitir que la aplicación web pueda recibir solicitudes desde diferentes dominios, lo cual es útil en entornos de desarrollo y producción donde el frontend y el backend pueden estar en servidores distintos.
app = Flask(__name__) # Crea una instancia de la aplicación Flask, que servirá como el núcleo de la aplicación web.
CORS(app)

# Configuración e inicialización de la base de datos
db = BaseDatos() 
print ("Conexión a la base de datos establecida, Flask inicializado y CORS habilitado.") 
modelo_ia = tf.keras.applications.MobileNetV2(weights='imagenet') # Cargar el modelo 

clases_comida = [
'apple_pie', 'baby_back_ribs', 'baklava', 'beef_carpaccio', 'beef_tartare', 
'beet_salad', 'beignets', 'bibimbap', 'bread_pudding', 'breakfast_burrito', 
'bruschetta', 'caesar_salad', 'cannoli', 'caprese_salad', 'carrot_cake', 'ceviche', 
'cheesecake', 'cheese_plate', 'chicken_curry', 'chicken_quesadilla', 'chicken_wings', 
'chocolate_cake', 'chocolate_mousse', 'churros', 'clam_chowder', 'club_sandwich', 'crab_cakes', 
'creme_brulee', 'croque_madame', 'cup_cakes', 'deviled_eggs', 'donuts', 'dumplings', 'edamame', 
'eggs_benedict', 'escargots', 'falafel', 'filet_mignon', 'fish_and_chips', 'foie_gras', 
'french_fries', 'french_onion_soup', 'french_toast', 'fried_calamari', 'fried_rice', 'frozen_yogurt',
'garlic_bread', 'gnocchi', 'greek_salad', 'grilled_cheese_sandwich', 'grilled_salmon', 'guacamole',
'gyoza', 'hamburger', 'hot_and_sour_soup', 'hot_dog', 'huevos_rancheros', 'hummus', 'ice_cream', 
'lasagna', 'lobster_bisque', 'lobster_roll_sandwich', 'macaroni_and_cheese', 'macarons', 'miso_soup', 
'mussels', 'nachos', 'omelette', 'onion_rings', 'oysters', 'pad_thai', 'paella', 'pancakes', 
'panna_cotta', 'peking_duck', 'pho', 'pizza', 'pork_chop', 'poutine', 'prime_rib', 
'pulled_pork_sandwich', 'ramen', 'ravioli', 'red_velvet_cake', 'risotto', 'samosa', 
'sashimi', 'scallops', 'seaweed_salad', 'shrimp_and_grits', 'spaghetti_bolognese', 
'spaghetti_carbonara', 'spring_rolls', 'steak', 'strawberry_shortcake', 'sushi', 'tacos', 
'takoyaki', 'tiramisu', 'tuna_tartare', 'waffles'
]

def formatear_nombre(nombre_tecnico):
    ""
    "Retorna el nombre del alimento, dada la calse del modelo de IA."
    ""
    traducciones = {
        'apple_pie': 'Tarta de manzana',
        'baby_back_ribs': 'Costillas de cerdo',
        'baklava': 'Baklava',
        'beef_carpaccio': 'Carpaccio de ternera', 
        'beef_tartare': 'Tartar de ternera',
        'beet_salad': 'Ensalada de remolacha',
        'beignets': 'Buñuelos', 
        'bibimbap': 'Bibimbap',
        'bread_pudding': 'Budín de pan',
        'breakfast_burrito': 'Burrito de desayuno',
        'bruschetta': 'Bruschetta',
        'caesar_salad': 'Ensalada César',
        'cannoli': 'Cannoli',
        'caprese_salad': 'Ensalada Caprese',
        'carrot_cake': 'Pastel de zanahoria',
        'ceviche': 'Ceviche',
        'cheesecake': 'Tarta de queso', 
        'cheese_plate': 'Plato de quesos',
        'chicken_curry': 'Curry de pollo',
        'chicken_quesadilla': 'Quesadilla de pollo',
        'chicken_wings': 'Alitas de pollo',
        'chocolate_cake': 'Pastel de chocolate',
        'chocolate_mousse': 'Mousse de chocolate',
        'churros': 'Churros',
        'clam_chowder': 'Sopa de almejas',
        'club_sandwich': 'Sándwich club',
        'crab_cakes': 'Pasteles de cangrejo',
        'creme_brulee': 'Crema catalana',   
        'croque_madame': 'Croque Madame',
        'cup_cakes': 'Magdalenas',
        'deviled_eggs': 'Huevos rellenos',
        'donuts': 'Donas',
        'dumplings': 'Dumplings',
        'edamame': 'Edamame',
        'eggs_benedict': 'Huevos benedictinos',
        'escargots': 'Caracoles',
        'falafel': 'Falafel',
        'filet_mignon': 'Filete mignon',
        'fish_and_chips': 'Pescado con patatas fritas',
        'foie_gras': 'Foie gras',
        'french_fries': 'Papas fritas',     
        'french_onion_soup': 'Sopa de cebolla francesa',
        'french_toast': 'Tostadas francesas',
        'fried_calamari': 'Calamares fritos',
        'fried_rice': 'Arroz frito',
        'frozen_yogurt': 'Yogur helado',
        'garlic_bread': 'Pan de ajo',
        'gnocchi': 'Ñoquis',
        'greek_salad': 'Ensalada griega',
        'grilled_cheese_sandwich': 'Sándwich de queso a la parrilla',
        'grilled_salmon': 'Salmón a la parrilla',
        'guacamole': 'Guacamole',
        'gyoza': 'Gyoza',
        'hamburger': 'Hamburguesa',
        'hot_and_sour_soup': 'Sopa agripicante',
        'hot_dog': 'Perro caliente',
        'huevos_rancheros': 'Huevos rancheros',     
        'hummus': 'Hummus',
        'ice_cream': 'Helado',
        'lasagna': 'Lasaña',
        'lobster_bisque': 'Bisque de langosta',
        'lobster_roll_sandwich': 'Sándwich de langosta',
        'macaroni_and_cheese': 'Macarrones con queso',
        'macarons': 'Macarons',
        'miso_soup': 'Sopa de miso',
        'mussels': 'Mejillones',
        'nachos': 'Nachos',
        'omelette': 'Tortilla francesa',
        'onion_rings': 'Aros de cebolla',
        'oysters': 'Ostras',
        'pad_thai': 'Pad Thai',
        'paella': 'Paella',
        'pancakes': 'Panqueques',
        'panna_cotta': 'Panna cotta',
        'peking_duck': 'Pato Pekín',
        'pho': 'Pho',
        'pizza': 'Pizza',
        'pork_chop': 'Chuleta de cerdo',
        'poutine': 'Poutine',
        'prime_rib': 'Costilla de res', 
        'pulled_pork_sandwich': 'Sándwich de cerdo desmenuzado',
        'ramen': 'Ramen',
        'ravioli': 'Raviolis',
        'red_velvet_cake': 'Pastel de red velvet',
        'risotto': 'Risotto',
        'samosa': 'Samosa',
        'sashimi': 'Sashimi',
        'scallops': 'Vieiras',
        'seaweed_salad': 'Ensalada de algas',
        'shrimp_and_grits': 'Camarones con sémola',
        'spaghetti_bolognese': 'Espaguetis a la boloñesa',
        'spaghetti_carbonara': 'Espaguetis a la carbonara',
        'spring_rolls': 'Rollitos de primavera',
        'steak': 'Bistec',
        'strawberry_shortcake': 'Pastel de fresa',
        'sushi': 'Sushi',
        'tacos': 'Tacos',
        'takoyaki': 'Takoyaki',
        'tiramisu': 'Tiramisú',     
        'tuna_tartare': 'Tartar de atún',
        'waffles': 'Waffles'
    }

    if nombre_tecnico in traducciones:
        return traducciones[nombre_tecnico]
    else: 
        return nombre_tecnico.replace('_', ' ').title()

@app.route('/predecir', methods=['POST']) # Ruta en Flask para solicitudes POST en una URL: '/predecir'.  
def predecir():
    """Predecir el nombre de un alimento."""
    # 1. Verificar si realmente se envió un archivo de imagen
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró la imagen en la petición.'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo o la imagen está vacía.'}), 400

    try:
        img = tf.image.decode_jpeg(file.read(), channels=3)  # Actualización necesaria: Agregar formatos
        img = tf.image.resize(img, (224, 224)) 
        img_array = tf.keras.preprocessing.image.img_to_array(img).copy() 
        img_array = np.expand_dims(img_array, axis=0) 
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array) 

        predicciones = modelo_ia.predict(img_array) 
        # Para recordar: Un  array es una estructura de datos que permite almacenar una colección de elementos del mismo tipo bajo un mismo nombre
        
        import keras
        decode_predictions = keras.applications.mobilenet_v2.decode_predictions
        resultados = decode_predictions(predicciones, top=1)[0]. # Adoro los parámetros. Facilitan todo... 
        _, nombre_tecnico, probabilidad = resultados[0] 
        nombre_amigable = formatear_nombre(nombre_tecnico) 
        mejor_certeza = float(probabilidad) * 100.0 

        info_alimento = db.obtener_informacion_alimento(nombre_tecnico) 
        if info_alimento:
            nombre_amigable = info_alimento.get("nombre_pantalla", formatear_nombre(nombre_tecnico))
            calorias = info_alimento.get("calorias", 250)
            es_balanceado = info_alimento.get("es_saludable", 0)
        else: 
            nombre_amigable = formatear_nombre(nombre_tecnico)
            calorias = 250 
            es_balanceado = 0 
            # valores por defecto
        guardado_exitoso = False 

        if mejor_certeza >= 70.0: # ¿Deberíamos exigir más confianza?
            if db.conexion and db.conexion.is_connected():
                db.registrar_comida(nombre_amigable, float(mejor_certeza), calorias=calorias, es_balanceado=es_balanceado)
                guardado_exitoso = True
                respuesta = {
                    'success': True,
                    'alimento_codigo': nombre_tecnico,
                    'alimento_app': nombre_amigable,
                    'certeza': mejor_certeza,
                    'calorias': calorias,
                    'guardado_baseDatos': guardado_exitoso
                }
        else:
            respuesta = {
                'success': False,
                'guardado_baseDatos': False, 
                'seleccion_manual': True,
                'mensaje': "La certeza de la IA es muy baja para guardarse automáticamente.",
                'certeza': float(mejor_certeza),
                'alimento': nombre_amigable
            }
        return jsonify(respuesta), 200 
    except Exception as e:
def obtener_informacion_nutricional(codigo_predicho):  
    """
    Busca un alimento por su código en MySQL y devuelve sus valores nutricionales.
    Es decir, es como una API interna entre la predicción de la IA y el usuario.
    """
    db = BaseDatos()
    if not db.conexion or not db.conexion.is_connected():
        return {"error": "Error en la conexión de la base de datos"}

    try:
        cursor = db.conexion.cursor(dictionary=True) 
        sql = "SELECT nombre_pantalla, calorias, es_saludable FROM tabla_alimentos WHERE alimento_codigo = %s"
        cursor.execute(sql, (codigo_predicho,))
        resultado = cursor.fetchone() 
    
        if resultado:
            return {
                "encontrado": True,
                "nombre": resultado["nombre_pantalla"],
                "calorias": resultado["calorias"],
                "es_saludable": bool(resultado["es_saludable"])
            }
        else: 
            return {"encontrado": False, "error": "Alimento no registrado en la base de datos de la app"}
    except Exception as e:
        return {"error": f"No hay conexión con el backend"}
    finally: 
        if 'cursor' in locals(): 
            cursor.close
        db.cerrar_conexion()

@app.route('/historial', methods=['GET'])
def obtener_historial():
    """Obtener todas las comidas registradas"""
    try: 
        historial = db.obtener_historial_comida()
        return jsonify({
            'sucess': True, 
            'cantidad_registros': len(historial),
            'historial': historial
        }), 200 
    except Exception as e: 
        return jsonify({'error': f'Error al consultar el historial: {str(e)}'}), 500

@app.route('/alimentos', methods= ['GET'])
def lista_alimentos():
    """Obtener la lista de alimentos para seleccionar"""
    try: 
        cursor = db.conexion.cursor(dictionary= True) 
        sql = "Select alimento_codigo, nombre_pantalla, calorias FROM tabla_alimentos" 
        cursor.execute(sql) 
        alimentos = cursor.fetchall()
        cursor.close() 
        return jsonify({
            'success': True, 
            'cantidad': len(alimentos),
            'alimentos': alimentos
        }), 200 
    except Exception as e: 
        return jsonify({'Error': f'Error al obtener la lista de alimentos: {str(e)}'}), 500 # 500 significa error


if __name__ == '__main__':
    app.run(debug=True) 

## Normalmente utilizo los comentarios para que se me quede lo que he aprendido sobre algún método, parámetro, libreria o artilugio nuevo. 
