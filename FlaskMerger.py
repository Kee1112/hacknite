from flask import Flask, request, jsonify
from torchvision import transforms
from PIL import Image
import torch
import io
from flask import Flask, request, jsonify
from torchvision import models, transforms
from PIL import Image
import torch
import io

# Load the trained AlexNet model correctly
MODEL_PATH = 'alexnet_trained.pth'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Define the AlexNet model
  # Set the model to evaluation mode

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    image = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(image)
        prediction = torch.argmax(output, dim=1).item()
        confidence = torch.softmax(output, dim=1).max().item()
    
    return jsonify({'class': str(prediction), 'confidence': confidence})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# Load the trained AlexNet model

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

# Flask app
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    image = transform(image).unsqueeze(0).to(device)
    
    with torch.no_grad():
        output = model(image)
        prediction = torch.argmax(output, dim=1).item()
        confidence = torch.softmax(output, dim=1).max().item()
    
    return jsonify({'class': str(prediction), 'confidence': confidence})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
