from ultralytics import YOLO
from PIL import Image
from log import log
import io

# Activar recorte y centrado
if (ROI_ACTIVATION:=False):
    from roi import procesar_imagen

# Modelos para el server
models = {
    'USD': YOLO('backend/src/models/train/USD_Model_13/weights/best.pt'),
    'VEF': YOLO('backend/src/models/train/VEF_Model_09/weights/best.pt'),
}

# Versiones de los modelos
versions = {
    'USD': 13,
    'VEF': 9,
}

# Clases de los modelos
classes = {
    'USD': [
        'fifty-back',  'fifty-front', 
        'five-back',   'five-front', 
        'one-back',    'one-front', 
        'ten-back',    'ten-front', 
        'twenty-back', 'twenty-front',
        'one_hundred-back', 'one_hundred-front',
    ],
    'VEF': [
        'fifty-back-vef',       'fifty-front-vef',
        'five-back-vef',        'five-front-vef',
        'ten-back-vef',         'ten-front-vef',
        'twenty-back-vef',      'twenty-front-vef',
        'one_hundred-back-vef', 'one_hundred-front-vef',
        'two_hundred-back-vef', 'two_hundred-front-vef'
    ]
}

# Importamos FastAPI
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

# Creamos la app del FastAPI
app = FastAPI()
# Se agrega el CORS para aceptar peticiones de un origen externo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/detection/")
async def detection_vef(image: UploadFile):
    # Se carga la imagen de forma dinámica
    imageBytes = await image.read()
    imageStream = io.BytesIO(imageBytes)
    imageFile = Image.open(imageStream)

    #TODO Aquí iría la clasificación del modelo para inferir si es VEF o USD
    currency = 'VEF'

    # Se recorta y se centra, o no
    if ROI_ACTIVATION:
        results = models[currency].predict(procesar_imagen(imageFile), verbose=False) # Se pasa la imagen por el modelo
    else:
        results = models[currency].predict(imageFile, verbose=False) # Se pasa la imagen por el modelo

    # Se extraen las cajas de los resultados
    if len(results[0].boxes) > 0:
        boxes = []
        for box in results[0].boxes:
            boxes.append({
                'label': classes[currency][int(box.cls.item())], # Clase detectada
                'confidence': box.conf.item(),   # Confianza
                'bbox': box.xyxy.tolist()        # Coordenadas del cuadro
            })
        print(boxes)
        # Guardamos los resultados en la carpeta img-API
        await log(f'backend/src/data/img-API/VEF/Model_{versions[currency]}/', boxes, imageFile)
        # Retornamos los resultados
        return {'detections': boxes}
    else:
        return {'message': 'No objects detected'}
