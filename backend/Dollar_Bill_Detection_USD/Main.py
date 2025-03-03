from ultralytics import YOLO
import torch.multiprocessing as mp
import torch
import torch.nn as nn

#Agregando una ruta dinámica para los datasets
from ultralytics import settings
settings.update(datasets_dir = '.')

def train_model():
    # Cargar el modelo YOLO preentrenado
    model = YOLO(r'./../../yolov8s.pt') 

    # Entrenar el modelo
    results = model.train(
        data=r'backend/Dollar_Bill_Detection_USD/data.yaml',
        epochs = 350,
        batch = 16,
        imgsz = 416,
        cls=0.7,
        patience = 10, #Detener el entrenamiento si no hay mejora en 10 epochs
        optimizer = "SGD",
        #freeze = [0,1], #indice de las cpas que se congelarán
        task = "detect",
    )
    print(results)

if __name__ == "__main__":
    mp.freeze_support()  #Evitar un error con Windows
    train_model()  #Llamar a la función que entrena el modelo
 
