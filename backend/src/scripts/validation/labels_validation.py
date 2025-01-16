import os

def check_labels_for_boxes(label_dir, output_file):
    valid = True
    incorrect_labels = []
    
    for label_file in os.listdir(label_dir):
        if label_file.endswith('.txt'):
            with open(os.path.join(label_dir, label_file), 'r') as f:
                lines = f.readlines()
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) != 5:
                        valid = False
                        incorrect_labels.append(label_file)
                        print(f"Formato incorrecto en el archivo: {label_file} - {line.strip()}")
                        break
    
    if valid:
        print("Todos los archivos de etiquetas están en formato de boxes para YOLO.")
    else:
        print("Hay archivos de etiquetas con formato incorrecto.")
        # Escribir los nombres de los archivos incorrectos en un archivo de texto
        with open(output_file, 'w') as f:
            for label in incorrect_labels:
                f.write(f"{label}\n")
        print(f"Lista de archivos de etiquetas incorrectos guardada en {output_file}")

# Ruta a la carpeta que contiene los archivos de etiquetas
label_dir = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection\valid\labels'
# Ruta al archivo de salida para los nombres de los archivos incorrectos
output_file = r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection\valid\incorrect_labels.txt'

check_labels_for_boxes(label_dir, output_file)
