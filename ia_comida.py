import tensorflow as tf
import numpy as np
import os
# os es una biblioteca de Python que proporciona funciones para interactuar con el sistema operativo, como manejar archivos y directorios. 

#path es una submódulo de os que se utiliza para manipular rutas de archivos y directorios de manera independiente del sistema operativo. 
#dirname es una función de os.path que devuelve la ruta del directorio que contiene un archivo dado.
#abspath es una función de os.path que devuelve la ruta absoluta de un archivo dado; la ruta desde la raíz del sistema hasta el actual. 
# join es una función de os.path que se utiliza para unir partes de una ruta de archivo de manera segura, asegurando que se utilicen los separadores de ruta correctos según el sistema operativo.



#Para recordar# Un directorio es una carpeta con carpetas.... :)
# --------   #
batch_size = 32
img_height = (224, 224)

modelo_base = tf.keras.applications.MobileNetV2(
    input_shape =(224, 224, 3), # Especifica la forma de entrada que el modelo espera, en este caso, imágenes de 224x224 píxeles con 3 canales de color (RGB).
    include_top = False, # Las clasificaciones orginilaes no serán importadas, ahora nosotros editaremos el modelo para que se adapte a nuestro proyecto de comida.
    weights = 'imagenet' # Carga los pesos preentrenados del modelo MobileNetV2 que fueron entrenados en el conjunto de datos ImageNet. 
    # Lo anterior  permite que el modelo tenga un buen rendimiento en tareas de clasificación de imágenes sin necesidad de entrenarlo desde cero.
    # Los pesos son los valores que el modelo ha aprendido. 
)

# Congelar el modelo base para el Transfer Learning - IMPORTANTE- Así no perdemos en conocimiento original 
modelo_base.trainable = False 

numero_clases_comida = 101 # Número de clases de comida en el conjunto de datos FOOD-101

lumea_modelo = tf.keras.Sequential([
    modelo_base, # Agrega el modelo base MobileNetV2 como la primera capa de la red neuronal secuencial.
    tf.keras.layers.GlobalAveragePooling2D(), # Agrega una capa de pooling global que reduce la dimensionalidad de las características extraídas por el modelo base, promediando cada mapa de características en un solo valor.
    tf.keras.layers.Dense(numero_clases_comida, activation='softmax') # Agrega una capa densa (fully connected) con un número de unidades igual al número de clases de comida (101) y una función de activación softmax, que convierte las salidas en probabilidades para cada clase.
])

lumea_modelo.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
    loss='sparse_categorical_crossentropy', # Especifica la función de pérdida que se utilizará durante el entrenamiento del modelo. En este caso, 'sparse_categorical_crossentropy' es adecuada para problemas de clasificación multiclase donde las etiquetas son enteros (en lugar de codificadas en one-hot). Esta función de pérdida mide la diferencia entre las probabilidades predichas por el modelo y las etiquetas reales, penalizando más fuertemente las predicciones incorrectas.
    metrics=['accuracy'] # Especifica que se desea evaluar la precisión del modelo durante el entrenamiento y la evaluación. La precisión es una métrica comúnmente utilizada para medir el rendimiento de los modelos de clasificación, indicando el porcentaje de predicciones correctas realizadas por el modelo.
)
# Define el optimizador Adam con una tasa de aprendizaje de 0.001. 
# Esa tasa se utilizará para actualizar los pesos del modelo durante el entrenamiento.
# Adam es un optimizador que combina las ventajas de otros optimizadores como AdaGrad y RMSProp, adaptando la tasa de aprendizaje para cada parámetro de manera eficiente.

 # Quitamos lo de study = lumea_modelo.fit ()



class ClasificadorComida:
    def __init__(self):
        print("🧠 Cargando el cerebro de Lumea de forma local...")
        carpeta_actual = os.path.dirname(os.path.abspath(__file__)) # Obtiene la ruta del directorio actual donde se encuentra el script.  
        # para construir rutas relativas a los archivos del modelo y las imágenes de prueba.
        ruta_modelo = os.path.join(carpeta_actual, 'modelo_lumea_comida.h5') # Construye la ruta completa al archivo del modelo 'modelo_lumea_comida.h5',  
        # ubicado en el mismo directorio que el script.
         
       



        if not os.path.exists(ruta_modelo): # Verifica si el archivo del modelo existe en la ruta especificada. Si no existe, lanza un error indicando que el archivo no se encuentra.
            raise FileNotFoundError(f"⚠️ El archivo del modelo no está en: {ruta_modelo}")
            
        self.modelo = tf.keras.models.load_model(ruta_modelo) # Carga el modelo de TensorFlow desde el archivo 'modelo_lumea_comida.h5' y lo asigna a la variable 'self.modelo' para su uso posterior en las predicciones.
    ## Esta parte del código fue refinada con IA para ayudarle a los desarrolladores con la sintaxis. ⬆️
    
    
        # Las clases de comida de FOOD-101, en el orden del modelo...
        self.clases_comida = [
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


 #Definiendo funciones, módulos y submódulos para que sea más sencillo entender el código #
 # tf.keras es una API que sirve para crear y entrenar modelos de aprendizaje automático de manera sencilla.
 # tf.io es un módulo de TensorFlow que proporciona funciones para leer y escribir datos
 # Una API es la manera en la que nosotros podemos utilizar una biblioteca de código abierto, como Keras, para crear nuestras aplicaciones. 
 # np es la abreviatura para NumPy 
 # expand_dims es una función que agrega una nueva dimensión a un array de NumPy
 # un array es una tabla de datos que puede contener números, texto u otro tipo de información

    def procesar_imagen_local(self, ruta_imagen): # Esta función toma la ruta de una imagen local, la lee, decodifica, redimensiona a 224x224 píxeles, la preprocesa para el modelo MobileNetV2 y la convierte en un formato adecuado para la predicción.
        img = tf.io.read_file(ruta_imagen) # Lee el archivo de imagen desde la ruta especificada y lo carga en memoria como un tensor de bytes.
        img = tf.image.decode_image(img, channels=3, expand_animations=False) # Decodifica el tensor de bytes en una imagen con 3 canales de color (RGB) y evita expandir animaciones (como GIFs), asegurando que la imagen resultante sea un tensor de forma [altura, anchura, 3].
        img = tf.image.resize(img, [224, 224]) # Added specific dimensions to avoid conversion bugs
        img = tf.keras.applications.mobilenet_v2.preprocess_input(img) # Preprocesa la imagen utilizando la función de preprocesamiento específica para MobileNetV2, que ajusta los valores de los píxeles a un rango adecuado para el modelo (normalmente entre -1 y 1).
        img = np.expand_dims(img, axis=0) # Agrega una dimensión adicional al tensor de la imagen para que tenga la forma [1, 224, 224, 3], lo que es necesario para que el modelo pueda procesarla correctamente durante la predicción.
        return img
    
    # self sirve para referirse a la instancia actual de la clase, lo que permite acceder a sus atributos y métodos desde dentro de la clase.
    # En este caso, self.modelo se refiere al modelo de TensorFlow que se cargó en el método __init__. 
    # una instancia es un objeto creado a partir de una clase. 

    def predecir(self, ruta_imagen): # Esta función toma la ruta de una imagen, la procesa utilizando la función 'procesar_imagen_local', realiza una predicción con el modelo cargado y devuelve los 3 alimentos más probables junto con sus porcentajes de certeza.
        imagen_lista = self.procesar_imagen_local(ruta_imagen) # Procesa la imagen utilizando la función 'procesar_imagen_local', lo que devuelve un tensor de imagen listo para ser utilizado en la predicción del modelo.
        predicciones_raw = self.modelo.predict(imagen_lista) # Realiza la predicción utilizando el modelo cargado, pasando la imagen procesada como entrada. El resultado es un array de predicciones que contiene las probabilidades para cada clase de comida.
        
    
        predicciones = predicciones_raw[0] # Extrae el primer elemento del array de predicciones, que contiene las probabilidades para cada clase de comida. Esto se hace porque el modelo devuelve un array de predicciones para cada imagen procesada, y en este caso solo estamos procesando una imagen, por lo que nos quedamos con el primer (y único) conjunto de predicciones.
        resultados_top_3 = [] 
        for indice in indices_top_3:
            porcentaje = float(predicciones[indice] * 100)
            nombre_comida = self.clases_comida[indice] if indice < len(self.clases_comida) else f"Clase #{indice}" # Manejo de índice fuera de rango, es decir, si el índice es mayor que el número de clases disponibles, se asigna un nombre genérico basado en el índice.
            resultados_top_3.append((nombre_comida, porcentaje)) # Agrega una tupla con el nombre de la comida y su porcentaje de certeza a la lista 'resultados_top_3'.
            return resultados_top_3
           # .append es una función de las listas en Python que se utiliza para agregar un elemento al final de la lista. En este caso, se está agregando una tupla (nombre_comida, porcentaje) a la lista resultados_top_3.
    
        
    def formatear_nombre_alimento(nombre_tecnico):
        traducciones = {
            "hamburger": "Hamburguesa Tradicional",
            "pizza": "Pizza Artesanal",
            "pancakes": "Panqueques",
            "croque_madame": "Sándwich con Huevo",
            "omelette": "Tortilla de Huevo (Omelette)",
            "french_fries": "Papas Fritas",
            # Había olvidado esta parte, tengo que actualizarlo. Un momento, esto tengo que eliminarlo. 

        if nombre_tecnico in traducciones:
            return traducciones[nombre_tecnico]
        nombre_limpio = nombre_tecnico.replace("_", " ").title()
        return nombre_limpio  
    
    

# --- PRUEBAS --- 
if __name__ == "__main__":
    from backend.database import BaseDatos
    
    db = BaseDatos()
    clasificador = ClasificadorComida()
    

    carpeta_actual = os.path.dirname(os.path.abspath(__file__))
    # os.path.dirname(os.path.abspath(__file__)) obtiene la ruta del directorio actual donde se encuentra el script, lo que permite construir rutas relativas a los archivos del modelo y las imágenes de prueba de manera más flexible y portátil. Esto es especialmente útil para asegurarse de que el código funcione correctamente sin importar desde dónde se ejecute, siempre y cuando los archivos necesarios estén en el mismo directorio o en subdirectorios relacionados.
    ruta_imagen_prueba = os.path.join(carpeta_actual, 'Test.jpg') 
    
    if not os.path.exists(ruta_imagen_prueba):
        raise FileNotFoundError(f"La imagen de prueba no está en: {ruta_imagen_prueba}") 
    else : 
        print (f"Imagen de prueba encontrada en: {ruta_imagen_prueba}")
        print(f"Aalizando la imagen '{ruta_imagen_prueba}'...")
        top_3_resultados = clasificador.predecir(ruta_imagen_prueba)
        print("\n Top 3 resultados")
        for i, (alimento, certeza) in enumerate(top_3_resultados, 1):
            print(f"{i}. {alimento} -> Certeza: {certeza:.2f}%")
        mejor_alimento, mejor_certeza = top_3_resultados[0]
        nombre_amigable = clasificador.formatear_nombre_alimento(mejor_alimento)

if mejor_certeza >= 70.0: 
            print(f"\n Se ha detectado: {nombre_amigable} con {mejor_certeza:.2f}% de certeza." )
            # Diccionario base.... Tengo mis dudas sobre esto, debe haber otra manera más efectiva de hacerlo. 
            dicc_calorias = {"apple_pie": 237, "baby_back_ribs": 300, "baklava": 250, "beef_carpaccio": 200, "beef_tartare": 250} 
            calorias = dicc_calorias.get(nombre_amigable, 250)
            if db.conexion: 
                db.registrar_comida(nombre_amigable, mejor_certeza, calorias=calorias, es_balanceado=1)
                print("Registro guardado en MySQL")
            else:
                print("No se guardó en la base de datos porque el servidor está desconectado o rechazó el acceso.")               
else:
   print(f"Registro bloqueado. ({mejor_certeza:.2f}%). Intenta con otra foto.")



