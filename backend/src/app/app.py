from ultralytics import YOLO
from PIL import Image
from log import log
import io
# Carga del modelo YOLO

models = {
    'USD': YOLO('backend/src/models/Dollar_Model_11.pt'),
    'VEF': YOLO('backend/src/models/VEF_Model_06.pt'),
}

versions = {
    'USD': 11,
    'VEF': 6,
}

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

from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/detection/vef")
async def detection_vef(image: UploadFile):
    imageBytes = await image.read()
    imageStream = io.BytesIO(imageBytes)
    imageFile = Image.open(imageStream)

    results = models['VEF'].predict(imageFile, verbose=False)

    if len(results[0].boxes) > 0:
        boxes = []
        for box in results[0].boxes:
            boxes.append({
                'label': classes['VEF'][int(box.cls.item())], # Clase detectada
                'confidence': box.conf.item(),   # Confianza
                'bbox': box.xyxy.tolist()        # Coordenadas del cuadro
            })
        print(boxes)
        await log(f'backend/src/data/img-API/VEF/Model_{versions['VEF']}/', boxes, imageFile)
        return {'detections': boxes}
    else:
        return {'message': 'No objects detected'}

@app.post("/detection/usd")
async def detection_usd(image: UploadFile):
    imageBytes = await image.read()
    imageStream = io.BytesIO(imageBytes)
    imageFile = Image.open(imageStream)

    results = models['USD'].predict(imageFile, verbose=False)

    if len(results[0].boxes) > 0:
        boxes = []
        for box in results[0].boxes:
            boxes.append({
                'label': classes['USD'][int(box.cls.item())], # Clase detectada
                'confidence': box.conf.item(),   # Confianza
                'bbox': box.xyxy.tolist()        # Coordenadas del cuadro
            })
        print(boxes)
        await log(f'backend/src/data/img-API/USD/Model_{versions['USD']}/', boxes, imageFile)
        return {'detections': boxes}
    else:
        return {'message': 'No objects detected'}
