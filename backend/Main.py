from ultralytics import YOLO, settings
import torch.multiprocessing as mp
from PIL import Image
import json
import numpy as np
import os
import cv2

#Agregando una ruta dinámica para los datasets

settings.update(datasets_dir = '.')

def train_model(m_name, moneda, disable=False):
    if disable:
        pass
    else:
        if moneda=="VEF" or moneda=="USD":
            # Cargar el modelo YOLO preentrenado
            model = YOLO(r'backend/src/models/YOLO/yolov8s.pt') 

            # Entrenar el modelo
            results = model.train(
                data=f"backend/datasets/{moneda}/dataset-extend-{moneda}/data.yaml",
                project = r'backend/src/models/train', #Ruta donde se guardará el modelo
                name = m_name, #Nombre de la carpeta del modelo
                epochs = 400,
                batch = 32,
                imgsz = 416,
                patience = 20, #Detener el entrenamiento si no hay mejora en 10 epochs
                optimizer = "SGD",
                #freeze = [0,1], #indice de las cpas que se congelarán
                task = "detect",
            )
            print(results)
            
        else:
            print("\nrevisar los parametros asignados en la llamada de la funcion")
    
def test_model(m_name, moneda, evaluate_model, disable=False):
    if disable:
        pass
    else:
        if moneda=="VEF" or moneda=="USD":
            
            model = YOLO(f"backend/src/models/train/{evaluate_model}/weights/best.pt") #reemplazar por modelo a probar
            
            # Evaluar en el conjunto de test
            results = model.val(
                data=f"backend/datasets/{moneda}/dataset-extend-{moneda}/data.yaml",  # Archivo YAML con rutas a los datos
                project = r'backend/src/models/train', #Ruta donde se guardará la validacion(test)
                name = m_name, #Nombre de la carpeta de la validacion(test)
                split="test",      # Especifica que use el conjunto de test
                batch=16,          # Tamaño del batch
                imgsz=416,         # Tamaño de la imagen
                conf=0.96,         # Umbral de confianza
                iou=0.8,          # Umbral de IoU
                device=0,          # especifica el uso de GPU
                plots= True, # genera y guarda gráficos de predicciones frente a la verdad sobre el   terreno para una evaluación visual del rendimiento del modelo.
                rect = True
            )  
            
            """
            Aumentar iou: Más estricto, solo considera detecciones con alta superposición (mejor precisión, menor recall).

            Disminuir iou: Más flexible, permite más detecciones (mejor recall, menor precisión)
            
            *Recomendaciones para Ajustar conf e iou
            Valores por Defecto:
            Usa conf=0.001 e iou=0.6 como punto de partida.

            Si Priorizas Precisión:
            Aumenta conf (ej: 0.5) y iou (ej: 0.6).

            Si Priorizas Recall:
            Disminuye conf (ej: 0.1) y iou (ej: 0.3).
            """

            # Mostrar métricas
            print("\nMetricas:")
            for metric, value in results.results_dict.items():
                print(f"{metric.replace("metrics/", "")}: {value}\n")
        
        else:
            print("\nrevisar los parametros asignados en la llamada de la funcion")
    
def evalPredict_model(evaluate_model, image_path, conf_threshold=0.25, iou_threshold=0.45, use_pil=True, disable=False):
    """
    Args:
        model (YOLO): Modelo YOLO cargado y entrenado.
        image_path (str): Ruta de la imagen a predecir.
        conf_threshold (float): Umbral de confianza para las detecciones (por defecto 0.25).
        iou_threshold (float): Umbral de IoU para la supresión no máxima (por defecto 0.45).
        use_pil (bool): Si es True, usa PIL para cargar la imagen. Si es False, usa OpenCV.

    Returns:
        dict: Diccionario con las predicciones y métricas.
    """
    # Cargar la imagen usando PIL o OpenCV
    
    if disable:
        pass
    else:
        model = YOLO(f"backend/src/models/train/{evaluate_model}/weights/best.pt")
        
        if use_pil:
            # Usar PIL para cargar la imagen
            image = Image.open(image_path)
            if image is None:
                raise ValueError(f"No se pudo cargar la imagen en {image_path}")
            # Convertir la imagen a un array de NumPy y cambiar de RGB a BGR
            #image = np.array(image)  # Convierte a un array de NumPy
            #image = image[:, :, ::-1]  # Convierte de RGB a BGR
        else:
            # Usar OpenCV para cargar la imagen
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError(f"No se pudo cargar la imagen en {image_path}")

        # Realizar la predicción
        results = model.predict(
            source=image,
            conf=conf_threshold,
            iou=iou_threshold,
            imgsz=416,  # Tamaño de la imagen para la predicción
            device=0,
            save=False,  # No guardar la imagen predicha
            show=False,  # No mostrar la imagen predicha
        )

        # Procesar las predicciones
        predictions = []
        for result in results:
            for box in result.boxes:
                # Obtener las coordenadas, confianza y clase
                x1, y1, x2, y2 = box.xyxy[0].tolist()  # Coordenadas de la caja
                confidence = box.conf.item()            # Confianza de la detección
                class_id = box.cls.item()               # ID de la clase
                class_name = model.names[class_id]      # Nombre de la clase

                # Guardar la predicción
                predictions.append({
                    "bbox": [x1, y1, x2, y2],
                    "confidence": confidence,
                    "class_id": class_id,
                    "class_name": class_name,
                })

        # Devolver las predicciones y métricas
        return {
            "image_path": image_path,
            "predictions": predictions,
            "metrics": {
                "num_detections": len(predictions),
                "average_confidence": sum(p["confidence"] for p in predictions) / len(predictions) if predictions else 0,
            },
        }
    
def fastPredict_log(model_path, image_path, conf_threshold=0.25, iou_threshold=0.45):
    """
    Realiza predicciones en una imagen y devuelve resultados en formato específico del server
    
    Args:
        image_path (str): Ruta completa a la imagen
        model_path (str): Ruta al archivo .pt del modelo
        conf_threshold (float): Umbral de confianza mínimo
    
    Returns:
        list: Lista de detecciones en el formato solicitado
    """
    try:
        # Cargar modelo y realizar predicción
        model = YOLO(model_path)
        img = Image.open(image_path)
        
        # Realizar predicción
        results = model.predict(
            source=img,
            conf=conf_threshold,
            iou=iou_threshold,
            imgsz=416,
            device=0,
            save=False,
            show=False
            
        )
        
        # Procesar resultados
        detections = []
        for result in results:
            for box in result.boxes:
                detection = {
                    "label": model.names[int(box.cls.item())],
                    "confidence": round(box.conf.item(), 4),
                    "bbox": [box.xyxy[0].tolist()]
                }
                detections.append(detection)
        
        return detections
    
    except Exception as e:
        print(f"Error procesando {image_path}: {str(e)}")
        return []
    
def predModel_iterable(model_directory, input_dir, output_dir, conf_threshold=0.25, iou_threshold=0.45):
    """
    Procesa todas las imágenes en un directorio y guarda resultados en archivos .txt
    
    Args:
        model_directory (str): Directorio del modelo (contiene weights/best.pt)
        input_dir (str): Directorio con imágenes de entrada
        output_dir (str): Directorio para guardar los resultados
        conf_threshold (float): Umbral de confianza mínimo
    """
    # Configurar rutas
    model_path = os.path.join(model_directory, "weights", "best.pt")
    os.makedirs(output_dir, exist_ok=True)

    # Procesar imágenes
    for filename in os.listdir(input_dir):
        if filename.endswith("_orign.jpg"):
            # Construir rutas
            input_path = os.path.join(input_dir, filename)
            base_name = filename.replace("_orign.jpg", "")
            output_filename = f"{base_name}_json.txt"
            output_path = os.path.join(output_dir, output_filename)
            
            # Realizar predicción
            detections = fastPredict_log(model_path, input_path, conf_threshold, iou_threshold)
            
            # Guardar resultados
            with open(output_path, 'w') as f:
                json.dump(detections, f, indent=2)
            
            print(f"Resultados guardados en: {output_path}")

if __name__ == "__main__":
    mp.freeze_support()  #Evitar un error con Windows

    train_model(
                m_name="VEF_model_14f", 
                moneda="VEF",
                disable=False
                )  #Llamar a la función que entrena el modelo

    """
    test_model(
                m_name="VEF_Model_09_Val_01f",
                moneda="USD",
                evaluate_model="VEF_Model_09",
                disable=True
                ) #Llamar a la funcion que evalua el modelo(test)
    """
    """
    r = evalPredict_model(evaluate_model="USD_Model_13",
                image_path="backend/Dollar_Bill_Detection_USD/test/images/IMG_2079_jpg.rf.99e98d88844006e9f948ace274d42b2e.jpg",
                use_pil=False,
                disable=True
                ) #Llammar a la funcion que realiza predicciones
    print(r)
    """
    """
    predModel_iterable(
    model_directory="backend/src/models/train/VEF_Model_09",
    input_dir="backend/src/data/img-data-vef/mergeLogs_model",
    output_dir="backend/src/data/img-data-vef/process_model_09",
    #conf_threshold=0.6,
    #iou_threshold=0.6
)
    """