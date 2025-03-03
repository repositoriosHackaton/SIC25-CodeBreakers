import os  # Para manejar operaciones del sistema de archivos
import shutil  # Para copiar archivos

def find_and_copy_images(txt_list_file, image_dir, output_dir):
    """
    Busca las imágenes correspondientes a los nombres de los labels previamente listadas en un txt
    y las copia a una carpeta de salida.

    """
    # Crea la carpeta de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Abre el archivo de texto que contiene la lista de nombres de archivos .txt
    with open(txt_list_file, 'r') as file:
        txt_files = file.read().splitlines()  # Lee todas las líneas y las almacena en una lista

    # Recorre cada nombre de archivo .txt en la lista
    for txt_filename in txt_files:
        # Construye el nombre de la imagen correspondiente (mismo nombre pero con extensión .jpg)
        image_filename = os.path.splitext(txt_filename)[0] + '.jpg'
        image_path = os.path.join(image_dir, image_filename)  # Ruta completa de la imagen

        # Verifica si la imagen existe en la carpeta de imágenes
        if os.path.exists(image_path):
            # Copia la imagen a la carpeta de salida
            shutil.copy(image_path, output_dir)
            print(f"Imagen {image_filename} copiada a {output_dir}")
        else:
            print(f"Imagen {image_filename} no encontrada en {image_dir}")

# Configuración de rutas
txt_list_file = r'datasets/incorrect_labels.txt'  # Ruta del archivo de texto con la lista de nombres de archivos .txt
image_dir = r'datasets/images'  # Ruta de la carpeta que contiene las imágenes
output_dir = r'Dollar_Bill_Detection/datasets'  # Ruta de la carpeta de salida donde se copiarán las imágenes

# Llama a la función para buscar y copiar las imágenes
find_and_copy_images(txt_list_file, image_dir, output_dir)
