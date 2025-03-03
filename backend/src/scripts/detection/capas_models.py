from ultralytics import YOLO
"""
Este script se encarga de cargar el modelo YOLO preentrenado y mostrar la estructura del modelo.
"""
# Cargar el modelo
model = YOLO(r'backend/Dollar_Bill_Detection_USD/yolov8s.pt') 

# Imprimir la estructura del modelo
print(model.model)