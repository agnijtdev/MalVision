# MalVision: Pattern-Based AI Malware Classifier

MalVision is an end-to-end deep learning and computer vision pipeline designed to classify malware families using static structural analysis. By converting raw binary executables into visual textures, the system leverages a Convolutional Neural Network (CNN) based on the VGG16 architecture to identify malicious payloads while remaining resilient to header-obfuscation and metadata spoofing.

---

## 🚀 Key Features

* **Binary-to-Texture Transformation:** Converts raw bytes from compiled executables (`.exe`, `.dll`, etc.) into 2D structural intensity matrices rescaled to 224x224 RGB images.
* **Metadata-Bias Elimination:** Integrates a custom `Cropping2D` layer directly into the neural network topology to trim the top 30 pixels, effectively blinding the model to standard PE headers and forcing feature extraction from core code/data sections.
* **Three-Step Web Interface:** Features a clean, state-driven UI built with Flask and Bootstrap 5 that splits the operational workflow into explicit Upload, Visual Conversion, and Deep Learning Inference phases.
* **High-Confidence Classification:** Built to map visual entropy patterns across 25 distinct malware families from the benchmark Malimg dataset.

---

## 📦 Project Architecture

```text
/MalVision-Engine
│
├── app.py                     # Flask backend with VGG16 model setup & routes
├── requirements.txt           # Verified package dependency manifest
├── models/    
|   └──malvision_model.h5         # Pre-trained CNN weights file
│
├── templates/
│   └── index.html             # State-driven Bootstrap 5 web interface
│
└── venv/                      # Local isolated Python environment



⚙️ Model Specification & Optimization

The network uses transfer learning on a top-truncated VGG16 base model compiled with specific mathematical properties optimized for binary image classification:

Optimizer: Adam (Adaptive Moment Estimation) combining Momentum and RMSProp characteristics to handle gradient updating across sharp and flat entropy surfaces alike.

Loss Function: categorical_crossentropy targeting cross-entropy optimization across the 25 distinct categorical malware distribution profiles.

Input Layer Geometry: Operates with an initial input shape constraints matrix of (224, 224, 3).




🛠️ Installation & Setup

1. Environment Isolation

        # Navigate to the project root
        cd path/to/malvision

        # Create the virtual environment
        python -m venv venv

2. Execution Policy & Activation

    For PowerShell:
        Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
        .\venv\Scripts\Activate.ps1
    
    For Command Prompt:
        venv\Scripts\activate

3. Install Dependencies
    pip install -r requirements.txt

4. Running the Application
    4.1 python app.py
    4.2 Open your web browser and navigate to: http://127.0.0.1:5000"# MalVision" 
