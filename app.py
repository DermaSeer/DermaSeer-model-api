from flask import Flask, request, jsonify
import numpy as np
import requests
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet import preprocess_input
from io import BytesIO
from PIL import Image
import firebase_admin
from firebase_admin import credentials, auth

app = Flask(__name__)

cred = credentials.Certificate('firebaseAdmin.json')
firebase_admin.initialize_app(cred)

model = load_model('model-dermaseer-mobilenet.keras') 

class_indices = {0: 'f', 1: 'fu', 2: 'n', 3: 'p', 4: 'pa'}
class_labels = list(class_indices.values())

descriptions = {
    'f': 'Fulminans',
    'fu': 'Fungal',
    'n': 'Nodules',
    'p': 'Postula',
    'pa': 'Papula'
}

def predict_acne_type(img_url, model):
    try:
        response = requests.get(img_url)
        img = Image.open(BytesIO(response.content))

        img = img.resize((224, 224)) 
        img_array = np.array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)

        predictions = model.predict(img_array)[0]
        predicted_class_index = np.argmax(predictions)
        predicted_class_label = class_indices[predicted_class_index]

        results = {class_labels[i]: float(predictions[i]) for i in range(len(predictions))}
        return predicted_class_label, results
    except Exception as e:
        print(f"Error While Processing Image: {e}")
        return None, {}

def token_required(f):
    def decorator(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return jsonify({'error': 'Unauthorized'}), 401
        try:
            decoded_token = auth.verify_id_token(token)
            request.user = decoded_token
        except Exception as e:
            return jsonify({'error': 'Unauthorized, Please login again'}), 401
        return f(*args, **kwargs)
    return decorator

@app.route('/predict', methods=['POST'])
@token_required
def predict():
    data = request.get_json()
    img_url = data.get('img_url')
    
    if not img_url:
        return jsonify({'error': 'No image URL provided'}), 400

    predicted_label, probabilities = predict_acne_type(img_url, model)

    if predicted_label:
        response = {
            'data': {
            'predicted_acne_type': descriptions[predicted_label],
            'probabilities': {descriptions[class_indices[class_labels.index(acne_type)]]: round(prob, 2) for acne_type, prob in probabilities.items()}
        }
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Prediction failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)