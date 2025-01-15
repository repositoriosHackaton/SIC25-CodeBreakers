import os
import shutil

def compare_and_copy(txt_dir, jpg_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    txt_files = [f for f in os.listdir(txt_dir) if f.endswith('.txt')]
    jpg_files = [f for f in os.listdir(jpg_dir) if f.endswith('.jpg')]
    
    jpg_filenames = {os.path.splitext(f)[0] for f in jpg_files}
    
    for txt_file in txt_files:
        txt_filename = os.path.splitext(txt_file)[0]
        if txt_filename in jpg_filenames:
            source_path = os.path.join(txt_dir, txt_file)
            destination_path = os.path.join(output_dir, txt_file)
            shutil.copy(source_path, destination_path)
            print(f"Archivo {txt_file} copiado a {output_dir}")

# Configuración de las carpetas
txt_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection - Copy\datasets _division-copy\output\labels'
jpg_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection - Copy\datasets _division-copy\output\image'
output_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection - Copy\datasets _division-copy\output\label_new'

# Llamar a la función
compare_and_copy(txt_dir, jpg_dir, output_dir)
