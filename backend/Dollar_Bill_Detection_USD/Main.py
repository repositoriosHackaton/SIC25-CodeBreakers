from ultralytics import YOLO
import torch.multiprocessing as mp

#Agregando una ruta dinámica para los datasets
from ultralytics import settings
settings.update(datasets_dir = '.')

def train_model():
    # Cargar el modelo YOLO preentrenado
    model = YOLO("yolov8n.yaml") 
    
    # Entrenar el modelo
    results = model.train(data=r'C:\Users\jesus\Desktop\Clones\cash_reader\backend\Dollar_Bill_Detection\data.yaml', epochs = 100)
    print(results)

if __name__ == "__main__":
    mp.freeze_support()  #Evitar un error con Windows
    train_model()  #Llamar a la función que entrena el modelo

