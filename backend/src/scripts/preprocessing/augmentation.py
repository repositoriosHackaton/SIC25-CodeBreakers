import os
import random
import shutil
import logging
import albumentations as A
import numpy as np
import cv2

# Configuración del logging
logging.basicConfig(level=logging.INFO)

def random_select(struct: dict, percentage):
    num_to_select = int(len(struct['input']) * percentage / 100)
    id_to_select = random.sample(range(len(struct['input'])), num_to_select)

    struct['input'] = [item for i, item in enumerate(struct['input']) if i in id_to_select]
    struct['output'] = [item for i, item in enumerate(struct['output']) if i in id_to_select]

    mixed = list(zip(struct['input'], struct['output']))
    random.shuffle(mixed)
    struct['input'], struct['output'] = zip(*mixed)

    return struct

def divide_select(struct, transformations):
    size_input = len(struct['input'])
    num_of_output = len(transformations) + 1  # +1 Por el mix

    return [size_input // num_of_output + (1 if i < size_input % num_of_output else 0) for i in range(num_of_output)]

def noise(input_img_path: str, output_img_path: str, transformations):
    input_img = cv2.imread(input_img_path)  # Cargar la imagen de entrada
    augmented = transformations(image=input_img)  # Aplicar la transformación de ruido
    transformed_img = augmented['image']  # Obtener la imagen transformada

    cv2.imwrite(output_img_path, transformed_img)
    logging.info(f"Imagen transformada guardada en {output_img_path}")

def noise_group(base_path: str, input_dir: str, output_dir: str, q_percentage: int, transformations):
    from get_struct import get_struct
    
    struct = get_struct(base_path, input_dir, output_dir)

    struct = random_select(struct, q_percentage)

    num_of_output = np.cumsum(divide_select(struct, transformations))

    num_imgs, index_transform = 0, 0
    label_dir = os.path.join(base_path, "label")

    for input_img_path, output_img_path in zip(struct['input'], struct['output']):
        original_filename = os.path.basename(input_img_path)
        name, ext = os.path.splitext(original_filename)
        random_number = random.randint(1000, 9999)
        new_filename = f"{name}_{random_number}{ext}"
        new_output_img_path = os.path.join(os.path.dirname(output_img_path), new_filename)

        # Copiar el archivo original con un nuevo nombre
        shutil.copy(input_img_path, new_output_img_path)
        logging.info(f"Archivo de imagen copiado a {new_output_img_path}")
        
        # Buscar el archivo de etiquetas correspondiente
        original_label_path = os.path.join(label_dir, f"{name}.txt")
        new_label_path = os.path.join(label_dir, f"{name}_{random_number}.txt")

        if os.path.exists(original_label_path):
            shutil.copy(original_label_path, new_label_path)
            logging.info(f"Archivo de etiquetas copiado a {new_label_path}")

        if num_imgs >= num_of_output[index_transform]:
            index_transform += 1

        if index_transform == len(num_of_output) - 1:  # El mix y la última transformación
            noise(new_output_img_path, new_output_img_path, transformations)
        else:
            noise(new_output_img_path, new_output_img_path, transformations[index_transform])

        num_imgs += 1

logging.info("Iniciando procesamiento de grupo de imágenes")

noise_group(
    base_path = r"C:\Users\jesus\Downloads\otra prueba\one",
    input_dir = r"C:\Users\jesus\Downloads\otra prueba\one\image",
    output_dir = r"C:\Users\jesus\Downloads\otra prueba\one\augmentation",
    q_percentage = 35,
    transformations = A.Compose([
        A.RGBShift(r_shift_limit=20, g_shift_limit=20, b_shift_limit=20, p=1),
        A.RandomBrightnessContrast(brightness_limit=0.15, contrast_limit=0.25, p=1),
        A.Blur(blur_limit=4, p=1),
        A.SaltAndPepper(salt_vs_pepper=(0.4, 0.6), amount=(0.01, 0.06), p=1),
    ])
)

logging.info("Procesamiento de grupo de imágenes completado")