"""
Script para augmentar un grupo de imágenes en especifico.
"""

import os  
import cv2  # Para leer y manipular imágenes
import logging  # Para registrar mensajes de log
import random  # Para seleccionar imágenes aleatoriamente
import albumentations as A  # Para aplicar transformaciones de aumento de datos

# Configuración del logging
logging.basicConfig(level=logging.INFO)  # Establece el nivel de logging a INFO

def has_target_label(label_path: str, target_label: str) -> bool:
    """
    Verifica si un archivo de etiqueta contiene una etiqueta específica.
    """
    if not os.path.exists(label_path):  # Verifica si el archivo de etiqueta existe
        return False
    
    with open(label_path, 'r') as f:  # Abre el archivo de etiqueta en modo lectura
        lines = f.readlines()  # Lee todas las líneas del archivo
        for line in lines:  # Recorre cada línea
            label = line.strip().split()[0]  # Obtiene la etiqueta (primer elemento de la línea)
            if label == target_label:  # Compara la etiqueta con la etiqueta objetivo
                return True
    return False

def noise(input_img_path: str, output_img_path: str, transformations):
    """
    Aplica transformaciones de aumento de datos a una imagen y la guarda.
    """
    input_img = cv2.imread(input_img_path)  # Lee la imagen de entrada
    if input_img is None:  # Verifica si la imagen se leyó correctamente
        logging.error(f"No se pudo leer la imagen {input_img_path}")
        return
    
    augmented = transformations(image=input_img)  # Aplica las transformaciones
    transformed_img = augmented['image']  # Obtiene la imagen transformada
    cv2.imwrite(output_img_path, transformed_img)  # Guarda la imagen transformada
    logging.info(f"Imagen transformada guardada en {output_img_path}")

def noise_group(base_path: str, input_dir: str, labels_dir: str, output_dir: str, transformations, target_label: str, augment_percentage: float):
    """
    Aplica transformaciones de aumento de datos a un grupo de imágenes que contienen una etiqueta específica.
    """
    struct = {
        'input': [],  # Lista de rutas de imágenes de entrada
        'output': []  # Lista de rutas de imágenes de salida (no se usa en este código)
    }
    
    # Obtener todas las imágenes en el directorio de entrada
    for img_name in os.listdir(input_dir):
        img_path = os.path.join(input_dir, img_name)
        if os.path.isfile(img_path):  # Verifica si es un archivo (no una carpeta)
            struct['input'].append(img_path)
    
    # Filtrar imágenes que contienen la etiqueta
    filtered_input = []
    
    for img_path in struct['input']:
        img_name = os.path.splitext(os.path.basename(img_path))[0]  # Obtiene el nombre de la imagen sin extensión
        label_path = os.path.join(labels_dir, f"{img_name}.txt")  # Ruta del archivo de etiqueta correspondiente
        
        if has_target_label(label_path, target_label):  # Verifica si la etiqueta está presente
            filtered_input.append(img_path)
    
    struct['input'] = filtered_input
    logging.info(f"Imágenes con etiqueta {target_label}: {len(struct['input'])}")
    
    if not struct['input']:
        logging.warning("No hay imágenes con la etiqueta objetivo")
        return
    
    # Calcular el número de imágenes a augmentar basado en el porcentaje
    num_images_to_augment = int(len(struct['input']) * (augment_percentage / 100.0))
    if num_images_to_augment < 1:
        num_images_to_augment = 1  # Asegurarse de que al menos una imagen sea augmentada
    
    # Selección aleatoria basada en el porcentaje
    selected_indices = random.sample(range(len(struct['input'])), num_images_to_augment)
    selected_images = [struct['input'][i] for i in selected_indices]
    
    # Aplicar transformaciones a las imágenes seleccionadas
    for img_path in selected_images:
        # Generar nuevo nombre de archivo en el directorio de salida
        original_filename = os.path.basename(img_path)
        output_img_path = os.path.join(output_dir, original_filename)
        
        noise(img_path, output_img_path, transformations)

# Ejemplo de uso
if __name__ == "__main__":
    logging.info("Iniciando augmentación...")
    
    base_path = "ruta/a/tu/carpeta"
    input_dir = os.path.join(base_path, "images")
    labels_dir = os.path.join(base_path, "labels")  # Carpeta donde están los labels
    output_dir = os.path.join(base_path, "augmented_images")  # Carpeta de salida para las imágenes augmentadas
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    target_label = "11"  # Etiqueta específica que deseas augmentar
    augment_percentage = 100  # Porcentaje de imágenes con la etiqueta específica que deseas augmentar (100%)
    
    noise_group(
        base_path=r'backend/Dollar_Bill_Detection_USD/valid',
        input_dir=r'backend/Dollar_Bill_Detection_USD/valid/images',
        labels_dir=r'backend/Dollar_Bill_Detection_USD/valid/labels',  # Carpeta de labels
        output_dir=r'backend/Dollar_Bill_Detection_USD/valid/augmentation',  # Carpeta de salida
        transformations=A.Compose([
            #A.RGBShift(p=1),
            #A.RandomBrightnessContrast(p=1),
            A.Blur(p=0.1),  # Aplica un efecto de desenfoque con una probabilidad del 10%
            A.SaltAndPepper(p=1)  # Aplica ruido sal y pimienta con una probabilidad del 100%
        ]),
        target_label=target_label,
        augment_percentage=augment_percentage
    )
    
    logging.info("Proceso completado")

