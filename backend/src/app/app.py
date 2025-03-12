from ultralytics import YOLO
from PIL import Image
from log import log
import io

# Activar recorte y centrado
if (ROI_ACTIVATION:=False):
    from roi import procesar_imagen

# Modelos para el server
models = {
    'USD':        YOLO('backend/src/models/train/USD_model_plus_01/weights/best.pt'),
    'VEF':        YOLO('backend/src/models/train/VEF_model_13f/weights/best.pt'),
    'INFERENCIA': YOLO('backend/src/models/train/USD_VEF_Model_01j/weights/best.pt'),
}

# Versiones de los modelos
versions = {
    'USD': 'plus_01',
    'VEF': '13f',
    'INFERENCIA': '1',
}

# Clases de los modelos
classes = {
    'USD': [
        'fifty-back',        'fifty-front', 
        'five-back',         'five-front', 
        'one-back',          'one-front', 
        'one_hundred-back',  'one_hundred-front',
        'ten-back',          'ten-front', 
        'twenty-back',       'twenty-front',
    ],
    'VEF': [
        'fifty-back-vef',       'fifty-front-vef',
        'five-back-vef',        'five-front-vef',
        'one_hundred-back-vef', 'one_hundred-front-vef',
        'ten-back-vef',         'ten-front-vef', 
        'twenty-back-vef',      'twenty-front-vef', 
        'two_hundred-back-vef', 'two_hundred-front-vef', 
    ],
    'INFERENCIA': [
        'dollar_back', 'dollar_front',
        'vef_back', '   vef_front',
    ],
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

@app.post("/detection")
async def detection_vef(image: UploadFile):
    # Se carga la imagen de forma dinámica
    imageBytes = await image.read()
    imageStream = io.BytesIO(imageBytes)
    imageFile = Image.open(imageStream)

    # Se recorta y se centra si
    if ROI_ACTIVATION: # El ROI activado
        which_currency = models['INFERENCIA'].predict(procesar_imagen(imageFile), verbose=False)
        currency_label = classes['INFERENCIA'][int(which_currency[0].boxes[0].cls.item())]
        if 'vef' in currency_label:
            currency = 'VEF'
        else:
            currency = 'USD'
        results = models[currency].predict(procesar_imagen(imageFile), verbose=False) # Se pasa la imagen por el modelo

    else: # ROI no activado
        which_currency = models['INFERENCIA'].predict(imageFile, verbose=False)
        currency_label = classes['INFERENCIA'][int(which_currency[0].boxes[0].cls.item())]
        if 'vef' in currency_label:
            currency = 'VEF'
        else:
            currency = 'USD'
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
        await log(f'backend/src/data/img-API/{currency}/Model_{versions[currency]}/', boxes, imageFile)
        # Retornamos los resultados
        return {'detections': boxes}
    else:
        return {'message': 'No objects detected'}