from ultralytics import YOLO
import torch.multiprocessing as mp

def train_model():
    # Cargar el modelo YOLO preentrenado
    model = YOLO("yolov8n.yaml") 
    
    # Entrenar el modelo
    results = model.train(data=r'C:\Users\jesus\Desktop\PRUEBA_TENSOR\Dollar_Bill_Detection\data.yaml', epochs = 1)
    print(results)

if __name__ == "__main__":
    mp.freeze_support()  # Esto es necesario para Windows
    train_model()  # Llamar a la función que entrena el modelo
