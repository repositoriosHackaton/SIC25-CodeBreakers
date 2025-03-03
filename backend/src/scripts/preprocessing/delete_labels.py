import os  # Para manejar operaciones del sistema de archivos
import shutil  # Para copiar archivos

def compare_and_copy(txt_dir, jpg_dir, output_dir):
    """
    Compara los nombres de archivos .txt en una carpeta con los nombres de archivos .jpg en otra carpeta.
    Si un archivo .txt tiene un archivo .jpg correspondiente (mismo nombre sin extensión), copia el archivo .txt
    a una carpeta de salida.
    """
    # Crea la carpeta de salida si no existe
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Obtener la lista de archivos .txt en la carpeta de texto
    txt_files = [f for f in os.listdir(txt_dir) if f.endswith('.txt')]
    
    # Obtener la lista de archivos .jpg en la carpeta de imágenes
    jpg_files = [f for f in os.listdir(jpg_dir) if f.endswith('.jpg')]
    
    # Crear un conjunto con los nombres de los archivos .jpg (sin extensión)
    jpg_filenames = {os.path.splitext(f)[0] for f in jpg_files}
    
    # Recorrer todos los archivos .txt
    for txt_file in txt_files:
        # Obtener el nombre del archivo .txt sin extensión
        txt_filename = os.path.splitext(txt_file)[0]
        
        # Verificar si existe un archivo .jpg con el mismo nombre
        if txt_filename in jpg_filenames:
            # Construir la ruta completa del archivo .txt de origen
            source_path = os.path.join(txt_dir, txt_file)
            
            # Construir la ruta completa del archivo .txt de destino
            destination_path = os.path.join(output_dir, txt_file)
            
            # Copiar el archivo .txt a la carpeta de salida
            shutil.copy(source_path, destination_path)
            
            # Mostrar un mensaje indicando que el archivo fue copiado
            print(f"Archivo {txt_file} copiado a {output_dir}")

# Configuración de las carpetas
txt_dir = r'backend/Dollar_Bill_Detection/datasets _division-copy/output/labels'  # Carpeta de archivos .txt
jpg_dir = r'backend/Dollar_Bill_Detection/datasets _division-copy/output/image'  # Carpeta de archivos .jpg
output_dir = r'Dollar_Bill_Detection/datasets _division-copy/output/label_new'  # Carpeta de salida para los archivos .txt copiados

# Llamar a la función para comparar y copiar los archivos
compare_and_copy(txt_dir, jpg_dir, output_dir)
