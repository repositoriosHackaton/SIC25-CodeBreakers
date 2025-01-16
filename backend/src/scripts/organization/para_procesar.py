import os
import shutil

def find_and_copy_images(txt_list_file, image_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(txt_list_file, 'r') as file:
        txt_files = file.read().splitlines()

    for txt_filename in txt_files:
        image_filename = os.path.splitext(txt_filename)[0] + '.jpg'
        image_path = os.path.join(image_dir, image_filename)
        
        if os.path.exists(image_path):
            shutil.copy(image_path, output_dir)
            print(f"Imagen {image_filename} copiada a {output_dir}")
        else:
            print(f"Imagen {image_filename} no encontrada en {image_dir}")

# Configuración
txt_list_file = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection\datasets\incorrect_labels.txt'
image_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection\datasets\images'
output_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection\datasets'

find_and_copy_images(txt_list_file, image_dir, output_dir)
