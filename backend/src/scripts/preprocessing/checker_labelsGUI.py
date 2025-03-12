import os
import math
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

# Lista de nombres de clases (ajústala según tu configuración)
CLASS_NAMES = [
    "fifty-back",
    "fifty-front",
    "five-back",
    "five-front",
    "one-back",
    "one-front",
    "ten-back",
    "ten-front",
    "twenty-back",
    "twenty-front",
    "one_hundred-back",
    "one_hundred-front",
]

def load_labels(label_path):
    """
    Lee el archivo de labels y devuelve una lista de tuplas:
    (class_id, xc, yc, w, h, angle)
    Se asume que los valores están separados por espacios y que xc, yc, w, h están normalizados.
    """
    labels = []
    if os.path.exists(label_path):
        with open(label_path, "r") as f:
            for line in f.readlines():
                parts = line.strip().split()
                if len(parts) >= 6:
                    cls_id = int(parts[0])
                    xc = float(parts[1])
                    yc = float(parts[2])
                    w = float(parts[3])
                    h = float(parts[4])
                    angle = float(parts[5])
                    labels.append((cls_id, xc, yc, w, h, angle))
    return labels

def compute_rotated_box(xc, yc, w, h, angle, img_width, img_height):
    """
    Convierte las coordenadas normalizadas y el ángulo (en grados) a una lista de 4 puntos (x,y) en píxeles.
    Se asume que (xc, yc) es el centro, y w y h son el ancho y alto normalizados.
    """
    # Convertir a píxeles
    cx_px = xc * img_width
    cy_px = yc * img_height
    w_px = w * img_width
    h_px = h * img_height

    # Convertir el ángulo a radianes
    theta = math.radians(angle)
    # Mitades
    dw = w_px / 2.0
    dh = h_px / 2.0

    # Definir las esquinas sin rotar (relativas al centro)
    corners = [
        (-dw, -dh),
        ( dw, -dh),
        ( dw,  dh),
        (-dw,  dh)
    ]
    # Rotar cada esquina y trasladarla al centro
    rotated = []
    for x, y in corners:
        xr = x * math.cos(theta) - y * math.sin(theta)
        yr = x * math.sin(theta) + y * math.cos(theta)
        rotated.append((cx_px + xr, cy_px + yr))
    return rotated

class LabelViewer:
    def __init__(self, root, dataset_dir):
        self.root = root
        self.dataset_dir = dataset_dir
        self.images_dir = os.path.join(dataset_dir, "images")
        self.labels_dir = os.path.join(dataset_dir, "labels")
        # Listar los archivos de imagen (filtrando por extensión común)
        self.image_files = sorted([f for f in os.listdir(self.images_dir)
                                    if f.lower().endswith((".jpg", ".jpeg", ".png"))])
        self.index = 0

        # Configurar la interfaz
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        self.prev_button = tk.Button(btn_frame, text="Anterior", command=self.prev_image)
        self.prev_button.pack(side=tk.LEFT, padx=5)
        self.next_button = tk.Button(btn_frame, text="Siguiente", command=self.next_image)
        self.next_button.pack(side=tk.LEFT, padx=5)

        self.info_label = tk.Label(root, text="")
        self.info_label.pack(pady=5)

        self.show_image()

    def show_image(self):
        if not self.image_files:
            self.info_label.config(text="No hay imágenes en el directorio")
            return

        # Obtener nombre y ruta de la imagen actual
        image_filename = self.image_files[self.index]
        image_path = os.path.join(self.images_dir, image_filename)
        # Construir la ruta del label (asumiendo misma base y extensión .txt)
        label_filename = os.path.splitext(image_filename)[0] + ".txt"
        label_path = os.path.join(self.labels_dir, label_filename)

        # Cargar la imagen y convertirla a RGB
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        img_width, img_height = image.size

        # Cargar y dibujar los labels (si existen)
        labels = load_labels(label_path)
        for cls_id, xc, yc, w, h, angle in labels:
            box = compute_rotated_box(xc, yc, w, h, angle, img_width, img_height)
            # Dibujar la caja (se dibuja un polígono que conecta los 4 puntos)
            draw.line(box + [box[0]], fill="red", width=2)
            # Escribir el nombre de la clase en la primera esquina
            label_text = CLASS_NAMES[cls_id] if cls_id < len(CLASS_NAMES) else str(cls_id)
            draw.text(box[0], label_text, fill="blue")

        # Ajustar la imagen para que se visualice en el canvas (manteniendo la relación de aspecto)
        image.thumbnail((800, 600), Image.ANTIALIAS)
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.config(width=self.photo.width(), height=self.photo.height())
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

        # Actualizar la información de la imagen actual
        self.info_label.config(text=f"{self.index+1}/{len(self.image_files)}: {image_filename}")

    def next_image(self):
        if self.index < len(self.image_files) - 1:
            self.index += 1
            self.show_image()

    def prev_image(self):
        if self.index > 0:
            self.index -= 1
            self.show_image()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Visualizador de Labels YOLOv8-OBB")
    # Permite al usuario seleccionar el directorio del dataset
    dataset_dir = filedialog.askdirectory(title="Selecciona el directorio del dataset")
    if dataset_dir:
        viewer = LabelViewer(root, dataset_dir)
        root.mainloop()
