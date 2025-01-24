from ultralytics import YOLO
import torch.multiprocessing as mp
import torch
import torch.nn as nn

#Agregando una ruta dinámica para los datasets
from ultralytics import settings
settings.update(datasets_dir = '.')

def train_model():
    # Cargar el modelo YOLO preentrenado
    model = YOLO("yolov8n.yaml") 
    
    class_weights = torch.tensor([1.3, 1.3, 1.7, 1.7, 1.0, 1.0, 1.5, 1.5, 1.7, 1.7, 0.8, 0.8])  # Pesos de las clases
    # Entrenar el modelo
    results = model.train(
        data=r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection_USD\data.yaml',
        epochs = 70,
        batch = 16,
        imgsz = 640,
        device = '0',)
    print(results)

if __name__ == "__main__":
    mp.freeze_support()  #Evitar un error con Windows
    train_model()  #Llamar a la función que entrena el modelo

