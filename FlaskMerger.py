import torch
import torchvision.transforms as transforms
import torchvision.models as models
from flask import Flask, request, jsonify
from PIL import Image
import io
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Flask is running! Use /predict/ for image classification."

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load AlexNet model
num_classes = 6  # Update to match your trained model
model = models.alexnet(weights=None)  # No pretrained weights, we use custom
num_ftrs = model.classifier[6].in_features
model.classifier[6] = torch.nn.Linear(num_ftrs, num_classes)

# Load trained weights
model.load_state_dict(torch.load("alexnet_trained.pth", map_location=device))
model.eval()
model.to(device)

# Image Preprocessing (AlexNet expects 227x227 images)
transform = transforms.Compose([
    transforms.Resize((227, 227)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Class Labels
class_names = ["Blast - increase Nitrogen supply", "BLB - reduce Nitrogen supply", "Plant is perfectly healthy", "Hispa - Reduce Fertilizer Quantity", "Leaf Miner - Remove Dead and Infested Leaves", "Leaf Spot - Ensure sanitation and increase Potassium"]  # Update accordingly

# Prediction Function
def predict(image):
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        output = model(image)
        _, predicted = torch.max(output, 1)
    return class_names[predicted.item()]

# API Endpoint for Prediction
@app.route("/predict/", methods=["POST"])
def predict_image():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]
    image = Image.open(io.BytesIO(file.read())).convert("RGB")  # Convert to RGB
    prediction = predict(image)

    return jsonify({"prediction": prediction})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
