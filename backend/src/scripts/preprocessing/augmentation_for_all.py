"""
Script para augmentar todas las imagenes de una carpeta.
"""

import os
import cv2
import logging
import random
import albumentations as A

# Configuración del logging
logging.basicConfig(level=logging.INFO)

def noise(input_img_path: str, output_img_path: str, transformations):
    input_img = cv2.imread(input_img_path)
    if input_img is None:
        logging.error(f"No se pudo leer la imagen {input_img_path}")
        return
    
    augmented = transformations(image=input_img)
    transformed_img = augmented['image']
    cv2.imwrite(output_img_path, transformed_img)
    logging.info(f"Imagen transformada guardada en {output_img_path}")

def noise_group(base_path: str, input_dir: str, output_dir: str, transformations, augment_percentage: float):
    struct = {
        'input': [],
        'output': []
    }
    
    # Obtener todas las imágenes en el directorio de entrada
    for img_name in os.listdir(input_dir):
        img_path = os.path.join(input_dir, img_name)
        if os.path.isfile(img_path):
            struct['input'].append(img_path)
    
    logging.info(f"Total de imágenes encontradas: {len(struct['input'])}")
    
    if not struct['input']:
        logging.warning("No hay imágenes en el directorio de entrada")
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


if __name__ == "__main__":
    logging.info("Iniciando augmentación...")
    
    base_path = r"backend/Dollar_Bill_Detection_VEF/datasets"
    input_dir = os.path.join(base_path, "images")
    output_dir = os.path.join(base_path, "augmented")  # Carpeta de salida para las imágenes augmentadas
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    augment_percentage = 70  # Porcentaje de imágenes que deseas augmentar
    
    noise_group(
        base_path=r'backend/Dollar_Bill_Detection_VEF/valid',
        input_dir=r'backend/Dollar_Bill_Detection_VEF/valid/images',
        output_dir=r'backend/Dollar_Bill_Detection_VEF/valid/augmented',  # Carpeta de salida
        transformations=A.Compose([
            #A.RGBShift(p=1),
            #A.RandomBrightnessContrast(p=1),
            A.Blur(p=0.1),
            A.SaltAndPepper(p=1)
        ]),
        augment_percentage=augment_percentage
    )
    
    logging.info("Proceso completado")
