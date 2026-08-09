import json
import os
import numpy as np
import tensorflow as tf
from PIL import Image
import io 

# == Modelo y lista de clases ===
model = tf.keras.models.load_model("modelo_lumea_comida.h5") 

with open("clases.json", "r", encoding="utf-8") as f:
    classes = json.load(f)

def predecir_alimento(image_bytes: bytes):
    """ Recibe los bytes, procesa la imágen y devuelve la clase predicha."""
    # Cargar la imagen y redimensionarla al tamaño esperado por el modelo
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))

    # Convertir la imagen a un array de numpy y normalizar los valores de los píxeles
    image_array = np.array(image, dtype=np.float32) 

    # Añadir una dimensión extra para representar el batch size (1 en este caso)
    image_array = np.expand_dims(image_array, axis=0)

    # --- Predicciones ---
    predictions = model.predict(image_array)
    clase_final = np.argmax(predictions[0])  # Obtener el índice de la clase con mayor probabilidad
    confianza = float(predictions[0][clase_final])  # Obtener la probabilidad de la clase predicha
    alimento_detectado = classes[clase_final]  # Obtener el nombre de la clase predicha

    return {
        "alimento_detectado": alimento_detectado,
        "confianza_porcentaje": round(confianza * 100, 2)
    }