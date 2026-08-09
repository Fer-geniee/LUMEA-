import os 
import io 
import numpy as np
import tensorflow as tf
from PIL import Image

Size = (224, 224)
BATCH_SIZE = 32
DATASET_PATH = "dataset/"

training = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    subset="training",
    validation_split=0.2, 
    image_size=Size,
    batch_size=BATCH_SIZE, 
    seed = 123
)
validation = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    subset="validation",
    validation_split=0.2,
    image_size=Size,
    batch_size=BATCH_SIZE, 
    seed = 123
)

classes = training.class_names  
print (f'Clases de entrenamiento: {classes}')

# === Clases en un archivo JSON ===
import json
with open("clases.json", "w", encoding="utf-8") as f: # Escribe las clases en un archivo JSON para que el backend pueda acceder a ellas
    json.dump(classes, f) # 

# ==== Red neuronal ====== #

data_argumentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal_and_vertical"),
    tf.keras.layers.RandomRotation(0.2),
    tf.keras.layers.RandomZoom(0.2),
])

base_model = tf.keras.applications.MobileNetV2(input_shape=Size + (3,), include_top=False, weights='imagenet')
base_model.trainable = False ## Las capas base se congelan para no entrenarlas

# == Capa de entrada === 
input_layer = tf.keras.layers.Input(shape=Size + (3,)) # Capa de entrada
x = data_argumentation(input_layer) 
x = tf.keras.applications.mobilenet_v2.preprocess_input(x) # Normalizar los valores de los píxeles del rango [0,255] al rango [−1,1], que es lo que exige MobileNetV2.
model = base_model(x, training=False) # Se pasa la imagen por la red neuronal
model = tf.keras.layers.GlobalAveragePooling2D()(model) # Aplanar a un vector 1D desde 3D

# == Capa de salida ===
output_layer = tf.keras.layers.Dense(len(classes), activation='softmax')(model) 

# == Modelo final ===
model = tf.keras.Model(inputs=input_layer, outputs=output_layer)

# == Compilación del modelo ===
optomizer = tf.keras.optimizers.Adam(learning_rate=0.0001) # Adam ajusta de manera adaptativa la velocidad de aprendizaje. 
model.compile(
    optimizer=optomizer,
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# == Callbacks ===
EarlyStopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss', # Se monitoriza la pérdida de validación
    min_delta=0.001, # Mínimo cambio en la pérdida para ser considerado
    patience=5, # Número de épocas sin mejora antes de detener el entrenamiento
    verbose=1, # Muestra información en la consola
    restore_best_weights=True # Restaura los pesos del modelo a los de la mejor época al final del entrenamiento
)
ReduceLROnPlateau = tf.keras.callbacks.ReduceLROnPlateau(
    monitor='val_loss', # Se monitoriza la pérdida de validación
    factor=0.2, # Factor por el cual se reduce la tasa de aprendizaje
    verbose=1, 
    patience=3, 
    min_lr=0.00001 # Mínima tasa de aprendizaje a la que se puede reducir. 
) 

ModelCheckpoint = tf.keras.callbacks.ModelCheckpoint(
    'modelo_lumea_comida.h5',
    save_best_only=True, # Guarda solo el mejor modelo
    monitor='val_loss', # Se monitoriza la pérdida de validación
    verbose=1 
) 

# == Entrenamiento del modelo ===
history = model.fit(
    training,
    validation_data = validation,
    epochs = 10, 
    callbacks=[EarlyStopping, ReduceLROnPlateau, ModelCheckpoint]
)   

# == Fine-tuning del modelo ===
base_model.trainable = True # Se desbloquean las capas de la red neuronal para entrenarlas
# Se congela las primeras 100 capas de la red neuronal para no entrenarlas
for layer in base_model.layers[:100]:
    layer.trainable = False 

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
    loss = 'sparse_categorical_crossentropy', 
    metrics = ['accuracy']
)
fine_tune_epochs = 10
total_epochs = 10 + fine_tune_epochs

fine_tuning_history = model.fit(
    training, 
    validation_data=validation,
    epochs=total_epochs,
    initial_epoch=len(history.epoch),
    callbacks=[EarlyStopping, ReduceLROnPlateau, ModelCheckpoint]
)
