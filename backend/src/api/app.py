from flask import Flask, jsonify, request
import numpy as np
from PIL import Image
from ultralytics import YOLO
from flask_cors import CORS

from werkzeug.utils import secure_filename
import cv2
import os

from log import log
from logging.config import dictConfig
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s]: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
CORS(app)

DEBUG = False
HOST = '127.0.0.1'
PORT = 5000

# Carga del modelo YOLO
model = YOLO('backend/src/models/VEF_Model_06.pt')

classes = [
    'fifty-back-vef',       'fifty-front-vef',
    'five-back-vef',        'five-front-vef',
    'ten-back-vef',         'ten-front-vef',
    'twenty-back-vef',      'twenty-front-vef',
    'one_hundred-back-vef', 'one_hundred-front-vef',
    'two_hundred-back-vef', 'two_hundred-front-vef'
]

''' Dolares
classes = [
    'fifty-back',  'fifty-front', 
    'five-back',   'five-front', 
    'one-back',    'one-front', 
    'ten-back',    'ten-front', 
    'twenty-back', 'twenty-front',
    'one_hundred-back', 'one_hundred-front',
]
'''
@app.route('/detection', methods=['POST'])
def bill_detection():
    # Verificar si la solicitud incluye un archivo de imagen
    if 'image' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            filename = secure_filename(file.filename)
            file_path = os.path.join('backend/src/api/uploads/', filename)
            file.save(file_path)

            # Preprocesar la imagen
            img = Image.open(file_path).convert("RGB")
            #img = np.array(img)

            app.logger.info("\n")
            app.logger.info(img.size)
            app.logger.info(f'{len(img.tobytes()) / (1024 * 1024)} MB')

            # Realizar predicción con el modelo YOLO
            results = model.predict(img)

            # Eliminar el archivo temporal
            os.remove(file_path)

            # Procesar resultados del modelo
            if len(results[0].boxes) > 0:
                boxes = []
                for box in results[0].boxes:
                    boxes.append({
                        'label': classes[int(box.cls.item())],          # Clase detectada
                        'confidence': box.conf.item(),   # Confianza
                        'bbox': box.xyxy.tolist()        # Coordenadas del cuadro
                    })
                app.logger.info(boxes)
                log('backend/src/api/logs/VEF6/', boxes, img)
                # Retornar todos los boxes como un array
                return jsonify({'detections': boxes}), 200
            else:
                # Si no hay detecciones
                return jsonify({'message': 'No objects detected'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
