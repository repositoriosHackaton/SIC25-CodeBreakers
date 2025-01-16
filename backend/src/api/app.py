from flask import Flask, jsonify, request
import numpy as np
from PIL import Image
from ultralytics import YOLO
from flask_cors import CORS

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

DEBUG = True
HOST = '127.0.0.1'
PORT = 5000

# Carga del modelo YOLO
model = YOLO('backend/src/models/Dollar_Model.pt')
classes = [
    'fifty-back',  'fifty-front', 
    'five-back',   'five-front', 
    'one-back',    'one-front', 
    'ten-back',    'ten-front', 
    'twenty-back', 'twenty-front',
    'one_hundred-back', 'one_hundred-front',
]

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
            # Leer la imagen directamente desde la memoria
            img = Image.open(file.stream).convert("RGB")
            img = np.array(img)

            # Realizar predicción con el modelo YOLO
            results = model.predict(img, verbose=False)

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
                app.logger.info("\n")
                # Retornar todos los boxes como un array
                return jsonify({'detections': boxes}), 200
            else:
                # Si no hay detecciones
                return jsonify({'message': 'No objects detected'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host=HOST, port=PORT)
