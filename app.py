 # Es un módulo que proporciona una forma de interactuar con el sistema operativo, permitiendo realizar operaciones como leer y escribir archivos, manipular rutas de archivos, y obtener información del entorno del sistema. 
import keras
import numpy as np # Biblioteca para el cálculo en python 
import tensorflow as tf # Biblioteca de código abierto para el aprendizaje automático y la inteligencia artificial, utilizada para construir y entrenar modelos de aprendizaje profundo.
from flask import Flask, request, jsonify # Flask es un microframework web para Python que permite crear aplicaciones web de manera sencilla. request se utiliza para manejar las solicitudes HTTP entrantes y jsonify se utiliza para convertir datos en formato JSON para enviarlos como respuesta.   
from flask_cors import CORS # Flask-CORS es una extensión de Flask que permite habilitar el intercambio de recursos de origen cruzado (CORS) en aplicaciones web, lo que permite que los navegadores realicen solicitudes a dominios diferentes al del servidor de la aplicación.
from werkzeug.utils import secure_filename # secure_filename es una función de la biblioteca Werkzeug que se utiliza para asegurar que los nombres de archivo sean seguros y válidos, evitando problemas de seguridad al guardar archivos en el servidor.
from database import BaseDatos # Importa la clase BaseDatos desde el módulo database, que probablemente contiene la lógica para interactuar con la base de datos de la aplicación.

# Antes que nada, hay que inicializar Flask y habilitar CORS 
# Esto se hace para permitir que la aplicación web pueda recibir solicitudes desde diferentes dominios, lo cual es útil en entornos de desarrollo y producción donde el frontend y el backend pueden estar en servidores distintos.
app = Flask(__name__) # Crea una instancia de la aplicación Flask, que servirá como el núcleo de la aplicación web.
CORS(app) # Habilita CORS para la aplicación Flask, permitiendo que se realicen solicitudes desde diferentes dominios.

# Configuración e inicialización de la base de datos
db = BaseDatos() # Crea una instancia de la clase BaseDatos, para la conexión y manejo de la base de datos.
print ("Conexión a la base de datos establecida, Flask inicializado y CORS habilitado.") 
modelo_ia = tf.keras.applications.MobileNetV2(weights='imagenet') # Carga el modelo preentrenado MobileNetV2 con pesos entrenados en el conjunto de datos ImageNet, que se utilizará para realizar predicciones de clasificación de imágenes.

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
    return traducciones.get(nombre_tecnico, nombre_tecnico.replace('_', ' ').title())

# ====== Predicción de alimentos ======
@app.route('/predecir', methods=['POST'])  
def predecir():
    # 1. Verificación de la solucitud y del archivo de imagen
    if 'file' not in request.files:
        return jsonify({'error': 'No se encontró el campo de imagen en la petición.'}), 400
    file = request.files['file']
    
    # Validación de la imagen 
    if file.filename == '':
        return jsonify({'error': 'No se seleccionó ningún archivo o la imagen está vacía.'}), 400

    try:
        img = tf.image.decode_jpeg(file.read(), channels=3)
        img = tf.image.resize(img, (224, 224)) 
        img_array = tf.keras.preprocessing.image.img_to_array(img) # Convierte el tensor de imagen en un array de NumPy, que es el formato esperado por el modelo de IA.
        img_array = np.expand_dims(img_array, axis=0) # Agrega una dimensión adicional al array de imagen para que tenga la forma (1, 224, 224, 3), que es la forma esperada por el modelo de IA.
        img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array) 

        predicciones = modelo_ia.predict(img_array) 
        decode_predictions = keras.applications.mobilenet_v2.decode_predictions 
        resultados = decode_predictions(predicciones, top=1)[0] 

        _, nombre_tecnico, probabilidad = resultados[0]
        mejor_certeza = float(probabilidad) * 100.0
        info_alimento = db.obtener_informacion_alimento(nombre_tecnico) 
        if info_alimento:
            nombre_amigable = info_alimento.get("nombre_pantalla", formatear_nombre(nombre_tecnico))
            calorias = info_alimento.get("calorias", 250)
            es_balanceado = info_alimento.get("es_saludable", 1)
        else: 
            nombre_amigable = formatear_nombre(nombre_tecnico)
            calorias = 250 
            es_balanceado = 1 

        guardado_exitoso = False

        if mejor_certeza >= 70.0: 
            guardado_exitoso = db.registrar_comida(nombre_tecnico, 
                nombre_amigable, 
                calorias, 
                es_balanceado, 
                mejor_certeza
                ) 
            respuesta = {
                'success': True,
                'alimento_codigo': nombre_tecnico,
                'alimento_app': nombre_amigable,
                'guardado_baseDatos': guardado_exitoso,
                'mensaje': "Predicción realizada y guardada en la base de datos." if guardado_exitoso else "Predicción realizada pero no se pudo guardar en la base de datos.",
                'certeza': round(mejor_certeza, 2),
                'alimento': nombre_amigable
            }         
        else:
            respuesta = {
                'success': False,
                'guardado_baseDatos': False, 
                'seleccion_manual': True,
                'mensaje': "La certeza de la IA es muy baja para guardarse automáticamente.",
                'certeza': round(mejor_certeza, 2),
                'alimento': nombre_amigable
            }
        
        return jsonify(respuesta), 200 
    except Exception as e:
        return jsonify({'error': f'Error al procesar la imagen: {str(e)}'}), 500 

# ====== Historial ====== 
@app.route('/historial', methods=['GET'])
def obtener_historial_comida():
    try:
        historial = db.obtener_historial_comida()
        return jsonify({
            'success': True,
            'cantidad_registros': len(historial),
            'historial': historial
        }), 200
    except Exception as e:
        return jsonify({'error': f'Error al consultar el historial: {str(e)}'}), 500


# ===== Alimentos disponibles =====
@app.route('/alimentos', methods=['GET'])
def lista_alimentos():
    try:
        if not db.conexion or not db.conexion.is_connected():
            return jsonify({'error': 'Sin conexión a la base de datos'}), 500
            
        cursor = db.conexion.cursor(dictionary=True)
        sql = "SELECT alimento_codigo, nombre_pantalla, calorias, es_saludable FROM tabla_alimentos"
        cursor.execute(sql)
        alimentos = cursor.fetchall()
        cursor.close()

        return jsonify({
            'success': True,
            'cantidad': len(alimentos),
            'alimentos': alimentos
        }), 200
    except Exception as e:
        return jsonify({'error': f'Error al obtener la lista de alimentos: {str(e)}'}), 500

# ==== Cargar aliemntos desde CSV/EXCEL ====
@app.route('/cargar-alimentos-csv', methods=['POST'])
def cargar_alimentos_desde_csv():
    """
    Permite subir un archivo .csv con la estructura:
    alimento_codigo,nombre_pantalla,calorias,es_saludable
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No se adjuntó ningún archivo CSV.'}), 400
        
    file = request.files['file']
    if not file.filename.endswith('.csv'):
        return jsonify({'error': 'El archivo debe tener extensión .csv'}), 400

    try:
        contenido_csv = file.read().decode('utf-8')
        exito, mensaje = db.cargar_alimentos_desde_csv(contenido_csv)
        
        if exito:
            return jsonify({'success': True, 'mensaje': mensaje}), 200
        else:
            return jsonify({'error': mensaje}), 400
    except Exception as e:
        return jsonify({'error': f'Error al leer el archivo: {str(e)}'}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
