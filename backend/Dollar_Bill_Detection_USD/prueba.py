from ultralytics import YOLO

# Cargar el modelo
model = YOLO(r'C:\Users\jesus\Documents\Proyectos\Cashreader\yolov8m.pt') 

# Imprimir la estructura del modelo
print(model.model)