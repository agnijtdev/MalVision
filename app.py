import os
import io
import base64
import numpy as np
from PIL import Image
from flask import Flask, request, jsonify, render_template
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras import layers, models

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'exe', 'dll', 'bin', 'msi', 'sys', 'elf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# --- MODEL ARCHITECTURE ---
def build_model():
    base_model = VGG16(weights=None, include_top=False, input_shape=(224, 224, 3))
    model = models.Sequential([
        layers.Input(shape=(224, 224, 3)),
        layers.Cropping2D(cropping=((30, 0), (0, 0))), # Header removal
        layers.Resizing(224, 224),
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),
        layers.Dense(25, activation='softmax')
    ])
    return model

model = build_model()
try:
    model.load_weights('./models/malvision_model.h5') 
    print("✅ Weights Loaded")
except Exception as e:
    print(f"❌ Load Error: {e}")

CLASSES = ['Adialer.C', 'Agent.FYI', 'Allaple.A', 'Allaple.L', 'Alueron.gen!J', 
           'Autorun.K', 'C2LOP.P', 'C2LOP.gen!g', 'Dialplatform.B', 'Dontovo.A', 
           'Fakerean', 'Instantaccess', 'Lolyda.AA1', 'Lolyda.AA2', 'Lolyda.AA3', 
           'Lolyda.AT', 'Malex.gen!J', 'Obfuscator.AD', 'Rbot!gen', 'Skintrim.N', 
           'Swizzor.gen!E', 'Swizzor.gen!I', 'VB.AT', 'Wintrim.BX', 'Yuner.A']

# --- HELPER: BINARY TO IMAGE ---
def get_processed_image(file_bytes):
    d = np.frombuffer(file_bytes, dtype=np.uint8)
    size = len(d)
    # Standard Malimg Width Logic
    if size < 10240: width = 32
    elif size < 61440: width = 128
    elif size < 204800: width = 384
    elif size < 512000: width = 512
    else: width = 1024
    
    height = int(size / width)
    if height == 0: height = 1
    img_matrix = np.reshape(d[:height * width], (height, width))
    return Image.fromarray(img_matrix).resize((224, 224)).convert("RGB")

@app.route('/')
def home():
    return render_template('index.html')

# STEP 2: CONVERT TO IMAGE
@app.route('/convert', methods=['POST'])
def convert():
    file = request.files.get('file')
    if not file: return jsonify({'error': 'No file'})
    
    try:
        img = get_processed_image(file.read())
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return jsonify({'image': img_str})
    except Exception as e:
        return jsonify({'error': str(e)})

# STEP 3: ANALYZE PATTERNS
@app.route('/analyze', methods=['POST'])
def analyze():
    file = request.files.get('file')
    if not file: return jsonify({'error': 'No file'})
    
    try:
        img = get_processed_image(file.read())
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        preds = model.predict(img_array)
        idx = np.argmax(preds[0])
        conf = float(np.max(preds[0])) * 100
        
        return jsonify({
            'family': CLASSES[idx],
            'confidence': f"{conf:.2f}",
            'status': 'Malicious' if conf > 70 else 'Suspicious'
        })
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)